# 🕉️ Verse2Vision: Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack & Versions](#technology-stack--versions)
3. [What is Multimodal RAG?](#what-is-multimodal-rag)
4. [Complete Architecture](#complete-architecture)
5. [Detailed Workflow](#detailed-workflow)
6. [Cultural Preservation: Why RAG Matters](#cultural-preservation-why-rag-matters)
7. [Technical Deep Dive](#technical-deep-dive)
8. [Data Flow Diagrams](#data-flow-diagrams)

---

## Project Overview

**Verse2Vision** is a **Bidirectional Multimodal Retrieval-Augmented Generation (RAG)** system designed to preserve and transmit authentic Indian epic knowledge (specifically Hanuman Chalisa) to future generations through:

1. **Visual Storytelling**: Converting ancient verses into engaging comic-style images with subtitles
2. **Authentic Narratives**: Grounding all outputs in the original knowledge base (no hallucination)
3. **Multilingual Support**: Supporting multiple Indian languages for broader accessibility
4. **Educational Focus**: Making complex epic stories accessible to children while maintaining cultural authenticity

### Core Philosophy

The system ensures that **every piece of information** comes directly from the original knowledge base (`kb.json`), preventing:
- ❌ Misinformation
- ❌ Cultural misinterpretation
- ❌ Loss of authentic details
- ❌ Modern reinterpretations that deviate from source material

---

## Technology Stack & Versions

### Python Libraries & Versions

| Library | Version | Purpose |
|---------|---------|---------|
| `streamlit` | ≥1.28.0 | Web UI framework for interactive frontend |
| `scikit-learn` | ≥1.3.0 | TF-IDF vectorization and cosine similarity |
| `google-generativeai` | ≥0.3.0 | Google Gemini API client for LLM and vision |
| `numpy` | ≥1.24.0 | Numerical operations for embeddings |
| `Pillow` | ≥9.0.0 | Image processing and manipulation |
| `requests` | ≥2.28.0 | HTTP requests for Pollinations API |
| `gtts` | ≥2.5.0 | Google Text-to-Speech for multilingual narration |

### AI Models Used

#### 1. **Embedding Model: TF-IDF (Term Frequency-Inverse Document Frequency)**
- **Type**: Statistical text vectorization (not a neural network)
- **Library**: `sklearn.feature_extraction.text.TfidfVectorizer`
- **Why TF-IDF?**
  - ✅ No GPU required
  - ✅ Fast and lightweight
  - ✅ No model downloads
  - ✅ Works offline
  - ✅ Perfect for small-to-medium knowledge bases
  - ✅ Interpretable (you can see which words matter)

**How it works:**
- Converts each verse into a numerical vector
- Each dimension represents a word's importance
- Words that appear frequently across all verses get lower weight
- Words unique to specific verses get higher weight
- Creates a "fingerprint" for each verse

#### 2. **Large Language Model (LLM): Google Gemini**
- **Models Used** (in priority order):
  - `gemini-2.5-flash` (primary - fastest)
  - `gemini-2.5-pro` (fallback - more capable)
  - `gemini-2.0-flash` (alternative)
  - `gemini-flash-latest` (latest version)
  - `gemini-pro-latest` (pro version)
- **API**: Google Generative AI API
- **Purpose**: 
  - Generate stories from retrieved verses
  - Create image prompts
  - Answer questions
  - Generate explanations
- **Key Feature**: Context-aware generation based on retrieved verses

#### 3. **Vision Model: Google Gemini Vision**
- **Models Used**:
  - `gemini-2.5-flash` (with vision capability)
  - `gemini-2.5-pro` (with vision capability)
  - `gemini-pro-vision` (legacy)
- **Purpose**: Image captioning (Image → Text conversion)
- **How it works**:
  - Takes uploaded image as input
  - Generates detailed textual description
  - Description becomes query for RAG retrieval

#### 4. **Image Generation: Pollinations AI**
- **Type**: Cloud-based image generation API
- **Model**: Flux (default, can be customized)
- **API Endpoint**: `https://image.pollinations.ai/prompt/`
- **Features**:
  - Free (no API key needed)
  - Fast generation (15-30 seconds)
  - High quality (1024x1024 images)
  - Comic-style illustrations
- **Purpose**: Generate visual stories from text prompts

#### 5. **Text-to-Speech: Google TTS (gTTS)**
- **Type**: Cloud-based TTS service
- **Languages Supported**:
  - English (`en`)
  - Hindi (`hi`)
  - Marathi (`mr`)
  - Bengali (`bn`)
  - Tamil (`ta`)
  - Telugu (`te`)
  - Kannada (`kn`)
  - Malayalam (`ml`)
  - Gujarati (`gu`)
  - Punjabi (`pa`)
  - Urdu (`ur`)
- **Features**:
  - Automatic language detection
  - Multilingual support
  - Free to use
- **Purpose**: Narrate stories, answers, and explanations

---

## What is Multimodal RAG?

### Traditional RAG (Text-only)
```
User Query (Text) 
    ↓
Retrieve Relevant Documents (Text)
    ↓
Generate Answer (Text)
```

### Multimodal RAG (Our System)
```
Input: Text OR Image
    ↓
Process: Convert between modalities
    ↓
Retrieve: Find relevant knowledge base entries
    ↓
Generate: Text, Images, or Audio
```

### Why "Bidirectional"?

Our system works in **two directions**:

#### Direction 1: Text → Image (Epic to Visual)
```
Ancient Verse (Text)
    ↓
RAG Retrieval (Find related verses)
    ↓
LLM Enhancement (Create visual description)
    ↓
Image Generation (Visual story)
```

#### Direction 2: Image → Text (Visual to Epic)
```
Mythological Image
    ↓
Vision Model (Generate caption)
    ↓
RAG Retrieval (Find matching verses)
    ↓
Authentic Narrative (Grounded explanation)
```

### Why "Multimodal"?

The system handles **multiple data types**:
- 📝 **Text**: Verses, questions, stories
- 🖼️ **Images**: Generated artwork, uploaded photos
- 🔊 **Audio**: Narrated stories and explanations
- 🎨 **Visual Stories**: Sequential comic-style images

---

## Complete Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Verse2Vision System                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐         ┌──────────────┐                │
│  │   Frontend    │         │  Knowledge    │                │
│  │  (Streamlit)  │◄────────┤    Base       │                │
│  │               │         │   (kb.json)    │                │
│  └──────┬────────┘         └───────┬───────┘                │
│         │                           │                         │
│         │                           │                         │
│  ┌──────▼───────────────────────────▼───────┐               │
│  │         RAG Pipeline                      │               │
│  │  ┌──────────┐  ┌──────────┐             │               │
│  │  │ Embedding │  │Retriever │             │               │
│  │  │   Store   │─►│          │             │               │
│  │  └──────────┘  └────┬─────┘             │               │
│  └─────────────────────┼───────────────────┘               │
│                         │                                     │
│         ┌───────────────┼───────────────┐                   │
│         │               │               │                     │
│  ┌──────▼──────┐  ┌─────▼─────┐  ┌─────▼─────┐             │
│  │   LLM       │  │  Vision    │  │  Image    │             │
│  │  (Gemini)   │  │  (Gemini)  │  │ Generator │             │
│  └──────┬──────┘  └─────┬─────┘  └─────┬─────┘             │
│         │               │               │                     │
│  ┌──────▼───────────────▼───────────────▼─────┐           │
│  │         Output Generation                     │           │
│  │  • Stories  • Images  • Audio  • Answers    │           │
│  └──────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### Module Breakdown

#### 1. **`rag/loader.py`** - Knowledge Base Loader
- **Purpose**: Parse and load `kb.json` into structured Python objects
- **Input**: JSON file with verse data
- **Output**: List of `KBEntry` objects
- **Key Fields Loaded**:
  - Sanskrit text
  - Transliteration
  - Simple & detailed meanings
  - Story contexts
  - Image prompts
  - Story seeds
  - Tags and emotions

#### 2. **`rag/embeddings.py`** - Embedding Store
- **Purpose**: Convert verses into numerical vectors
- **Method**: TF-IDF Vectorization
- **Process**:
  1. Combine all text fields (Sanskrit, transliteration, meanings, tags)
  2. Create TF-IDF vectorizer
  3. Fit on all verses
  4. Transform each verse into vector
  5. Store vectors in memory
- **Output**: Matrix of vectors (one per verse)

#### 3. **`rag/retriever.py`** - Verse Retriever
- **Purpose**: Find most relevant verses for a query
- **Method**: Cosine Similarity
- **Process**:
  1. Convert query to TF-IDF vector
  2. Calculate cosine similarity with all verse vectors
  3. Rank by similarity score
  4. Return top-k verses
- **Output**: List of (KBEntry, similarity_score) tuples

#### 4. **`rag/generator.py`** - LLM Generator
- **Purpose**: Generate text using Gemini LLM
- **Functions**:
  - `ask_gemini()`: Direct LLM calls
  - `build_qa_prompt()`: Create Q&A prompts
  - `build_story_prompt()`: Create story generation prompts
  - `build_sequential_story_images_prompt()`: Create visual story prompts
  - `parse_sequential_image_descriptions()`: Parse LLM responses
- **Key Feature**: All prompts emphasize using ONLY knowledge base content

#### 5. **`rag/vision.py`** - Image Captioning
- **Purpose**: Convert images to text descriptions
- **Model**: Gemini Vision API
- **Process**:
  1. Receive PIL Image object
  2. Send to Gemini Vision API
  3. Get detailed textual description
  4. Return caption
- **Output**: Text description of image

#### 6. **`rag/image_generator.py`** - Image Generation
- **Purpose**: Generate images from text prompts
- **Service**: Pollinations AI
- **Process**:
  1. Enhance prompt with comic-style instructions
  2. Encode prompt for URL
  3. Send GET request to Pollinations API
  4. Receive image bytes
  5. Convert to PIL Image
- **Output**: PIL Image object (1024x1024)

#### 7. **`rag/tts.py`** - Text-to-Speech
- **Purpose**: Convert text to audio narration
- **Service**: Google TTS (gTTS)
- **Features**:
  - Automatic language detection
  - Multilingual support
  - Returns audio as BytesIO
- **Output**: MP3 audio data

#### 8. **`app_streamlit.py`** - Frontend
- **Purpose**: User interface
- **Framework**: Streamlit
- **Tabs**:
  1. **Create Story**: Generate 3 sequential comic images
  2. **Analyze Image**: Upload image, get explanation
  3. **Ask Question**: Q&A based on verses
  4. **Text Story**: Generate text-only stories
- **Sidebar**: Verse explorer, API key input

---

## Detailed Workflow

### Workflow 1: Creating Visual Stories (Text → Image)

```
Step 1: User Input
    User enters: "Hanuman carrying Sanjeevani mountain"
    ↓
Step 2: RAG Retrieval
    Query → TF-IDF Vector
    ↓
    Cosine Similarity with all verse vectors
    ↓
    Retrieve top-3 most similar verses
    Example matches:
    - Verse 15: About Hanuman's strength
    - Verse 23: About carrying mountain
    - Verse 8: About devotion
    ↓
Step 3: LLM Prompt Building
    System creates prompt:
    "Create 3 comic-style images based on these verses:
     Verse 15: [meaning]
     Verse 23: [meaning]
     Verse 8: [meaning]
     
     Requirements:
     - Comic book style
     - Child-friendly subtitles
     - Visual continuity
     - Cultural authenticity"
    ↓
Step 4: LLM Generation
    Gemini generates:
    IMAGE 1:
    VISUAL: [Detailed scene description]
    SUBTITLE: "Hanuman sees Lakshmana needs help"
    
    IMAGE 2:
    VISUAL: [Detailed scene description]
    SUBTITLE: "Hanuman lifts the entire mountain"
    
    IMAGE 3:
    VISUAL: [Detailed scene description]
    SUBTITLE: "Hanuman brings the mountain to save Lakshmana"
    ↓
Step 5: Image Generation
    For each image:
    - Enhance prompt: "comic book style, vibrant colors..."
    - Send to Pollinations API
    - Receive 1024x1024 image
    ↓
Step 6: TTS Narration
    Combine subtitles: "Scene 1: ... Scene 2: ... Scene 3: ..."
    - Detect language (auto)
    - Generate audio
    ↓
Step 7: Display
    - Show images (600px width)
    - Show subtitles
    - Play audio narration
```

### Workflow 2: Analyzing Images (Image → Text)

```
Step 1: User Upload
    User uploads image of Hanuman
    ↓
Step 2: Vision Analysis
    Image → Gemini Vision API
    ↓
    Caption: "A powerful monkey deity with orange fur, 
             carrying a large mountain on his shoulder, 
             flying through the sky, traditional Indian 
             mythological art style"
    ↓
Step 3: RAG Retrieval
    Caption → TF-IDF Vector
    ↓
    Find verses matching:
    - "monkey deity" → Verse 1, 2, 3
    - "mountain" → Verse 23, 24
    - "flying" → Verse 12, 13
    ↓
    Retrieve top-5 matching verses
    ↓
Step 4: LLM Explanation
    System creates prompt:
    "Based on this image description and these verses,
     identify the scene and provide an authenticated
     explanation grounded in the knowledge base."
    ↓
    Gemini generates:
    "This image depicts Hanuman carrying the Sanjeevani
     mountain, as described in Verse 23 of Hanuman Chalisa.
     According to the epic, when Lakshmana was injured in
     battle, Hanuman was sent to find the healing herb..."
    ↓
Step 5: TTS Narration
    Explanation → Audio (multilingual)
    ↓
Step 6: Display
    - Show uploaded image (500px)
    - Show explanation
    - Play audio narration
```

### Workflow 3: Question Answering

```
Step 1: User Question
    "What does बुद्धिहीन तनु जानिके mean?"
    ↓
Step 2: RAG Retrieval
    Query → TF-IDF Vector
    ↓
    Find verses containing:
    - "बुद्धिहीन" → Verse 2
    - Related concepts → Verse 1, 3
    ↓
    Retrieve top-5 verses
    ↓
Step 3: LLM Answer Generation
    System creates prompt:
    "Answer this question using ONLY the provided verses.
     Do not add information not in the knowledge base.
     
     Question: [user question]
     Verses:
     Verse 2: [full verse details]
     Verse 1: [full verse details]
     ..."
    ↓
    Gemini generates:
    "The phrase 'बुद्धिहीन तनु जानिके' means 'knowing this
     body to be without intelligence.' According to Verse 2
     of Hanuman Chalisa, this refers to the recognition that
     the physical body is limited and requires divine grace..."
    ↓
Step 4: TTS Narration
    Answer → Audio (auto-detect language)
    ↓
Step 5: Display
    - Show answer
    - Show source verses
    - Play audio
```

---

## Cultural Preservation: Why RAG Matters

### The Problem: Information Loss & Misinterpretation

Traditional methods of passing down epic knowledge face challenges:

1. **Oral Tradition Limitations**
   - Details can be forgotten or altered over generations
   - Regional variations may deviate from original
   - No permanent record

2. **Modern Interpretations**
   - Pop culture adaptations may change meanings
   - Commercial interests may simplify or alter stories
   - Loss of authentic context

3. **Language Barriers**
   - Sanskrit is not widely understood
   - Translations may lose nuance
   - Cultural context may be lost

4. **Hallucination in AI**
   - LLMs trained on internet data may generate incorrect information
   - Mixing of different sources
   - No guarantee of authenticity

### The Solution: RAG (Retrieval-Augmented Generation)

RAG solves these problems by:

#### 1. **Grounding in Authentic Sources**
```
Traditional LLM:
User Query → LLM → Answer (may be wrong)

RAG System:
User Query → Retrieve from KB → LLM → Answer (grounded in KB)
```

**Why this matters:**
- ✅ Every answer comes from `kb.json` (authentic source)
- ✅ No hallucination or made-up details
- ✅ Preserves original meanings and contexts
- ✅ Maintains cultural authenticity

#### 2. **Direct Connection to Original Epics**

The knowledge base (`kb.json`) contains:
- Original Sanskrit text
- Authentic translations
- Story contexts from traditional sources
- Image prompts based on traditional art
- Story seeds from original narratives

**RAG ensures:**
- Every generated story uses ONLY this authentic data
- No modern reinterpretations
- No mixing with other sources
- Direct lineage to original epics

#### 3. **Preservation Through Technology**

```
Original Epic (Ancient)
    ↓
Knowledge Base (kb.json) - Digital Preservation
    ↓
RAG System - Authentic Retrieval
    ↓
Generated Content - Grounded in Original
    ↓
Future Generations - Receive Authentic Knowledge
```

**Benefits:**
- ✅ Permanent digital record
- ✅ Accessible to all
- ✅ Cannot be altered (KB is source of truth)
- ✅ Scalable (can add more verses)
- ✅ Multilingual (preserves meaning across languages)

#### 4. **Educational Value**

RAG enables:
- **Visual Learning**: Children see stories through images
- **Authentic Context**: Every image/story is grounded in original
- **Multilingual Access**: Stories in multiple languages
- **Interactive Learning**: Q&A based on authentic verses
- **Cultural Continuity**: Preserves traditions accurately

### Example: Why RAG Prevents Misinformation

**Without RAG (Traditional LLM):**
```
User: "Tell me about Hanuman's birth"

LLM Response (may be wrong):
"Hanuman was born from the union of Anjana and Kesari.
 He was blessed by Lord Shiva and was born with divine
 powers. Some modern interpretations suggest..."
 
❌ Problem: May include incorrect or modern interpretations
```

**With RAG:**
```
User: "Tell me about Hanuman's birth"

System:
1. Retrieves verses from kb.json about Hanuman's birth
2. Finds Verse 5: "Anjana's son, blessed by Vayu..."
3. Finds Verse 8: "Born from Anjana and Kesari..."
4. LLM generates answer using ONLY these verses

Response:
"According to Verse 5 and 8 of Hanuman Chalisa,
 Hanuman was born to Anjana and Kesari, blessed by
 Vayu (wind god). The verses describe him as..."

✅ Solution: Grounded in authentic knowledge base
```

---

## Technical Deep Dive

### 1. TF-IDF Embedding Process

**Term Frequency (TF):**
```
TF(word, verse) = (Number of times word appears in verse) / 
                  (Total words in verse)
```

**Inverse Document Frequency (IDF):**
```
IDF(word) = log(Total number of verses / 
                Number of verses containing word)
```

**TF-IDF Score:**
```
TF-IDF(word, verse) = TF(word, verse) × IDF(word)
```

**Example:**
```
Verse: "Hanuman is the son of Anjana"
Word: "Hanuman"
- Appears 1 time in verse (TF = 1/5 = 0.2)
- Appears in 10 out of 100 verses (IDF = log(100/10) = 1.0)
- TF-IDF = 0.2 × 1.0 = 0.2

Word: "the"
- Appears 1 time (TF = 0.2)
- Appears in 95 out of 100 verses (IDF = log(100/95) = 0.02)
- TF-IDF = 0.2 × 0.02 = 0.004

Result: "Hanuman" gets higher weight (more important)
```

### 2. Cosine Similarity

**Formula:**
```
similarity = (A · B) / (||A|| × ||B||)
```

Where:
- A = Query vector
- B = Verse vector
- · = Dot product
- || || = Vector magnitude

**Why Cosine Similarity?**
- Measures angle between vectors (not distance)
- Normalized (0 to 1 scale)
- Works well with TF-IDF vectors
- Focuses on direction, not magnitude

**Example:**
```
Query: "Hanuman strength"
Query Vector: [0.5, 0.3, 0.1, ...]

Verse 1: "Hanuman is strong"
Verse 1 Vector: [0.6, 0.2, 0.1, ...]
Similarity: 0.92 (very similar)

Verse 2: "Rama is king"
Verse 2 Vector: [0.1, 0.1, 0.8, ...]
Similarity: 0.15 (not similar)
```

### 3. Prompt Engineering for Cultural Preservation

**Key Prompt Patterns:**

1. **Grounding Instructions:**
```
"Use ONLY the information from the provided verses.
 Do not add details not in the knowledge base.
 If information is not available, say so."
```

2. **Cultural Authenticity:**
```
"Maintain authentic representation of Indian
 mythological traditions. Respect spiritual and
 cultural significance."
```

3. **Creative Constraints:**
```
"Be creative in HOW you present the story, but
 stay true to WHAT the story contains. Use vivid
 descriptions, dialogue, and emotional depth while
 remaining faithful to the source material."
```

### 4. Multilingual TTS Language Detection

**Detection Algorithm:**
```python
1. Check for Devanagari script (Hindi, Marathi, Sanskrit)
   - Count Hindi-specific words: है, के, में
   - Count Marathi-specific words: आहे, चा, ची
   - Choose based on word frequency

2. Check for other Indian scripts:
   - Bengali: [\u0980-\u09FF]
   - Tamil: [\u0B00-\u0B7F]
   - Telugu: [\u0B80-\u0BFF]
   - etc.

3. Fallback to English if no script detected
```

### 5. Image Generation Pipeline

**Prompt Enhancement:**
```
Original: "Hanuman carrying mountain"

Enhanced:
"Hanuman carrying mountain, Indian comic book
 illustration style, vibrant colors, expressive
 characters, child-friendly, educational storytelling
 art, visual narrative that tells a story, detailed scene"
```

**API Call:**
```
URL: https://image.pollinations.ai/prompt/{encoded_prompt}
Parameters:
- width: 1024
- height: 1024
- model: flux
- enhance: true
- nologo: true
```

---

## Data Flow Diagrams

### Complete System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                          │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   [Text Input]    [Image Upload]  [Question]
        │               │               │
        ▼               ▼               ▼
┌───────────────┐ ┌──────────────┐ ┌──────────────┐
│  Text → Image │ │ Image → Text │ │   Q&A        │
│   Pipeline    │ │   Pipeline   │ │  Pipeline    │
└───────┬───────┘ └──────┬───────┘ └──────┬───────┘
        │                │                 │
        └────────────────┼─────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   RAG RETRIEVAL      │
              │  (TF-IDF + Cosine)  │
              └──────────┬───────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   LLM        │ │  Vision      │ │   LLM        │
│  (Gemini)    │ │  (Gemini)    │ │  (Gemini)    │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                 │
       └────────────────┼─────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Image Gen    │ │ Explanation  │ │   Answer     │
│(Pollinations)│ │  + TTS       │ │   + TTS      │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                 │
       └────────────────┼─────────────────┘
                        │
                        ▼
              ┌──────────────────────┐
              │   USER OUTPUT       │
              │ • Images            │
              │ • Stories           │
              │ • Audio             │
              │ • Explanations      │
              └──────────────────────┘
```

### Knowledge Base Structure

```
kb.json
│
├── Entry 1
│   ├── id: "verse_1"
│   ├── verse_number: 1
│   ├── text_sanskrit: "श्रीगुरु चरन सरोज..."
│   ├── text_transliteration: "Shri Guru Charan Saroj..."
│   ├── meaning_simple_en: "At the lotus feet of Guru..."
│   ├── meaning_detailed_en: "Detailed explanation..."
│   ├── context_story_en: "Story context..."
│   ├── story_seed_en: "Story seed..."
│   ├── image_prompt_en: "Visual description..."
│   ├── tags: ["devotion", "guru"]
│   └── emotion: ["respect", "devotion"]
│
├── Entry 2
│   └── ...
│
└── Entry N
    └── ...
```

### Embedding Process

```
Knowledge Base (kb.json)
    ↓
Loader (rag/loader.py)
    ↓
List of KBEntry objects
    ↓
Combine text fields:
- text_sanskrit
- text_transliteration
- meaning_simple_en
- meaning_detailed_en
- tags (joined)
    ↓
TF-IDF Vectorizer
    ↓
Fit on all verses
    ↓
Transform each verse
    ↓
Embedding Matrix
[Verse 1: [0.2, 0.1, 0.5, ...]]
[Verse 2: [0.3, 0.2, 0.1, ...]]
[Verse 3: [0.1, 0.4, 0.3, ...]]
...
```

---

## Why This Approach Preserves Culture

### 1. **Source of Truth**
- Knowledge base (`kb.json`) is the **single source of truth**
- All outputs are **derived from**, not **invented from**
- No external internet data pollutes the results

### 2. **Traceability**
- Every generated story can be traced back to specific verses
- Users can see which verses were used
- Transparency builds trust

### 3. **Scalability**
- Can add more verses to `kb.json`
- System automatically incorporates new knowledge
- Maintains consistency across additions

### 4. **Accessibility**
- Visual stories for children
- Multilingual support
- Audio narration
- Interactive Q&A

### 5. **Accuracy**
- RAG prevents hallucination
- Grounded in authentic sources
- Preserves original meanings

---

## Conclusion

**Verse2Vision** represents a new paradigm in cultural preservation:

1. **Technology as Preservation Tool**: Using AI to preserve, not replace, traditional knowledge
2. **Authenticity Through Architecture**: RAG ensures all outputs are grounded in original sources
3. **Accessibility Without Compromise**: Making knowledge accessible while maintaining accuracy
4. **Future-Proof**: Digital format ensures knowledge survives for generations

The system demonstrates that **modern AI can be a bridge to the past**, connecting ancient wisdom with future generations through authentic, grounded, and meaningful storytelling.

---

## Quick Reference

### Key Files
- `app_streamlit.py`: Main UI
- `rag/loader.py`: Load knowledge base
- `rag/embeddings.py`: TF-IDF vectorization
- `rag/retriever.py`: Verse retrieval
- `rag/generator.py`: LLM generation
- `rag/vision.py`: Image captioning
- `rag/image_generator.py`: Image generation
- `rag/tts.py`: Text-to-speech
- `kb.json`: Knowledge base

### Key Concepts
- **RAG**: Retrieval-Augmented Generation
- **TF-IDF**: Term Frequency-Inverse Document Frequency
- **Cosine Similarity**: Vector similarity measure
- **Multimodal**: Handling multiple data types (text, image, audio)
- **Bidirectional**: Text→Image and Image→Text workflows
- **Grounding**: Ensuring outputs are based on knowledge base

### API Endpoints
- Gemini API: `https://generativelanguage.googleapis.com`
- Pollinations API: `https://image.pollinations.ai/prompt/`
- Google TTS: Cloud service via `gtts` library

---

*This documentation provides a complete understanding of the Verse2Vision system, its architecture, workflow, and cultural preservation mission.*

