"""Streamlit frontend for Bidirectional Multimodal RAG System."""
import streamlit as st
import os
from pathlib import Path
from PIL import Image

from rag.loader import load_kb, KBEntry
from rag.embeddings import EmbeddingStore
from rag.retriever import retrieve_verses
from rag.generator import (
    ask_gemini, build_qa_prompt, build_story_prompt, 
    build_image_prompt_text, build_enhanced_image_prompt, build_image_to_text_prompt,
    build_sequential_story_images_prompt, parse_sequential_image_descriptions
)
from rag.vision import caption_image
from rag.image_generator import generate_image_from_prompt, generate_image_from_rag_prompt, generate_sequential_images
from rag.tts import generate_speech


# Page configuration
st.set_page_config(
    page_title="Verse2Vision",
    page_icon="🕉️",
    layout="wide"
)

# Initialize session state
if "kb_entries" not in st.session_state:
    st.session_state.kb_entries = None
if "embedding_store" not in st.session_state:
    st.session_state.embedding_store = None
if "initialized" not in st.session_state:
    st.session_state.initialized = False
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""


def initialize_app():
    """Load KB and build embeddings."""
    try:
        # Get paths
        kb_path = Path("kb.json")
        if not kb_path.exists():
            kb_path = Path("data/kb.json")
        
        if not kb_path.exists():
            st.error(f"Knowledge base not found. Expected at: {kb_path}")
            return False
        
        with st.spinner("Loading knowledge base..."):
            entries = load_kb(kb_path)
            st.session_state.kb_entries = entries
        
        with st.spinner("Building embeddings (this may take a minute)..."):
            embedding_store = EmbeddingStore()
            embedding_store.build_embeddings(entries)
            st.session_state.embedding_store = embedding_store
        
        st.session_state.initialized = True
        return True
    except Exception as e:
        st.error(f"Error initializing app: {e}")
        return False


def get_api_key() -> str:
    """Get API key from session state or environment variable."""
    if st.session_state.gemini_api_key:
        return st.session_state.gemini_api_key
    return os.getenv("GEMINI_API_KEY", "")


# Initialize on first load
if not st.session_state.initialized:
    if not initialize_app():
        st.stop()


# Title - Cleaner, more visual
st.title("🕉️ Verse2Vision")
st.markdown("### *Create visual stories for children with cultural preservation*")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🔑 API Configuration")
    
    # API Key Input
    api_key_input = st.text_input(
        "Gemini API Key:",
        value=st.session_state.gemini_api_key,
        type="password",
        placeholder="Enter your Google Gemini API key",
        help="Get your API key from https://makersuite.google.com/app/apikey"
    )
    
    # Update session state when user enters API key
    if api_key_input != st.session_state.gemini_api_key:
        st.session_state.gemini_api_key = api_key_input
    
    # Check API key status
    api_key = get_api_key()
    if api_key:
        st.success("✅ API key configured")
    else:
        st.warning("⚠️ API key required for AI features")
    
    st.markdown("---")
    st.header("📖 Verse Explorer")
    
    if st.session_state.kb_entries:
        verse_options = {
            f"Verse {entry.verse_number} - {entry.id}": entry
            for entry in st.session_state.kb_entries
        }
        
        selected_verse_label = st.selectbox(
            "Select a verse:",
            options=list(verse_options.keys())
        )
        
        selected_verse = verse_options[selected_verse_label]
        
        st.markdown("### Sanskrit")
        st.text(selected_verse.text_sanskrit)
        
        st.markdown("### Transliteration")
        st.text(selected_verse.text_transliteration)
        
        st.markdown("### Simple Meaning")
        st.write(selected_verse.meaning_simple_en)
        
        with st.expander("📝 Detailed Meaning"):
            st.write(selected_verse.meaning_detailed_en)
        
        with st.expander("🎨 Image Prompt"):
            st.text(selected_verse.image_prompt_en)
        
        with st.expander("📚 Story Seed"):
            st.write(selected_verse.story_seed_en)
        
        with st.expander("🏷️ Tags"):
            st.write(", ".join(selected_verse.tags))
        
        with st.expander("😊 Emotions"):
            st.write(", ".join(selected_verse.emotion))


# Main area - Simplified Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 Create Story", 
    "🔍 Analyze Image", 
    "💬 Ask Question", 
    "📚 Text Story"
])

# Tab 1: Story Creation (Main Feature)
with tab1:
    st.header("📖 Create Visual Story")
    
    # Simple, clean input
    text_input = st.text_input(
        "What story would you like to see?",
        placeholder='e.g., "Hanuman carrying Sanjeevani mountain" or "Hanuman meets Rama"',
        help="Enter a topic, verse, or story idea"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        top_k = st.slider("Verses to use:", min_value=1, max_value=5, value=3)
    
    if st.button("🎨 Create Story", type="primary", use_container_width=True) and text_input:
        api_key = get_api_key()
        if not api_key:
            st.error("⚠️ Please enter your Gemini API key in the sidebar.")
        else:
            with st.spinner("Creating your story..."):
                try:
                    # Retrieve relevant verses
                    results = retrieve_verses(
                        text_input,
                        st.session_state.embedding_store,
                        top_k=top_k
                    )
                    
                    if results:
                        # Generate 3 sequential comic-style storytelling images
                        story_prompt = build_sequential_story_images_prompt(text_input, results)
                        descriptions_response = ask_gemini(story_prompt, api_key)
                        
                        # Parse descriptions with subtitles
                        image_data = parse_sequential_image_descriptions(descriptions_response)
                        
                        # Generate images
                        generated_story = []
                        progress_container = st.container()
                        
                        with progress_container:
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            for i, (visual_desc, subtitle) in enumerate(image_data, 1):
                                status_text.text(f"🎨 Creating Scene {i}/3...")
                                
                                # Enhance prompt with comic style - subtitle will be displayed in UI, not in image
                                # But we mention it in prompt to guide the visual storytelling
                                comic_prompt = f"{visual_desc}, Indian comic book illustration style, vibrant colors, expressive characters, child-friendly, educational storytelling art, visual narrative that tells a story, detailed scene"
                                
                                try:
                                    image = generate_image_from_prompt(comic_prompt, method="pollinations")
                                    if image:
                                        generated_story.append((i, subtitle, image, visual_desc))
                                    progress_bar.progress(i / 3)
                                except Exception as e:
                                    st.warning(f"Scene {i} generation failed: {e}")
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Display story in clean, visual format
                        if generated_story:
                            st.markdown("---")
                            st.markdown("## 📚 Your Story")
                            
                            # Generate narration text
                            narration_parts = [f"Scene {i}: {subtitle}" for i, subtitle, _, _ in generated_story]
                            full_narration = ". ".join(narration_parts) + "."
                            
                            # Create TTS audio (multilingual auto-detect)
                            audio_data = generate_speech(full_narration)
                            
                            # Display audio player if available
                            if audio_data:
                                st.audio(audio_data, format="audio/mp3", autoplay=False)
                                st.caption("🔊 Listen to the story narration (multilingual)")
                            
                            # Display images with subtitles
                            for i, subtitle, image, visual_desc in generated_story:
                                st.markdown(f"### Scene {i}")
                                
                                # Large subtitle display
                                st.info(f"💬 **{subtitle}**")
                                
                                # Image - reduced size
                                st.image(image, width=600)
                                
                                if i < len(generated_story):
                                    st.markdown("---")
                    else:
                        st.warning("No verses found. Try a different topic.")
                except Exception as e:
                    st.error(f"Error: {e}")

# Tab 2: Image Analysis
with tab2:
    st.header("🔍 Analyze Image")
    
    uploaded_file = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, width=500)
        
        if st.button("🔍 Analyze", type="primary", use_container_width=True):
            api_key = get_api_key()
            if not api_key:
                st.error("⚠️ Please enter your Gemini API key in the sidebar.")
            else:
                with st.spinner("Analyzing..."):
                    try:
                        image_caption = caption_image(image, api_key)
                        results = retrieve_verses(
                            image_caption,
                            st.session_state.embedding_store,
                            top_k=5
                        )
                        
                        if results:
                            prompt = build_image_to_text_prompt(image_caption, results)
                            explanation = ask_gemini(prompt, api_key)
                            
                            st.markdown("### 📖 Story")
                            st.write(explanation)
                            
                            # Add TTS narration
                            audio_data = generate_speech(explanation)
                            if audio_data:
                                st.audio(audio_data, format="audio/mp3", autoplay=False)
                                st.caption("🔊 Listen to the explanation")
                        else:
                            st.warning("No matching verses found.")
                    except Exception as e:
                        st.error(f"Error: {e}")

# Tab 3: Ask Questions
with tab3:
    st.header("💬 Ask a Question")
    
    query = st.text_input("Your question:", placeholder='e.g., "What does this verse mean?"')
    
    if st.button("🔍 Ask", type="primary", use_container_width=True) and query:
        api_key = get_api_key()
        if not api_key:
            st.error("⚠️ Please enter your Gemini API key in the sidebar.")
        else:
            with st.spinner("Finding answer..."):
                try:
                    results = retrieve_verses(
                        query,
                        st.session_state.embedding_store,
                        top_k=5
                    )
                    
                    if results:
                        prompt = build_qa_prompt(query, results)
                        answer = ask_gemini(prompt, api_key)
                        
                        st.markdown("### 💡 Answer")
                        st.write(answer)
                        
                        # Add TTS narration
                        audio_data = generate_speech(answer)
                        if audio_data:
                            st.audio(audio_data, format="audio/mp3", autoplay=False)
                            st.caption("🔊 Listen to the answer")
                    else:
                        st.warning("No verses found. Try a different question.")
                except Exception as e:
                    st.error(f"Error: {e}")

# Tab 4: Text Story
with tab4:
    st.header("📖 Generate Text Story")
    
    story_query = st.text_input("Story topic:", placeholder='e.g., "Hanuman\'s devotion"')
    
    if st.button("📖 Generate", type="primary", use_container_width=True) and story_query:
        api_key = get_api_key()
        if not api_key:
            st.error("⚠️ Please enter your Gemini API key in the sidebar.")
        else:
            with st.spinner("Creating story..."):
                try:
                    results = retrieve_verses(
                        story_query,
                        st.session_state.embedding_store,
                        top_k=3
                    )
                    
                    if results:
                        prompt = build_story_prompt(results)
                        story = ask_gemini(prompt, api_key)
                        
                        st.markdown("### 📚 Story")
                        st.write(story)
                        
                        # Add TTS for text story (multilingual auto-detect)
                        audio_data = generate_speech(story)
                        if audio_data:
                            st.audio(audio_data, format="audio/mp3", autoplay=False)
                            st.caption("🔊 Listen to the story (multilingual)")
                    else:
                        st.warning("No verses found. Try a different topic.")
                except Exception as e:
                    st.error(f"Error: {e}")


