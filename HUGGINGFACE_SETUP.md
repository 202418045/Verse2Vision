# How to Get Your Hugging Face Token

## Quick Steps:

1. **Go to Hugging Face**: https://huggingface.co
2. **Sign up or Log in** (it's free!)
3. **Go to Settings**: Click your profile → Settings
4. **Create Access Token**: 
   - Go to: https://huggingface.co/settings/tokens
   - Click "New token"
   - Name it (e.g., "chalisa-app")
   - Select "Read" permission (that's enough)
   - Click "Generate token"
5. **Copy the token** (starts with `hf_...`)

## Where to Put Your Token:

### Option 1: In the Streamlit App (Easiest)
- Just paste it in the "Hugging Face Token" field in the sidebar when using the app
- It will be saved for your session

### Option 2: In a File (Persistent)
1. Open the file `hf_token.txt` in this folder
2. Replace `PASTE_YOUR_HUGGING_FACE_TOKEN_HERE` with your actual token
3. Save the file
4. The app will automatically use it

## Benefits of Using a Token:

- ✅ **Faster inference** - No waiting in queue
- ✅ **No rate limits** - Generate more images
- ✅ **More reliable** - Better uptime
- ✅ **Free** - No cost, just need an account

## Note:

The token is already added to `.gitignore`, so it won't be committed to git if you use version control.

