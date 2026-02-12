import streamlit as st
import os
import tempfile
import gc
import hashlib

from crewai import Agent, Crew, Process, Task, LLM
from src.agentic_rag.tools.custom_tool import DocumentSearchTool
try:
    from crewai_tools import SerperDevTool
    SERPER_AVAILABLE = True
except ImportError:
    SERPER_AVAILABLE = False

# Configuration
VERBOSE = False  # Set to True for debugging

# Helper function for file hashing
def file_hash(file):
    """Generate MD5 hash of file contents"""
    return hashlib.md5(file.getvalue()).hexdigest()

# Page config
st.set_page_config(
    page_title="Seekra",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS - ONE accent color, button styling only
st.markdown("""
<style>
    /* Single accent color */
    :root {
        --accent-color: #6366f1;
    }
    
    /* Button styling only */
    .stButton>button {
        background-color: var(--accent-color);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton>button:hover {
        background-color: #4f46e5;
    }
    
    /* Minimal spacing tweaks */
    .main .block-container {
        padding-top: 2rem;
        max-width: 900px;
    }
    
    /* Empty state card */
    .empty-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 24px;
        margin: 32px 0;
    }
</style>
""", unsafe_allow_html=True)

# Available Groq models
GROQ_MODELS = {
    "Llama 3.3 70B": "groq/llama-3.3-70b-versatile",
    "Llama 3.1 8B": "groq/llama-3.1-8b-instant",
    "Mixtral 8x7B": "groq/mixtral-8x7b-32768",
    "Gemma 2 9B": "groq/gemma2-9b-it"
}

# Default model - professional approach
DEFAULT_MODEL = "groq/llama-3.3-70b-versatile"

# ===========================
#   Load LLM
# ===========================
def load_llm(api_key, model_name):
    """Load Groq LLM with user-provided API key"""
    try:
        llm = LLM(model=model_name, api_key=api_key)
        return llm
    except Exception as e:
        return None

# ===========================
#   Define Agents & Tasks
# ===========================
def create_agents_and_tasks(pdf_tool, llm, web_tool=None):
    """Creates a Crew with appropriate tools. AUTO mode - uses whatever tools are available."""
    
    # Build tools list based on what's available
    tools = []
    if pdf_tool:
        tools.append(pdf_tool)
    if web_tool:
        tools.append(web_tool)
    
    # Set goal based on available tools
    if pdf_tool and web_tool:
        retriever_goal = """Find relevant information from the PDF first. Only search the internet if the PDF doesn't contain the answer for: {query}. 
        
        IMPORTANT RULES:
        - If the user explicitly asks about the PDF or document, ignore previous conversation topics and focus ONLY on the PDF
        - If the requested information is not present in the PDF, clearly state that it is not available instead of guessing
        - Start your response with either 'SOURCE: PDF' or 'SOURCE: Internet' on the first line to indicate which source was used"""
    elif pdf_tool:
        retriever_goal = """Find relevant information ONLY from the uploaded PDF for: {query}. 
        
        IMPORTANT RULES:
        - If the user explicitly asks about the PDF or document, ignore previous conversation topics and focus ONLY on the PDF
        - If information is not in the PDF, clearly state 'Information not found in PDF' - do NOT guess or make up information
        - Start your response with 'SOURCE: PDF' on the first line"""
    elif web_tool:
        retriever_goal = """Search the internet for information about: {query}. 
        IMPORTANT: Start your response with 'SOURCE: Internet' on the first line."""
    else:
        retriever_goal = "Find relevant information for: {query}"
    
    retriever_agent = Agent(
        role="Information retriever",
        goal=retriever_goal,
        backstory="You are thorough and honest. You clearly state when information is not available. You ALWAYS start your response with 'SOURCE: [PDF/Internet]' to indicate the source used.",
        verbose=VERBOSE,
        tools=tools,
        llm=llm
    )

    response_synthesizer_agent = Agent(
        role="Response synthesizer",
        goal="""Create a clear, well-structured answer for the user.

        FORMATTING RULES:
        - Do NOT respond in a single paragraph unless the answer is extremely short
        - Use headings and bullet points when summarizing documents
        - For PDFs, present information as sections or bullet points
        - For general knowledge questions, start with 1 short intro sentence, then list key points in bullets
        
        CONTENT RULES:
        - Avoid repetition
        - Keep the answer concise and readable
        - Do NOT mention sources inside the body text
        - If sources disagree, explicitly mention the disagreement
        - Preserve the SOURCE line from the retriever
        
        BANNED PHRASES (never use):
        - "The provided PDF..."
        - "Based on the retrieved information..."
        - "It does not mention..."
        - "According to the document..."
        - "The resume states..."
        """,
        backstory="""You are a helpful assistant who provides clear, well-formatted answers. 
        You use headings and bullet points to make information easy to scan. 
        You never mention where information came from in your answer text. 
        You write naturally and structure information logically.
        You highlight disagreements between sources when they exist.""",
        verbose=VERBOSE,
        llm=llm
    )

    retrieval_task = Task(
        description="Retrieve relevant information for: {query}",
        expected_output="Information with SOURCE: [PDF/Internet] prefix indicating which source was used",
        agent=retriever_agent
    )

    response_task = Task(
        description="Synthesize answer for: {query} using ONLY the retrieved information",
        expected_output="""Final answer format:
        - SOURCE: [PDF/Internet] on first line
        - Well-structured answer with headings and bullet points (for document summaries)
        - OR short intro + bullet points (for knowledge questions)
        - No meta explanations
        - No source mentions inside the text
        - Natural, readable formatting""",
        agent=response_synthesizer_agent
    )

    crew = Crew(
        agents=[retriever_agent, response_synthesizer_agent],
        tasks=[retrieval_task, response_task],
        process=Process.sequential,
        verbose=VERBOSE
    )
    return crew

# ===========================
#   Session State
# ===========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_tool" not in st.session_state:
    st.session_state.pdf_tool = None

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

if "pdf_file_path" not in st.session_state:
    st.session_state.pdf_file_path = None  # Actual file path for cleanup

if "crew" not in st.session_state:
    st.session_state.crew = None

if "last_model" not in st.session_state:
    st.session_state.last_model = None

def reset_chat():
    st.session_state.messages = []
    st.session_state.crew = None
    # Clean up temp PDF file
    if st.session_state.pdf_file_path:
        try:
            if os.path.exists(st.session_state.pdf_file_path):
                os.remove(st.session_state.pdf_file_path)
        except:
            pass  # Ignore cleanup errors
    gc.collect()

# ===========================
#   Sidebar - Clean & Minimal
# ===========================
selected_model = DEFAULT_MODEL  # Initialize with default

with st.sidebar:
    st.markdown("<h2 style='text-align:center; margin-bottom:20px'>Configuration</h2>", unsafe_allow_html=True)

    # API key help expander
    with st.expander("🔑 API key help"):
        st.markdown(
            """
            **Groq** – required  
            https://console.groq.com  

            **Serper** – optional (internet search)  
            https://serper.dev
            """
        )

    st.markdown("---")

    # Access
    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Get a free key from console.groq.com"
    )
    
    if groq_api_key:
        st.caption("🟢 Groq API connected")
    else:
        st.caption("🔴 Required")

    serper_key = None
    if SERPER_AVAILABLE:
        serper_key = st.text_input(
            "Serper API Key (optional)",
            type="password",
            help="Get a free key from serper.dev - enables internet search"
        )
        if serper_key:
            os.environ["SERPER_API_KEY"] = serper_key
            st.caption("🟢 Internet search enabled")
        else:
            st.caption("⚪ Internet search disabled")

    st.markdown("---")

    # Data
    st.markdown("#### Data")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")

    if uploaded_file is not None:
        # Use hash-based comparison for file identity
        current_hash = file_hash(uploaded_file)
        
        # Check if this is a new/different PDF
        if st.session_state.pdf_path != current_hash:
            # Clean up old PDF file
            if st.session_state.pdf_file_path:
                try:
                    if os.path.exists(st.session_state.pdf_file_path):
                        os.remove(st.session_state.pdf_file_path)
                except:
                    pass  # Ignore cleanup errors
            
            # New PDF - reset everything
            st.session_state.messages = []
            st.session_state.crew = None
            st.session_state.last_model = None
            st.session_state.pdf_tool = None
            st.session_state.pdf_path = None
            st.session_state.pdf_file_path = None
        
        # Index PDF if not already done
        if st.session_state.pdf_path is None:
            # Create persistent temp directory
            temp_dir = tempfile.mkdtemp()
            temp_file_path = os.path.join(temp_dir, uploaded_file.name)

            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            with st.spinner("Indexing PDF..."):
                st.session_state.pdf_tool = DocumentSearchTool(file_path=temp_file_path)
                st.session_state.pdf_path = current_hash
                st.session_state.pdf_file_path = temp_file_path  # Track for cleanup
        
        st.caption("🟢 PDF indexed and ready")
    else:
        st.caption("⚪ No PDF uploaded")

    st.markdown("---")
    
    # Advanced settings
    with st.expander("⚙️ Advanced"):
        selected_model_display = st.selectbox(
            "Model",
            options=list(GROQ_MODELS.keys()),
            index=0
        )
        selected_model = GROQ_MODELS[selected_model_display]
    
    # Default model if not changed in Advanced
    if "selected_model" not in st.session_state:
        selected_model = DEFAULT_MODEL

    st.markdown("---")
    st.markdown("#### Actions")
    
    if st.button("Reset session"):
        reset_chat()

# ===========================
#   Main Interface
# ===========================
# Header with centered text
st.markdown(
    """
    <div style='text-align:center'>
        <h1 style='margin-bottom:0'>Seekra</h1>
        <p style='margin-top:6px; font-size:12px; opacity:0.6;'>Powered by Groq • Serper</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Check readiness based on available tools
api_ready = bool(groq_api_key)
pdf_ready = st.session_state.pdf_tool is not None
internet_ready = SERPER_AVAILABLE and os.getenv("SERPER_API_KEY")

# Ready if API key is present (PDF and Internet are optional)
is_ready = api_ready

# ===== Mode indicator (compact, near title) =====
if pdf_ready and internet_ready:
    st.caption("🟢 PDF + Internet")
elif pdf_ready:
    st.caption("🟢 PDF only")
elif internet_ready:
    st.caption("🟢 Internet only")
elif api_ready:
    st.caption("🟢 Ready (General knowledge)")
else:
    st.caption("🔴 Add API key to start")

# ===== Empty State Card (styled) =====
if not is_ready:
    st.markdown("""
    <div class="empty-card">
        <h3 style="margin-top:0">Get started</h3>
        <ol>
            <li>Add your <b>Groq API key</b></li>
            <li>Upload a PDF <i>(optional)</i></li>
            <li>Ask a question</li>
        </ol>
        <p style="opacity:0.8; margin-bottom:0">You can search the internet even without a PDF.</p>
    </div>
    """, unsafe_allow_html=True)

# Always show chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Show source if available
        if message["role"] == "assistant" and "source" in message:
            st.caption(f"Source: {message['source']}")

prompt = st.chat_input(
    "Ask about your PDF or anything from the web…",
    disabled=not is_ready
)

if prompt and is_ready:
    # Intent detection - check if user is asking specifically about PDF (conservative)
    pdf_keywords = ["pdf", "document", "resume", "cv", "this file", "this pdf"]
    is_pdf_intent = any(word in prompt.lower() for word in pdf_keywords)
    
    # Build conversation history BEFORE appending new message
    history = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in st.session_state.messages[-6:]
    )
    
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Load LLM
    llm = load_llm(groq_api_key, selected_model)
    
    if llm is None:
        with st.chat_message("assistant"):
            st.error("Failed to load LLM. Check your API key.")
        st.stop()

    # Prepare web tool if available
    web_tool = None
    if SERPER_AVAILABLE and os.getenv("SERPER_API_KEY"):
        web_tool = SerperDevTool()

    # Build or rebuild crew if needed (when model changes or tools change)
    crew_needs_rebuild = (
        st.session_state.crew is None
        or st.session_state.last_model != selected_model
    )
    
    if crew_needs_rebuild:
        st.session_state.crew = create_agents_and_tasks(
            st.session_state.pdf_tool, 
            llm,
            web_tool
        )
        st.session_state.last_model = selected_model

    # Get response with intent-aware history
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                # Intent-aware query construction
                if is_pdf_intent:
                    # PDF-specific query - ignore history, focus on PDF
                    query_input = prompt
                else:
                    # General query - use history for context
                    query_input = f"{history}\n\nUser question: {prompt}" if history else prompt
                
                inputs = {"query": query_input}
                
                result = st.session_state.crew.kickoff(inputs=inputs).raw
                
                # Soft guard: ensure structured output for multi-line answers
                if result.count("\n") < 2 and len(result) > 100:
                    # LLM gave paragraph instead of structured format
                    result = "**Summary**\n\n" + result
                
                # Parse actual source from response (check anywhere in text)
                if "SOURCE: PDF" in result:
                    source_used = "PDF"
                    # Remove SOURCE line from display
                    result = result.replace("SOURCE: PDF\n", "").replace("SOURCE: PDF", "").strip()
                elif "SOURCE: Internet" in result:
                    source_used = "Internet"
                    # Remove SOURCE line from display
                    result = result.replace("SOURCE: Internet\n", "").replace("SOURCE: Internet", "").strip()
                else:
                    # Fallback if format not followed - infer from available tools
                    if pdf_ready and not internet_ready:
                        source_used = "PDF"
                    elif internet_ready and not pdf_ready:
                        source_used = "Internet"
                    else:
                        source_used = "Unknown"
                
            except Exception as e:
                # Log error for debugging
                if VERBOSE:
                    st.error(f"Debug: {str(e)}")
                result = "Something went wrong while processing your question. Please try again."
                source_used = "Error"
        
        st.markdown(result)
        
        # Add source citation
        st.caption(f"Source: {source_used}")

    # Save response with source
    st.session_state.messages.append({
        "role": "assistant",
        "content": result,
        "source": source_used
    })
