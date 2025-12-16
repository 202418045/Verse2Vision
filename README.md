# 🕉️ Verse2Vision: Bidirectional Multimodal RAG System

A **Bidirectional Multimodal Retrieval-Augmented Generation (RAG)** system that transforms epic text into visual storytelling and interprets mythological images into authenticated narratives using a shared knowledge base grounded in Indian epics.

## 📚 Complete Documentation

For detailed technical documentation, architecture, workflow, and cultural preservation philosophy, see:
- **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** - Complete project documentation with all details

## 🎯 Project Overview

This system works in **two directions**:

### 1. **Text → Image Generation (with RAG)**
- User provides text input (shloka, verse, or question)
- System retrieves relevant passages from vector-based knowledge base
- LLM converts retrieved knowledge into:
  - A coherent story or explanation
  - A detailed visual scene description
- Description is used to generate artwork (via image generation models or prompts)

### 2. **Image → Text Generation (with RAG)**
- User uploads an image depicting a mythological/epic scene
- Vision-language model analyzes the image and generates a textual description
- This caption becomes the query for the RAG pipeline
- System retrieves matching epic context and produces:
  - Identification of characters and scenes
  - Detailed story or explanation grounded in authentic sources

## ✨ Key Features

- **Bidirectional Generation**: Supports both text-to-image and image-to-text workflows
- **Context Grounding**: All outputs are anchored to retrieved knowledge rather than free hallucination
- **No Custom Training**: Uses existing LLM and vision/image models with RAG pipeline
- **Expandable**: New datasets or art styles can be added without rebuilding the core system

## 📁 Project Structure

```
chalisa/
├── app_streamlit.py          # Streamlit frontend (bidirectional UI)
├── rag/
│   ├── __init__.py
│   ├── loader.py             # Load kb.json
│   ├── embeddings.py         # Build and store embeddings
│   ├── retriever.py          # Retrieve top relevant verses
│   ├── generator.py          # LLM generation (text, stories, prompts)
│   ├── vision.py             # Image captioning (Image → Text)
│   └── image_generator.py     # Image generation (Text → Image)
├── kb.json                   # Knowledge base (JSON Lines format)
├── requirements.txt
└── README.md
```

## 🚀 Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Optional: For image generation (requires GPU):**
   ```bash
   pip install diffusers accelerate
   ```

3. **Set Gemini API Key:**
   - Enter your API key directly in the Streamlit app sidebar (recommended)
   - Or set it as an environment variable:
     ```bash
     # On Windows (PowerShell)
     $env:GEMINI_API_KEY="your-api-key-here"
     
     # On Linux/Mac
     export GEMINI_API_KEY="your-api-key-here"
     ```

4. **Ensure kb.json is in the project root or in data/kb.json**

## 🏃 Running the App

```bash
streamlit run app_streamlit.py
```

The app will automatically:
- Load the knowledge base from `kb.json`
- Build TF-IDF embeddings for all verses (fast, no model download needed)
- Initialize the Streamlit interface

## 📖 Usage

### 📝 Text → Image Tab
1. Enter text (shloka, verse, or question)
2. System retrieves relevant verses from knowledge base
3. LLM generates enhanced image prompt based on retrieved context
4. Option to generate image (if Stable Diffusion available) or copy prompt for external tools

### 🖼️ Image → Text Tab
1. Upload an image depicting a mythological/epic scene
2. Vision model generates detailed caption
3. Caption is used as RAG query to retrieve matching verses
4. System identifies scene, characters, and provides authenticated narrative

### 💬 Q&A Tab
1. Ask questions about the Hanuman Chalisa
2. Get answers based on retrieved verses
3. View source verses with similarity scores

### 📖 Story Generation Tab
1. Enter a topic to find relevant verses
2. Generate devotional stories based on story seeds
3. View source verses and context

### 📖 Verse Explorer (Sidebar)
- Browse all verses
- View Sanskrit text, transliteration, meanings
- Explore image prompts, story seeds, tags, and emotions

## 🔧 Technical Details

### Core Components

- **Knowledge Base (Vector Database)**: Stores embedded text chunks from epics
- **RAG Engine**: 
  - Converts queries into embeddings
  - Retrieves top-relevant passages
  - Uses LLM to generate grounded, context-aware outputs
- **Vision Module**: Captions uploaded images to convert visual content into text for RAG queries
- **Image Generation Module**: Converts RAG-generated prompts into images (via Hugging Face API or external tools)

### Technology Stack

- **Embeddings**: TF-IDF (Term Frequency-Inverse Document Frequency) - lightweight, fast, no ML models required
- **Vector Search**: Cosine similarity on TF-IDF vectors
- **LLM**: Google Gemini 1.5 Flash/Pro via `google-generativeai`
- **Vision**: Google Gemini Vision API for image captioning
- **Image Generation**: Pollinations AI (free, no API key needed) or external tools via prompts
- **Embedding Fields**: Combines Sanskrit text, transliteration, simple meaning, detailed meaning, and tags

## 📋 Requirements

- Python 3.8+
- Google Gemini API key
- kb.json file with verse data
- (No API key needed for image generation - uses Pollinations AI)

## 🛡️ Error Handling

The app includes error handling for:
- Missing kb.json file
- Missing GEMINI_API_KEY
- API call failures
- Empty search results
- Image processing errors

## 🎨 Image Generation Options

1. **Text Prompt Only** (Default): Copy the generated prompt and use with:
   - DALL·E
   - Midjourney
   - Stable Diffusion (online)
   - Other image generation tools

2. **Pollinations AI** (Default): Free cloud-based image generation:
   - No API key required
   - Fast and reliable
   - Works on any system with internet
   - Generates high-quality 1024x1024 images

## 🔄 Workflow Examples

### Text → Image Flow
```
User Input: "Hanuman carrying the mountain"
    ↓
RAG Retrieval: Finds relevant verses about Hanuman's strength
    ↓
LLM Enhancement: Creates detailed visual scene description
    ↓
Image Generation: Produces artwork (or prompt for external tools)
```

### Image → Text Flow
```
User Upload: Image of Hanuman
    ↓
Vision Model: "A powerful monkey deity carrying a mountain..."
    ↓
RAG Retrieval: Matches to verses about Hanuman's strength
    ↓
LLM Explanation: Identifies scene, provides authenticated narrative
```

## 📚 Learn More

For complete understanding of:
- All models, libraries, and versions used
- Detailed architecture and workflow
- How multimodal RAG works
- Cultural preservation philosophy
- Technical deep dive

**See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)**

## 📝 License

This project is designed for educational and research purposes.
