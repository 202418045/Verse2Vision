# 🚀 GitHub Upload Guide for Verse2Vision

## Step-by-Step Instructions

### Prerequisites
- GitHub account (if you don't have one, create at: https://github.com)
- Git installed on your computer (check with: `git --version`)

---

## Method 1: Using Command Line (Recommended)

### Step 1: Initialize Git Repository

Open terminal/PowerShell in your project folder and run:

```bash
git init
```

### Step 2: Add All Files

```bash
git add .
```

### Step 3: Make Your First Commit

```bash
git commit -m "Initial commit: Verse2Vision - Bidirectional Multimodal RAG System"
```

### Step 4: Create Repository on GitHub

1. Go to https://github.com and log in
2. Click the **"+"** icon in top right → **"New repository"**
3. Fill in:
   - **Repository name**: `Verse2Vision` (or your preferred name)
   - **Description**: "Bidirectional Multimodal RAG System for Cultural Preservation - Transforming epic text into visual storytelling"
   - **Visibility**: Choose Public or Private
   - **DO NOT** check "Initialize with README" (we already have one)
4. Click **"Create repository"**

### Step 5: Link Local Repository to GitHub

GitHub will show you commands. Use these (replace `YOUR_USERNAME` with your GitHub username):

```bash
git remote add origin https://github.com/YOUR_USERNAME/Verse2Vision.git
git branch -M main
git push -u origin main
```

If prompted for credentials:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (not your GitHub password)
  - Create token: https://github.com/settings/tokens
  - Click "Generate new token (classic)"
  - Select scopes: `repo` (full control)
  - Copy the token and use it as password

---

## Method 2: Using GitHub Desktop (Easier)

1. Download GitHub Desktop: https://desktop.github.com
2. Install and sign in with your GitHub account
3. Click **"File" → "Add Local Repository"**
4. Browse to your project folder: `C:\Users\Paarth\OneDrive\Desktop\chalisa`
5. Click **"Publish repository"**
6. Fill in repository details and click **"Publish"**

---

## Method 3: Using VS Code/Cursor

1. Open your project in VS Code/Cursor
2. Click the **Source Control** icon (left sidebar) or press `Ctrl+Shift+G`
3. Click **"Initialize Repository"**
4. Stage all files (click **"+"** next to "Changes")
5. Write commit message: "Initial commit: Verse2Vision"
6. Click **"✓ Commit"**
7. Click **"..."** → **"Publish Branch"**
8. Follow prompts to create GitHub repository

---

## What Files Will Be Uploaded?

✅ **Will be uploaded:**
- All Python files (`*.py`)
- `requirements.txt`
- `README.md`
- `PROJECT_DOCUMENTATION.md`
- `kb.json` (if you want to share it)
- `.gitignore`

❌ **Will NOT be uploaded** (protected by `.gitignore`):
- `api_key.txt` (your API keys)
- `hf_token.txt` (your tokens)
- `__pycache__/` (Python cache)
- `.env` files

---

## After First Upload: Regular Updates

When you make changes:

```bash
# See what changed
git status

# Add changed files
git add .

# Commit with message
git commit -m "Description of your changes"

# Push to GitHub
git push
```

---

## Quick Command Reference

```bash
# Check status
git status

# Add specific file
git add filename.py

# Add all changes
git add .

# Commit
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes
git pull

# View commit history
git log
```

---

## Troubleshooting

### Issue: "Permission denied"
- **Solution**: Use Personal Access Token instead of password

### Issue: "Repository not found"
- **Solution**: Check repository name matches exactly (case-sensitive)

### Issue: "Large file upload"
- **Solution**: If `kb.json` is very large, consider using Git LFS or excluding it

### Issue: "Authentication failed"
- **Solution**: 
  1. Generate new Personal Access Token
  2. Use token as password
  3. Or use SSH keys instead

---

## Next Steps After Upload

1. ✅ Add repository description on GitHub
2. ✅ Add topics/tags: `rag`, `multimodal`, `cultural-preservation`, `hanuman-chalisa`, `streamlit`, `gemini`
3. ✅ Create a LICENSE file (if you want to open source)
4. ✅ Add screenshots to README
5. ✅ Enable GitHub Pages (if you want website)

---

## Security Checklist

Before pushing, make sure:
- ✅ API keys are in `.gitignore`
- ✅ No secrets in code
- ✅ No passwords in files
- ✅ Sensitive data excluded

---

Good luck! 🎉

