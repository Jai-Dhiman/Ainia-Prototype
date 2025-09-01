"""Multi-modal system for Ainia Adventure Stories - Phase 7 Enhancement."""

import streamlit as st
import pyttsx3
import threading
from gtts import gTTS
import io
import base64
from PIL import Image
import requests
from openai import OpenAI
import google.generativeai as genai
from google.cloud import texttospeech
from typing import Dict, List, Optional, Tuple, Any
import json
import os
import time
import tempfile
from streamlit_drawable_canvas import st_canvas


class TextToSpeechManager:
    """Manages Google Cloud Text-to-Speech functionality with child-friendly voices."""
    
    def __init__(self):
        self.client = None
        self.available_voices = []
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Google Cloud TTS client."""
        try:
            # Check for Google Cloud credentials
            if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or os.getenv("GOOGLE_CLOUD_PROJECT"):
                self.client = texttospeech.TextToSpeechClient()
                self.available_voices = self._get_available_voices()
            else:
                st.info("💡 Add Google Cloud credentials for high-quality voice generation! Using fallback gTTS for now.")
                self.available_voices = [{'id': 'gtts-en', 'name': 'Google TTS (English)', 'type': 'fallback'}]
        except Exception as e:
            st.warning(f"Google Cloud TTS initialization failed: {e}. Using fallback gTTS.")
            self.available_voices = [{'id': 'gtts-en', 'name': 'Google TTS (English)', 'type': 'fallback'}]
    
    def _get_available_voices(self) -> List[Dict[str, str]]:
        """Get available child-friendly voices from Google Cloud TTS."""
        if not self.client:
            return [{'id': 'gtts-en', 'name': 'Google TTS (English)', 'type': 'fallback'}]
        
        try:
            # Get list of available voices
            voices_response = self.client.list_voices()
            
            # Define child-friendly voices (WaveNet and Neural2 for best quality)
            child_friendly_voices = [
                # English US - Female WaveNet voices (good for children)
                {'id': 'en-US-Wavenet-C', 'name': 'Emma (US Female, WaveNet)', 'lang': 'en-US', 'gender': 'FEMALE', 'type': 'WAVENET'},
                {'id': 'en-US-Wavenet-E', 'name': 'Ava (US Female, WaveNet)', 'lang': 'en-US', 'gender': 'FEMALE', 'type': 'WAVENET'},
                {'id': 'en-US-Wavenet-F', 'name': 'Sophie (US Female, WaveNet)', 'lang': 'en-US', 'gender': 'FEMALE', 'type': 'WAVENET'},
                {'id': 'en-US-Wavenet-H', 'name': 'Grace (US Female, WaveNet)', 'lang': 'en-US', 'gender': 'FEMALE', 'type': 'WAVENET'},
                
                # English US - Neural2 voices (newest, best quality)
                {'id': 'en-US-Neural2-C', 'name': 'Emma (US Female, Neural2)', 'lang': 'en-US', 'gender': 'FEMALE', 'type': 'NEURAL2'},
                {'id': 'en-US-Neural2-E', 'name': 'Ava (US Female, Neural2)', 'lang': 'en-US', 'gender': 'FEMALE', 'type': 'NEURAL2'},
                {'id': 'en-US-Neural2-F', 'name': 'Sophie (US Female, Neural2)', 'lang': 'en-US', 'gender': 'FEMALE', 'type': 'NEURAL2'},
                {'id': 'en-US-Neural2-H', 'name': 'Grace (US Female, Neural2)', 'lang': 'en-US', 'gender': 'FEMALE', 'type': 'NEURAL2'},
                
                # English GB - For variety
                {'id': 'en-GB-Wavenet-A', 'name': 'Lily (British Female, WaveNet)', 'lang': 'en-GB', 'gender': 'FEMALE', 'type': 'WAVENET'},
                {'id': 'en-GB-Wavenet-C', 'name': 'Rose (British Female, WaveNet)', 'lang': 'en-GB', 'gender': 'FEMALE', 'type': 'WAVENET'},
            ]
            
            # Filter to only include actually available voices
            available_voices = []
            available_voice_names = {voice.name for voice in voices_response.voices}
            
            for voice in child_friendly_voices:
                if voice['id'] in available_voice_names:
                    available_voices.append(voice)
            
            # Add fallback if no voices available
            if not available_voices:
                available_voices = [{'id': 'gtts-en', 'name': 'Google TTS (English)', 'type': 'fallback'}]
            
            return available_voices
            
        except Exception as e:
            st.warning(f"Failed to get voice list: {e}")
            return [{'id': 'gtts-en', 'name': 'Google TTS (English)', 'type': 'fallback'}]
    
    def speak_text(self, text: str, voice_id: str = 'en-US-Neural2-C', speed: float = 1.0) -> Optional[bytes]:
        """Convert text to speech using Google Cloud TTS and return audio bytes."""
        try:
            # Handle fallback to gTTS
            if voice_id == 'gtts-en' or not self.client:
                return self._fallback_gtts(text, speed)
            
            # Prepare the synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Build the voice request
            voice = texttospeech.VoiceSelectionParams(
                name=voice_id,
                language_code=voice_id.split('-')[0] + '-' + voice_id.split('-')[1],  # e.g., en-US
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )
            
            # Select the type of audio file
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=speed,
                pitch=2.0 if 'child' in voice_id.lower() else 0.0,  # Slightly higher pitch for child-friendly
                effects_profile_id=['headphone-class-device']  # Optimize for headphones/speakers
            )
            
            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            return response.audio_content
            
        except Exception as e:
            st.error(f"Google Cloud TTS failed: {e}. Falling back to basic TTS.")
            return self._fallback_gtts(text, speed)
    
    def _fallback_gtts(self, text: str, speed: float) -> Optional[bytes]:
        """Fallback to basic gTTS if Google Cloud TTS fails."""
        try:
            tts = gTTS(text=text, lang='en', slow=speed < 0.8)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer.getvalue()
        except Exception as e:
            st.error(f"Fallback TTS also failed: {e}")
            return None

    def create_audio_player(self, text: str, voice_id: str = 'en-US-Neural2-C', speed: float = 1.0):
        """Create Streamlit audio player for text using Google Cloud TTS."""
        with st.spinner("🎵 Creating beautiful voice..."):
            audio_bytes = self.speak_text(text, voice_id, speed)
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3')
            else:
                st.warning("Audio generation failed")


class ImageGenerator:
    """Manages Gemini 2.5 Flash Image integration for story illustrations."""
    
    def __init__(self, gemini_api_key: str):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-image')
        self.image_cache = {}
    
    def generate_story_illustration(self, story_text: str, theme: str, style: str = "children's book illustration") -> Optional[str]:
        """Generate illustration for story using Gemini 2.5 Flash Image."""
        try:
            # Create child-friendly prompt
            illustration_prompt = f"""
            Create a {style} for a children's adventure story about {theme}.
            The scene should be: {story_text[:200]}...
            Make it colorful, magical, and appropriate for children ages 5-9.
            No scary or violent elements. Focus on wonder and adventure.
            Style: bright colors, whimsical, storybook quality, digital art.
            High quality, detailed, engaging for children.
            """
            
            # Check cache first
            cache_key = f"{theme}_{hash(story_text[:100])}"
            if cache_key in self.image_cache:
                return self.image_cache[cache_key]
            
            response = self.model.generate_content([illustration_prompt])
            
            if response.candidates and response.candidates[0].content.parts:
                # Gemini 2.5 Flash Image returns the image directly
                image_data = response.candidates[0].content.parts[0]
                if hasattr(image_data, 'inline_data'):
                    # Convert to base64 data URL for display
                    image_url = f"data:image/png;base64,{image_data.inline_data.data}"
                    self.image_cache[cache_key] = image_url
                    return image_url
            
            return None
            
        except Exception as e:
            st.error(f"Image generation failed: {e}")
            return None
    
    def create_vocabulary_card(self, word: str, definition: str) -> Optional[str]:
        """Generate visual vocabulary card."""
        try:
            prompt = f"""
            Create a colorful educational card illustration for the word '{word}'.
            Definition: {definition}
            Make it look like a fun vocabulary flash card for children.
            Include the word '{word}' prominently displayed on the card.
            Show a visual representation of the word's meaning.
            Bright colors, simple design, educational and engaging.
            Child-friendly cartoon style, suitable for ages 5-9.
            """
            
            response = self.model.generate_content([prompt])
            
            if response.candidates and response.candidates[0].content.parts:
                image_data = response.candidates[0].content.parts[0]
                if hasattr(image_data, 'inline_data'):
                    return f"data:image/png;base64,{image_data.inline_data.data}"
            
            return None
            
        except Exception as e:
            st.error(f"Vocabulary card generation failed: {e}")
            return None


class InteractiveStoryElements:
    """Manages interactive decision points and mini-games."""
    
    def __init__(self, story_generator):
        self.story_generator = story_generator
    
    def create_decision_point(self, story_context: str, theme: str) -> Dict[str, Any]:
        """Generate interactive decision point in story."""
        try:
            decision_prompt = f"""
            Based on this story context: {story_context}
            
            Create an interactive decision point for a child aged 5-9.
            Return ONLY a JSON object with this exact format:
            {{
                "situation": "What happens next in the story (1-2 sentences)",
                "choices": [
                    {{"option": "Choice 1", "consequence": "What happens if they choose this"}},
                    {{"option": "Choice 2", "consequence": "What happens if they choose this"}},
                    {{"option": "Choice 3", "consequence": "What happens if they choose this"}}
                ],
                "learning_moment": "Educational element embedded in choices"
            }}
            
            Make choices age-appropriate and themed around: {theme}
            """
            
            response = self.story_generator.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": decision_prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            decision_data = json.loads(response.choices[0].message.content)
            return decision_data
            
        except Exception as e:
            st.error(f"Decision point generation failed: {e}")
            return {}
    
    def create_word_scramble_game(self, vocabulary_words: List[str]) -> Dict[str, str]:
        """Create word scramble mini-game."""
        import random
        
        if not vocabulary_words:
            return {}
        
        word = random.choice(vocabulary_words)
        scrambled = ''.join(random.sample(word, len(word)))
        
        return {
            'original_word': word,
            'scrambled_word': scrambled,
            'hint': f"This word has {len(word)} letters and is from our story!"
        }
    
    def create_matching_game(self, words: List[str], definitions: List[str]) -> Dict[str, Any]:
        """Create matching game for vocabulary."""
        import random
        
        if len(words) != len(definitions) or not words:
            return {}
        
        # Shuffle for the game
        shuffled_words = words.copy()
        random.shuffle(shuffled_words)
        
        return {
            'words': shuffled_words,
            'definitions': definitions,
            'correct_pairs': dict(zip(words, definitions))
        }


class DrawingCanvas:
    """Manages drawing canvas for children to illustrate scenes."""
    
    def create_drawing_canvas(self, prompt: str, width: int = 600, height: int = 400) -> Optional[Image.Image]:
        """Create interactive drawing canvas."""
        st.write(f"🎨 **Draw your version of:** {prompt}")
        
        # Drawing canvas
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0.3)",
            stroke_width=5,
            stroke_color="#000000",
            background_color="#FFFFFF",
            background_image=None,
            update_streamlit=True,
            height=height,
            width=width,
            drawing_mode="freedraw",
            point_display_radius=0,
            key="drawing_canvas",
        )
        
        if canvas_result.image_data is not None:
            return Image.fromarray(canvas_result.image_data.astype("uint8"), "RGBA")
        return None
    
    def save_child_artwork(self, image: Image.Image, child_name: str, story_theme: str) -> str:
        """Save child's artwork with metadata."""
        try:
            filename = f"artwork_{child_name}_{story_theme}_{int(time.time())}.png"
            filepath = os.path.join("saved_artwork", filename)
            
            os.makedirs("saved_artwork", exist_ok=True)
            image.save(filepath)
            
            return filepath
        except Exception as e:
            st.error(f"Failed to save artwork: {e}")
            return ""


class MultiModalStoryExperience:
    """Orchestrates the complete multi-modal story experience."""
    
    def __init__(self, api_key: str, story_generator):
        # Get Gemini API key for image generation
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            st.warning("⚠️ Gemini API key not found! Image generation will be disabled. Please add GEMINI_API_KEY to your .env file.")
            self.image_generator = None
        else:
            self.image_generator = ImageGenerator(gemini_api_key)
        
        self.tts_manager = TextToSpeechManager()
        self.interactive_elements = InteractiveStoryElements(story_generator)
        self.drawing_canvas = DrawingCanvas()
        self.story_generator = story_generator
    
    def create_enhanced_story_display(self, story_data: Dict[str, Any], theme: str, child_name: str):
        """Create rich multi-modal story display."""
        story_text = story_data.get('story', '')
        
        # Story title with audio
        st.markdown("### 🎵 Listen to Your Adventure")
        
        # Voice selection
        voices = self.tts_manager.available_voices
        selected_voice = st.selectbox(
            "Choose a voice for your story:",
            options=[v['id'] for v in voices],
            format_func=lambda x: next(v['name'] for v in voices if v['id'] == x),
            key="voice_selection"
        )
        
        # Reading speed
        reading_speed = st.slider("Reading Speed", 0.5, 1.5, 1.0, 0.1, key="reading_speed")
        
        # Audio player
        if st.button("🔊 Play Story", key="play_story"):
            self.tts_manager.create_audio_player(story_text, selected_voice, reading_speed)
        
        # Story illustration
        st.markdown("### 🎨 Story Illustration")
        if self.image_generator:
            with st.spinner("Creating magical illustration..."):
                illustration_url = self.image_generator.generate_story_illustration(story_text, theme)
                if illustration_url:
                    st.image(illustration_url, caption=f"An adventure in {theme}!", use_column_width=True)
        else:
            st.info("🎨 Image generation is currently disabled. Please add your Gemini API key to enable story illustrations!")
        
        # Story text with enhanced formatting
        st.markdown("### 📖 Your Story")
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            font-size: 1.1rem;
            line-height: 1.6;
            margin: 1rem 0;
        ">
        {story_text}
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive elements
        if st.button("🎮 Make a Story Choice!", key="story_choice"):
            decision_data = self.interactive_elements.create_decision_point(story_text, theme)
            if decision_data:
                self._display_decision_point(decision_data)
        
        # Vocabulary cards
        vocabulary_words = story_data.get('vocabulary_words', [])
        if vocabulary_words:
            st.markdown("### 📚 New Words You Learned")
            for word in vocabulary_words:
                with st.expander(f"🌟 {word.upper()}"):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if self.image_generator:
                            vocab_image_url = self.image_generator.create_vocabulary_card(
                                word, story_data.get('vocabulary_definitions', {}).get(word, '')
                            )
                            if vocab_image_url:
                                st.image(vocab_image_url, use_column_width=True)
                        else:
                            st.info("📸 Add Gemini API key for vocabulary cards")
                    with col2:
                        st.write(f"**Definition:** {story_data.get('vocabulary_definitions', {}).get(word, 'A wonderful word!')}")
                        if st.button(f"🔊 Hear '{word}'", key=f"word_{word}"):
                            self.tts_manager.create_audio_player(f"The word is {word}. {story_data.get('vocabulary_definitions', {}).get(word, '')}")
        
        # Drawing activity
        st.markdown("### ✏️ Draw Your Adventure")
        drawing_prompt = f"Draw your favorite part of {child_name}'s {theme} adventure!"
        child_drawing = self.drawing_canvas.create_drawing_canvas(drawing_prompt)
        
        if child_drawing and st.button("💾 Save My Artwork!", key="save_artwork"):
            filepath = self.drawing_canvas.save_child_artwork(child_drawing, child_name, theme)
            if filepath:
                st.success(f"🎉 Your amazing artwork has been saved! Great job, {child_name}!")
        
        # Mini-games
        self._create_story_games(vocabulary_words, theme)
    
    def _display_decision_point(self, decision_data: Dict[str, Any]):
        """Display interactive decision point."""
        st.markdown("### 🌟 Your Choice Shapes the Adventure!")
        
        situation = decision_data.get('situation', '')
        choices = decision_data.get('choices', [])
        
        st.write(situation)
        
        if choices:
            choice_labels = [choice['option'] for choice in choices]
            selected_choice = st.radio("What do you choose?", choice_labels, key="story_decision")
            
            if st.button("✨ See What Happens!", key="execute_choice"):
                for choice in choices:
                    if choice['option'] == selected_choice:
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(45deg, #FFD700, #FFA500);
                            padding: 1.5rem;
                            border-radius: 10px;
                            color: #2D3748;
                            font-weight: bold;
                            margin: 1rem 0;
                        ">
                        🌟 {choice['consequence']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Generate TTS for the consequence
                        self.tts_manager.create_audio_player(choice['consequence'])
                        break
    
    def _create_story_games(self, vocabulary_words: List[str], theme: str):
        """Create mini-games related to the story."""
        if not vocabulary_words:
            return
        
        st.markdown("### 🎲 Fun Learning Games")
        
        tab1, tab2 = st.tabs(["🔤 Word Scramble", "🧩 Memory Match"])
        
        with tab1:
            if st.button("🎮 Start Word Scramble!", key="start_scramble"):
                game_data = self.interactive_elements.create_word_scramble_game(vocabulary_words)
                if game_data:
                    st.write(f"**Unscramble this word:** `{game_data['scrambled_word']}`")
                    st.write(game_data['hint'])
                    
                    user_answer = st.text_input("Your answer:", key="scramble_answer")
                    
                    if st.button("✅ Check Answer", key="check_scramble"):
                        if user_answer.lower() == game_data['original_word'].lower():
                            st.success("🎉 Correct! You're amazing!")
                            st.balloons()
                        else:
                            st.info(f"Close! The answer was: {game_data['original_word']}")
        
        with tab2:
            st.write("Match the words with their meanings!")
            # Simple matching implementation
            if vocabulary_words and len(vocabulary_words) >= 2:
                import random
                sample_words = random.sample(vocabulary_words, min(3, len(vocabulary_words)))
                
                for word in sample_words:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**{word}**")
                    with col2:
                        # This would need the definitions from story_data
                        st.write("(Definition would appear here)")