"""Test script to check Gemini API key and list available models."""
import os
import sys
import google.generativeai as genai

# Try to get API key from multiple sources
api_key = None

# 1. Check api_key.txt file (easiest method)
api_key_file = "api_key.txt"
if os.path.exists(api_key_file):
    try:
        with open(api_key_file, 'r') as f:
            api_key = f.read().strip()
            # Remove placeholder text
            if api_key and api_key != "PASTE_YOUR_GEMINI_API_KEY_HERE" and len(api_key) > 10:
                print("✅ Using API key from api_key.txt file")
            else:
                api_key = None
    except Exception as e:
        print(f"⚠️  Could not read api_key.txt: {e}")

# 2. Check command line argument
if not api_key and len(sys.argv) > 1:
    api_key = sys.argv[1]
    print("✅ Using API key from command line argument")

# 3. Check environment variable
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("✅ Using API key from environment variable")

# 4. If still not found, show instructions
if not api_key:
    print("❌ GEMINI_API_KEY not found.")
    print("\n📝 EASIEST METHOD:")
    print(f"   1. Open the file: {api_key_file}")
    print("   2. Replace 'PASTE_YOUR_GEMINI_API_KEY_HERE' with your actual API key")
    print("   3. Save the file and run this script again")
    print("\nAlternative methods:")
    print("   - Command line: python test_gemini_api.py YOUR_API_KEY")
    print("   - Environment: $env:GEMINI_API_KEY='YOUR_API_KEY' (PowerShell)")
    exit(1)

print(f"✅ API Key found (starts with: {api_key[:10]}...)")
print("\nConfiguring Gemini API...")
genai.configure(api_key=api_key)

print("\n📋 Listing available models with 'generateContent' support:\n")
available_models = []
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            model_name = model.name.replace('models/', '')
            available_models.append(model_name)
            print(f"  ✅ {model_name}")
            print(f"     Full name: {model.name}")
            print(f"     Methods: {', '.join(model.supported_generation_methods)}")
            print()
    
    if not available_models:
        print("  ⚠️  No models found with generateContent support")
    else:
        print(f"\n✅ Found {len(available_models)} available model(s)")
        print(f"\nRecommended model to use: {available_models[0]}")
        
        # Test with the first available model
        print(f"\n🧪 Testing with model: {available_models[0]}")
        try:
            model = genai.GenerativeModel(available_models[0])
            response = model.generate_content("Say 'Hello' in one word.")
            print(f"✅ Test successful! Response: {response.text}")
        except Exception as e:
            print(f"❌ Test failed: {e}")
            
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print("\nPossible issues:")
    print("1. API key is invalid or expired")
    print("2. API key doesn't have required permissions")
    print("3. Billing not enabled (required for some regions)")
    print("4. Check API key at: https://makersuite.google.com/app/apikey")

