import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field, ConfigDict
from markitdown import MarkItDown
from chonkie import SemanticChunker
from qdrant_client import QdrantClient

class DocumentSearchToolInput(BaseModel):
    """Input schema for DocumentSearchTool."""
    query: str = Field(..., description="Query to search the document.")

class DocumentSearchTool(BaseTool):
    name: str = "DocumentSearchTool"
    description: str = "Search the document for the given query."
    args_schema: Type[BaseModel] = DocumentSearchToolInput
    
    model_config = ConfigDict(extra="allow")
    def __init__(self, file_path: str):
        """Initialize the searcher with a PDF file path and set up the Qdrant collection."""
        super().__init__()
        self.file_path = file_path
        self.client = QdrantClient(":memory:")  # For small experiments
        self._process_document()

    def _extract_text(self) -> str:
        """Extract raw text from PDF using MarkItDown."""
        md = MarkItDown()
        result = md.convert(self.file_path)
        return result.text_content

    def _create_chunks(self, raw_text: str) -> list:
        """Create semantic chunks from raw text."""
        chunker = SemanticChunker(
            embedding_model="minishlab/potion-base-8M",
            threshold=0.5,
            chunk_size=512,
            min_sentences=1
        )
        return chunker.chunk(raw_text)

    def _process_document(self):
        """Process the document and add chunks to Qdrant collection."""
        raw_text = self._extract_text()
        chunks = self._create_chunks(raw_text)
        
        docs = [chunk.text for chunk in chunks]
        metadata = [{"source": os.path.basename(self.file_path)} for _ in range(len(chunks))]
        ids = list(range(len(chunks)))

        self.client.add(
            collection_name="demo_collection",
            documents=docs,
            metadata=metadata,
            ids=ids
        )

    def _run(self, query: str) -> list:
        """Search the document with a query string."""
        relevant_chunks = self.client.query(
            collection_name="demo_collection",
            query_text=query
        )
        docs = [chunk.document for chunk in relevant_chunks]
        separator = "\n___\n"
        return separator.join(docs)


class FireCrawlWebSearchToolInput(BaseModel):
    """Input schema for FireCrawlWebSearchTool."""
    query: str = Field(..., description="Search query for web search.")


class FireCrawlWebSearchTool(BaseTool):
    name: str = "FireCrawlWebSearchTool"
    description: str = "Search the web using FireCrawl API for the given query."
    args_schema: Type[BaseModel] = FireCrawlWebSearchToolInput
    
    model_config = ConfigDict(extra="allow")
    
    def __init__(self):
        """Initialize the FireCrawl web search tool."""
        super().__init__()
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            print("Warning: FIRECRAWL_API_KEY not found in environment variables.")
    
    def _run(self, query: str) -> str:
        """Search the web with FireCrawl API."""
        try:
            # Import firecrawl if available
            from firecrawl import FirecrawlApp
            
            if not self.api_key or self.api_key == "your_firecrawl_api_key":
                return "FireCrawl API key not configured. Please set FIRECRAWL_API_KEY in your .env file. Get your free API key from https://www.firecrawl.dev"
            
            # Initialize FireCrawl
            app = FirecrawlApp(api_key=self.api_key)
            
            # Perform search
            search_results = app.search(query, limit=5)
            
            # Format results
            if search_results and 'data' in search_results:
                formatted_results = []
                for idx, result in enumerate(search_results['data'][:5], 1):
                    title = result.get('title', 'No title')
                    url = result.get('url', 'No URL')
                    snippet = result.get('description', result.get('content', 'No description'))[:300]
                    formatted_results.append(f"{idx}. {title}\nURL: {url}\n{snippet}\n")
                
                return "\n".join(formatted_results)
            else:
                return "No results found for the query."
                
        except ImportError:
            return "FireCrawl library not installed. Please install it with: pip install firecrawl-py"
        except Exception as e:
            return f"Error during web search: {str(e)}"


# Test the implementation
def test_document_searcher():
    # Test file path
    pdf_path = "/Users/akshaypachaar/Eigen/ai-engineering/agentic_rag/knowledge/dspy.pdf"
    
    # Create instance
    searcher = DocumentSearchTool(file_path=pdf_path)
    
    # Test search
    result = searcher._run("What is the purpose of DSpy?")
    print("Search Results:", result)

if __name__ == "__main__":
    test_document_searcher()
