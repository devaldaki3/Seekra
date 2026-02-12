# 🤖 Agentic RAG - PDF Q&A

AI-Powered PDF Question Answering System using CrewAI and Groq

Upload any PDF and ask questions - get complete, AI-generated answers powered by advanced language models!

## 🌟 Features

- 📄 **PDF Upload & Search** - Upload any PDF document and ask questions
- 🤖 **AI-Powered Answers** - Complete, coherent responses using state-of-the-art LLMs
- 🎯 **Smart Search** - Searches PDF first, then web if needed (optional)
- 🔑 **User-Provided API Keys** - Secure, no hardcoded secrets
- 🎨 **Model Selection** - Choose from multiple Groq models
- 💰 **100% FREE** - Uses FREE Groq API (no OpenAI costs!)
- 🚀 **Fast & Reliable** - Powered by Groq's lightning-fast inference
- 🔒 **Privacy-Focused** - Your API keys and documents are never stored

## 🎯 Live Demo

[Deploy your own!](https://share.streamlit.io)

## 🚀 Quick Start

### 1. Get FREE API Key

Get your FREE Groq API key (no credit card required):
- Go to: [console.groq.com](https://console.groq.com)
- Sign up for FREE
- Get your API key

### 2. Run Locally

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/agentic-rag-pdf-qa.git
cd agentic-rag-pdf-qa

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_final.py
```

### 3. Use the App

1. **Enter your Groq API key** in the sidebar
2. **Select a model** (Llama 3.3 70B recommended)
3. **Upload a PDF** document
4. **Ask questions** and get AI-powered answers!

## 📦 Installation

### Requirements

- Python 3.10 or higher
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Dependencies Include:

- `streamlit` - Web interface
- `crewai` - AI agent framework
- `markitdown` - PDF text extraction
- `chonkie` - Semantic chunking
- `qdrant-client` - Vector database
- `fastembed` - Fast embeddings
- `python-dotenv` - Environment variables

## 🌐 Deploy to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app_final.py` as the main file
   - Deploy!

3. **No Secrets Needed!**
   - Users will enter their own API keys in the UI
   - No need to configure secrets in Streamlit Cloud

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Groq API (Llama 3.3 70B, Mixtral, Gemma)
- **PDF Processing**: MarkItDown
- **Vector Search**: Qdrant + Chonkie
- **AI Agents**: CrewAI
- **Web Search**: FireCrawl (optional)

## 📖 How It Works

1. **PDF Upload**: User uploads a PDF document
2. **Indexing**: PDF is converted to text and chunked semantically
3. **Vector Storage**: Chunks are stored in Qdrant vector database
4. **Question**: User asks a question
5. **Retrieval**: AI agent searches PDF for relevant information
6. **Synthesis**: AI synthesizes a complete answer from retrieved chunks
7. **Response**: User gets a coherent, AI-generated answer

## 🎨 Available Models

- **Llama 3.3 70B** (Recommended) - Best quality, comprehensive answers
- **Llama 3.1 8B** - Faster responses, good quality
- **Mixtral 8x7B** - Excellent reasoning capabilities
- **Gemma 2 9B** - Balanced performance

## 💡 Why This App?

✅ **No OpenAI costs** - Uses FREE Groq API  
✅ **Complete answers** - Not just chunks, full AI synthesis  
✅ **Privacy-focused** - API keys never stored  
✅ **Fast** - Groq's inference is lightning fast  
✅ **Easy to deploy** - One-click Streamlit Cloud deployment  
✅ **User-controlled** - Users provide their own API keys  
✅ **Model choice** - Select the best model for your needs  

## 🔒 Privacy & Security

- ✅ API keys are **never stored** - only used during your session
- ✅ PDFs are processed **locally** in temporary storage
- ✅ No data is sent to external servers except Groq API
- ✅ Session data is cleared when you close the browser

## 📝 Project Structure

```
agentic-rag-pdf-qa/
├── app_final.py              # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── DEPLOYMENT_GUIDE.md       # Detailed deployment instructions
├── .gitignore               # Git ignore rules
├── knowledge/               # Sample PDF files
│   └── dspy.pdf            # Example document
└── src/
    └── agentic_rag/
        └── tools/
            └── custom_tool.py  # Custom search tools
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Acknowledgments

- **CrewAI** - AI agent framework
- **Groq** - FREE, fast LLM inference
- **Streamlit** - Amazing web framework
- **Qdrant** - Vector database
- **Chonkie** - Semantic chunking

## ⭐ Star this repo if you find it useful!

---

**Built with ❤️ for the AI community**
