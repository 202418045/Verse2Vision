"""Test script to check Hugging Face API connection using huggingface_hub."""
import os

# Try to load token from file
hf_token_file = "hf_token.txt"
hf_token = None

if os.path.exists(hf_token_file):
    try:
        with open(hf_token_file, 'r') as f:
            token = f.read().strip()
            if token and token != "PASTE_YOUR_HUGGING_FACE_TOKEN_HERE" and len(token) > 10:
                hf_token = token
                print("✅ Using token from hf_token.txt")
    except Exception as e:
        print(f"⚠️  Could not read hf_token.txt: {e}")

if not hf_token:
    print("❌ No Hugging Face token found.")
    print("Please add your token to hf_token.txt")
    exit(1)

print(f"✅ Token found (starts with: {hf_token[:10]}...)\n")

# Check if huggingface_hub is installed
try:
    from huggingface_hub import InferenceClient
    print("✅ huggingface_hub library is installed\n")
except ImportError:
    print("❌ huggingface_hub library not found.")
    print("Install with: pip install huggingface_hub")
    exit(1)

# Test with a simple prompt
test_prompt = "a beautiful sunset over mountains"
print(f"🧪 Testing with prompt: '{test_prompt}'\n")

try:
    client = InferenceClient(token=hf_token)
    
    # Try different models
    models = [
        "stabilityai/sdxl-turbo",
        "stabilityai/stable-diffusion-xl-base-1.0",
        "runwayml/stable-diffusion-v1-5",
    ]
    
    success = False
    for model in models:
        try:
            print(f"📡 Testing model: {model}")
            image = client.text_to_image(
                test_prompt,
                model=model,
                num_inference_steps=20
            )
            
            # text_to_image returns PIL Image directly
            if hasattr(image, 'size'):
                print(f"✅ SUCCESS! Generated image")
                print(f"   Image size: {image.size}")
                success = True
                break
            else:
                print(f"   ⚠️  Unexpected response type: {type(image)}")
                continue
            
        except Exception as e:
            error_str = str(e).lower()
            if 'not found' in error_str or '404' in error_str:
                print(f"   ❌ Model not found")
            elif 'loading' in error_str or '503' in error_str:
                print(f"   ⏳ Model loading...")
            else:
                print(f"   ❌ Error: {e}")
            continue
    
    if success:
        print("\n✅ Hugging Face API is working!")
    else:
        print("\n❌ All models failed.")
        print("\nPossible solutions:")
        print("1. Wait a few minutes and try again (models may be loading)")
        print("2. Check your token is valid at https://huggingface.co/settings/tokens")
        print("3. Try using 'Text Prompt Only' method in the app")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
