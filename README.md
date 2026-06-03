<div align="center">
  <h1>Seekra: Agentic RAG - PDF Q&A</h1>
  
  <p><b>AI-Powered PDF Question Answering System using CrewAI and Groq</b></p>
  
  [![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)](#)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](#)
  [![Groq](https://img.shields.io/badge/Groq-Fast_Inference-f55036?style=for-the-badge)](#)
  [![CrewAI](https://img.shields.io/badge/CrewAI-Agents-ff6c37?style=for-the-badge)](#)
  [![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-ff4e42?style=for-the-badge)](#)
</div>

<br/>

Seekra enables users to upload PDF documents and execute natural language queries against their contents. The system leverages an agentic orchestration layer to retrieve context dynamically and synthesize coherent responses via open-weight language models.

## Features

- **PDF Ingestion & Indexing:** Direct uploading of PDF documents for immediate vector indexing and semantic search capabilities.
- **Agentic Response Pipeline:** Utilizes a dual-agent configuration (Retriever and Synthesizer) to ensure context isolation and reduce hallucination.
- **Dynamic Fallback Search:** Automatically queries the public internet via the Serper API when the primary local document lacks the required context.
- **Stateless Authentication:** Requires client-provided API keys injected at runtime, ensuring complete host-side database privacy and zero persistent secret storage.
- **Selectable Inference Engines:** Supports multiple Groq-hosted open-weight models (Llama 3.3, Mixtral, Gemma).
- **Zero-Cost Telemetry:** Operates natively via the Groq free-tier limits, bypassing traditional API costs associated with proprietary models.

---

## Quick Start

### 1. Acquire API Keys

The application operates without hardcoded backend secrets. You must supply your own development keys:
- **Groq API** (Required for core LLM inference): [console.groq.com](https://console.groq.com)
- **Serper API** (Optional for internet fallback): [serper.dev](https://serper.dev)

### 2. Local Setup

```bash
# Clone the repository
git clone https://github.com/devaldaki3/Seekra.git
cd Seekra

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### 3. Usage

1. Input your Groq API key in the sidebar configuration.
2. Select an active model (Defaults to Llama 3.3 70B).
3. Upload a target PDF document.
4. Execute queries against the document via the chat interface.

---

## Architecture & Technology Stack

- **Frontend Environment**: Streamlit
- **LLM Provider**: Groq API
- **Document Parser**: MarkItDown
- **Vector Pipeline**: Qdrant (Database) + Chonkie (Semantic Chunking) + FastEmbed (Embeddings)
- **Orchestration**: CrewAI
- **Web Search Integration**: Serper API

### System Flow
1. **Upload Phase**: A PDF is ingested into temporary volatile storage.
2. **Indexing Phase**: The document is converted to markdown, split semantically, and persisted to a localized ephemeral Qdrant vector space.
3. **Query Phase**: The user submits a query via the WebSocket thread.
4. **Retrieval**: The CrewAI Retriever Agent parses the query and invokes the `DocumentSearchTool` (or `SerperDevTool`).
5. **Synthesis**: The Synthesis Agent organizes the raw chunk data into a formatted response payload.
6. **Delivery**: The synthesized payload overrides the UI block.

---

## Project Structure

```text
Seekra/
├── app.py                    # Application entry point and UI definition
├── requirements.txt          # Python environment dependencies
├── README.md                 # Primary system documentation
├── .gitignore                # Target exclusions for version control
├── knowledge/                # Evaluation documents dataset
│   └── dspy.pdf            
└── src/
    └── agentic_rag/
        └── tools/
            └── custom_tool.py  # Qdrant client mapping and Tool class logic
```

---

## Streamlit Cloud Deployment

The stateless nature of the application allows for zero-configuration deployments.

1. **Initialize Remote Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Trigger Deployment**
   - Navigate to [share.streamlit.io](https://share.streamlit.io).
   - Authorize GitHub access and select the repository.
   - Designate `app.py` as the primary executable.
   - Execute the deployment. Secrets configuration in the Streamlit Cloud dashboard is unnecessary.

---



## Acknowledgments
- Implementation framework provided by **CrewAI**.
- Accelerated open-weight inference provided by **Groq**.
- Web interaction layer built on **Streamlit**.
- Vector optimizations handled via **Qdrant** and **Chonkie**.
