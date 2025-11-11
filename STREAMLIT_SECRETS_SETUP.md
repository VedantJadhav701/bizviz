# 🔑 STREAMLIT SECRETS CONFIGURATION

## Setting Up Your Groq API Key

### For Streamlit Cloud Deployment:

1. **Go to your Streamlit Cloud dashboard:**
   - Visit: https://share.streamlit.io
   - Click on your app: `bizviz`

2. **Open App Settings:**
   - Click the **"⋮"** menu (three dots)
   - Select **"Settings"**

3. **Add Secrets:**
   - Click on **"Secrets"** tab
   - Paste this exactly:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

4. **Click "Save"**

5. **Your app will automatically restart** with the new secret!

---

## For Local Development:

### Create `.streamlit/secrets.toml` file:

File already exists at: `.streamlit/secrets.toml`

Add this content:

```toml
# Groq API Configuration
GROQ_API_KEY = "your_groq_api_key_here"
```

**Note:** This file is in `.gitignore` so it won't be uploaded to GitHub! ✅

---

## How to Use in Your Code:

### In your Python files:

```python
import streamlit as st

# Access the API key
api_key = st.secrets["GROQ_API_KEY"]

# Use it with Groq
from groq import Groq
client = Groq(api_key=api_key)
```

---

## ✅ Verification Steps:

After adding the secret:

1. **In Streamlit Cloud:**
   - Wait for app to restart
   - Check logs for any errors
   - Test the functionality that uses Groq API

2. **Locally:**
   ```powershell
   streamlit run app_enhanced.py
   ```
   - Should work without errors

---

## 🔒 Security Best Practices:

✅ **DO:**
- Use Streamlit secrets for API keys
- Keep `.streamlit/secrets.toml` in `.gitignore`
- Use different keys for dev/prod if needed

❌ **DON'T:**
- Commit API keys to GitHub
- Share secrets publicly
- Hardcode keys in your code

---

## 📝 Quick Reference:

### Streamlit Cloud Secrets Format:
```toml
# Single key
GROQ_API_KEY = "your-key-here"

# Multiple keys
GROQ_API_KEY = "key1"
OPENAI_API_KEY = "key2"

# Nested sections
[database]
host = "localhost"
port = 5432
```

### Access in Code:
```python
# Simple key
key = st.secrets["GROQ_API_KEY"]

# Nested key
host = st.secrets["database"]["host"]

# Check if key exists
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
```

---

## 🚀 Your Groq API Key is Set!

**For Streamlit Cloud:** Add it in the app settings
**For Local:** Already in `.streamlit/secrets.toml`

Your app will now be able to use the Groq API! 🎉
