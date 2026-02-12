# Streamlit Cloud Deployment Guide

## 🚀 Deploy Your Offline PDF Q&A App

This guide will help you deploy `app_offline.py` to Streamlit Cloud for **FREE**.

---

## ✅ What Makes This App Perfect for Deployment:

- ✅ **No API keys needed** - Completely self-contained
- ✅ **100% Offline logic** - Only needs PDF upload
- ✅ **Lightweight** - Uses semantic search, not heavy LLMs
- ✅ **Fast** - No external API calls
- ✅ **FREE** - Streamlit Cloud free tier is enough

---

## 📋 Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Create a GitHub account** (if you don't have one)
   - Go to: https://github.com
   - Sign up for free

2. **Create a new repository**
   - Click "New repository"
   - Name: `agentic-rag-pdf-qa`
   - Make it **Public**
   - Click "Create repository"

### Step 2: Upload Your Code to GitHub

**Option A: Using GitHub Web Interface (Easy)**

1. Go to your repository
2. Click "Add file" → "Upload files"
3. Upload these files:
   ```
   app_offline.py
   requirements.txt
   README.md
   src/agentic_rag/tools/custom_tool.py
   knowledge/dspy.pdf (optional - for demo)
   ```

**Option B: Using Git Command Line**

```bash
# In your project folder
git init
git add app_offline.py requirements.txt README.md src/
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/agentic-rag-pdf-qa.git
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub

2. **Create New App**
   - Click "New app"
   - Select your repository: `agentic-rag-pdf-qa`
   - Main file path: `app_offline.py`
   - Click "Deploy!"

3. **Wait for Deployment**
   - Takes 2-5 minutes
   - You'll get a URL like: `https://your-app.streamlit.app`

---

## 🎯 Your App is Now Live!

Share your URL with anyone - they can:
- ✅ Upload PDFs
- ✅ Ask questions
- ✅ Get instant answers
- ✅ No signup needed
- ✅ Completely free

---

## 📦 Required Files

Make sure these files are in your repository:

### 1. `requirements.txt`
```
streamlit>=1.31.0
markitdown>=0.0.1a2
chonkie[semantic]>=0.2.0
qdrant-client>=1.7.0
fastembed>=0.2.0
```

### 2. `app_offline.py`
(Already created - the main app file)

### 3. `README.md`
```markdown
# Offline PDF Q&A App

Upload a PDF and ask questions - completely offline and free!

## Features
- 🔒 100% Privacy - Your data never leaves the server
- ⚡ Fast semantic search
- 💰 Completely free
- 🚀 No API keys needed

## Try it Live
[Your Streamlit Cloud URL here]

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app_offline.py
```
```

---

## 🔧 Troubleshooting

### Issue: "Module not found"
**Solution:** Make sure `requirements.txt` has all dependencies

### Issue: "App crashes on PDF upload"
**Solution:** Check file size - Streamlit Cloud has 200MB limit per file

### Issue: "Slow performance"
**Solution:** Normal for first run - subsequent searches are fast

---

## 💡 Tips for Better Performance

1. **Keep PDFs under 50MB** for faster indexing
2. **Use clear questions** for better search results
3. **Share your app URL** - unlimited users can access it!

---

## 🎉 You're Done!

Your app is now:
- ✅ Live on the internet
- ✅ Accessible to anyone
- ✅ Completely free
- ✅ No maintenance needed

**Share your app and help others search their PDFs!** 🚀
