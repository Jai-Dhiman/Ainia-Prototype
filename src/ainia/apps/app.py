"""Streamlit web application for Ainia Adventure Stories - Simplified MVP with TTS."""

import streamlit as st
import os
import time
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
from gtts import gTTS
import io
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from ..core.multi_question_system import (
    MultiQuestionStoryGenerator, StorySession, DifficultyLevel,
    QuestionResult, AdaptiveDifficultyManager
)

# Load environment variables
load_dotenv()


def initialize_session_state():
    """Initialize session state variables for multi-question stories."""
    if 'story_session' not in st.session_state:
        st.session_state.story_session = None
    if 'multi_story_generator' not in st.session_state:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            st.session_state.multi_story_generator = MultiQuestionStoryGenerator(api_key)
    if 'current_question_start_time' not in st.session_state:
        st.session_state.current_question_start_time = None
    if 'waiting_for_answer' not in st.session_state:
        st.session_state.waiting_for_answer = False


class TextToSpeechManager:
    """Simple TTS manager using gTTS for story narration."""
    
    def create_audio_for_text(self, text):
        """Create audio from text using gTTS."""
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer.getvalue()
        except Exception as e:
            st.error(f"Audio generation failed: {e}")
            return None
    
    def create_audio_player(self, text, label="🎵 Listen to your story"):
        """Create Streamlit audio player for text."""
        with st.spinner("🎵 Creating audio..."):
            audio_bytes = self.create_audio_for_text(text)
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3')
            else:
                st.warning("Audio generation not available")


class DrawingCanvas:
    """Manages drawing canvas for children to illustrate scenes."""
    
    def create_drawing_canvas(self, prompt: str, width: int = 600, height: int = 400) -> Image.Image:
        """Create interactive drawing canvas."""
        st.markdown(f"🎨 **Draw your version of:** {prompt}")
        
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
            # Create filename with timestamp
            timestamp = int(time.time())
            filename = f"artwork_{child_name}_{story_theme}_{timestamp}.png"
            
            # Create saved_artwork directory if it doesn't exist
            os.makedirs("saved_artwork", exist_ok=True)
            
            filepath = os.path.join("saved_artwork", filename)
            image.save(filepath)
            
            return filepath
        except Exception as e:
            st.error(f"Failed to save artwork: {e}")
            return ""


def display_progress_indicator(session: StorySession):
    """Display progress indicator showing current question and difficulty."""
    if not session:
        return
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        progress = session.get_progress_percentage()
        st.progress(progress / 100.0, text=f"Progress: {progress}%")
    
    with col2:
        current_q = len(session.question_results) + 1
        if current_q <= 3:
            st.markdown(f"**Question {current_q}/3**")
    
    with col3:
        difficulty_colors = {
            DifficultyLevel.EASY: "🟢",
            DifficultyLevel.MEDIUM: "🟡", 
            DifficultyLevel.HARD: "🔴"
        }
        difficulty_icon = difficulty_colors.get(session.difficulty_level, "🟢")
        st.markdown(f"**Difficulty: {difficulty_icon} {session.difficulty_level.name.title()}**")


def display_completed_parts_with_qa(session: StorySession, tts_manager=None):
    """Display completed story parts with their questions and answers."""
    if not session or not session.story_parts:
        return
    
    st.markdown("### 📖 Your Adventure Journey")
    
    # Display each completed part with its Q&A
    for i, part in enumerate(session.story_parts):
        part_num = i + 1
        
        # Only show parts that have been completed (have results)
        if i < len(session.question_results):
            result = session.question_results[i]
            
            st.markdown(f"---")
            st.markdown(f"## 🏰 Part {part_num}")
            
            # Story part
            st.markdown(f'''
            <div style="
                background: #f8f9fa;
                border-radius: 10px;
                padding: 1.5rem;
                border: 2px solid #dee2e6;
                margin: 1rem 0;
                font-size: 1.1rem;
                line-height: 1.6;
                color: #212529;
            ">
                {part.replace(chr(10), "<br>")}
            </div>
            ''', unsafe_allow_html=True)
            
            # Add individual TTS button for this part (on-demand)
            if tts_manager:
                if st.button(f"🎵 Listen to Part {part_num}", key=f"tts_part_{part_num}"):
                    tts_manager.create_audio_player(part, f"🎵 Part {part_num} Audio")
            
            # Question and answer section
            st.markdown("#### 🤔 The Challenge:")
            st.markdown(f'''
            <div style="
                background: #e8f4f8;
                padding: 1rem;
                border-radius: 8px;
                border-left: 4px solid #17a2b8;
                margin: 0.5rem 0;
                color: #0c5460;
            ">
                <strong>Question:</strong> {result.question_text}
            </div>
            ''', unsafe_allow_html=True)
            
            # Show answer with success/failure styling
            if result.is_correct:
                st.markdown(f'''
                <div style="
                    background: #d4edda;
                    padding: 1rem;
                    border-radius: 8px;
                    border-left: 4px solid #28a745;
                    margin: 0.5rem 0;
                    color: #155724;
                ">
                    <strong>Your Answer:</strong> {result.user_answer} ✅<br>
                    <strong>Result:</strong> Correct! Great job! 🌟
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div style="
                    background: #f8d7da;
                    padding: 1rem;
                    border-radius: 8px;
                    border-left: 4px solid #dc3545;
                    margin: 0.5rem 0;
                    color: #721c24;
                ">
                    <strong>Your Answer:</strong> {result.user_answer}<br>
                    <strong>Correct Answer:</strong> {result.correct_answer}<br>
                    <strong>Result:</strong> Good try! Keep learning! 💪
                </div>
                ''', unsafe_allow_html=True)
            
            # Show explanation in an expandable section
            with st.expander(f"💡 Learning Explanation for Part {part_num}"):
                st.markdown(result.explanation)


def display_current_story_part(session: StorySession, tts_manager=None):
    """Display the current story part that needs to be answered."""
    if not session or not session.story_parts:
        return
    
    # Get the current part (the latest one)
    current_part_index = len(session.question_results)
    if current_part_index < len(session.story_parts):
        part = session.story_parts[current_part_index]
        part_num = current_part_index + 1
        
        st.markdown(f"---")
        st.markdown(f"## 🏰 Part {part_num} - New!")
        
        # Story part
        st.markdown(f'''
        <div style="
            background: #fff3cd;
            border-radius: 10px;
            padding: 1.5rem;
            border: 2px solid #ffc107;
            margin: 1rem 0;
            font-size: 1.1rem;
            line-height: 1.6;
            color: #212529;
        ">
            {part.replace(chr(10), "<br>")}
        </div>
        ''', unsafe_allow_html=True)
        
        # Add individual TTS button for this part (on-demand)
        if tts_manager:
            if st.button(f"🎵 Listen to Part {part_num}", key=f"tts_current_part_{part_num}"):
                tts_manager.create_audio_player(part, f"🎵 Part {part_num} Audio")


def display_question_section(session: StorySession, current_question_data: dict):
    """Display current question and handle user input."""
    questions_answered = len(session.question_results)
    
    st.markdown("### 🤔 Can you help solve this challenge?")
    
    # Display question in styled container
    st.markdown(f'''
    <div style="
        background: #e8f4f8;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #17a2b8;
        margin: 1rem 0;
    ">
        <h4 style="color: #0c5460; margin-bottom: 1rem;">
            {current_question_data["question"]}
        </h4>
    </div>
    ''', unsafe_allow_html=True)
    
    # Answer input based on learning focus
    clean_focus = session.learning_focus.replace("🔢 ", "").replace("📚 ", "").replace("🧩 ", "")
    
    if "counting" in clean_focus.lower() or "math" in clean_focus.lower() or "addition" in clean_focus.lower():
        user_answer = st.number_input(
            "Your answer:",
            min_value=0,
            max_value=100,
            step=1,
            help="Take your time and think it through!",
            key=f"answer_input_q{questions_answered}"
        )
    else:
        user_answer = st.text_input(
            "Your answer:",
            placeholder="Type your answer here...",
            help="Share your thoughts!",
            key=f"answer_input_q{questions_answered}"
        )
    
    # Submit button
    if st.button("✨ Submit My Answer! ✨", type="primary", use_container_width=True, key=f"submit_q{questions_answered}"):
        if user_answer is not None and str(user_answer).strip():
            # Calculate response time
            response_time = time.time() - st.session_state.current_question_start_time if st.session_state.current_question_start_time else 10.0
            
            # Process the answer
            is_correct, result = st.session_state.multi_story_generator.process_answer(
                session, user_answer, response_time
            )
            
            # Store answer result in session state to persist across reruns
            st.session_state.last_answer_result = {
                'is_correct': is_correct,
                'result': result,
                'processed': True
            }
            
            # Force rerun to show feedback
            st.rerun()
        else:
            st.error("Please provide an answer before submitting!")


def display_answer_feedback():
    """Display feedback for the last submitted answer."""
    if 'last_answer_result' not in st.session_state:
        return False
    
    answer_info = st.session_state.last_answer_result
    if not answer_info.get('processed', False):
        return False
    
    is_correct = answer_info['is_correct']
    result = answer_info['result']
    session = st.session_state.story_session
    
    # Show feedback
    if is_correct:
        st.markdown(f'''
        <div style="
            background: #d4edda;
            padding: 1.5rem;
            border-radius: 10px;
            color: #155724;
            font-weight: bold;
            text-align: center;
            margin: 1rem 0;
            border: 2px solid #28a745;
        ">
            🎉 Excellent work, {session.child_name}! You got it right! 🌟
        </div>
        ''', unsafe_allow_html=True)
        st.balloons()
    else:
        st.info(f"Good try, {session.child_name}! The answer was: **{result.correct_answer}**")
        st.markdown("🌟 Don't worry - learning is about trying your best!")
    
    # Show explanation
    st.markdown("### 📚 Learning Moment")
    st.markdown(result.explanation)
    
    # Difficulty adjustment info is now only shown to parents in the detailed results section
    
    # Continue or complete button
    if session.is_complete():
        st.success("🎆 Adventure Complete! Scroll down to see your results!")
        # Clear feedback state
        del st.session_state.last_answer_result
        return True
    else:
        st.markdown("")
        questions_answered = len(session.question_results)
        if st.button("🚀 Continue to Next Part! 🚀", type="primary", use_container_width=True, key=f"continue_q{questions_answered}"):
            # Clear feedback state and continue
            del st.session_state.last_answer_result
            st.rerun()
    
    return True


def display_story_completion(session: StorySession):
    """Display completion screen with results and achievements."""
    st.markdown("### 🎊 Adventure Complete! 🎊")
    
    # Success metrics
    success_rate = session.get_success_rate()
    correct_count = sum(1 for result in session.question_results if result.is_correct)
    
    st.markdown(f'''
    <div style="
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 2rem;
        border-radius: 15px;
        color: #155724;
        text-align: center;
        margin: 1rem 0;
        border: 2px solid #28a745;
        box-shadow: 0 8px 32px rgba(40, 167, 69, 0.3);
    ">
        <h2 style="color: #155724; margin-bottom: 1rem;">🏆 Congratulations, {session.child_name}! 🏆</h2>
        <p style="font-size: 1.2rem; color: #155724;">
            You completed your {session.theme} adventure!<br>
            You got {correct_count}/3 questions right ({int(success_rate * 100)}%)
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Achievement badges based on performance
    st.markdown("### 🏅 Your Adventure Badges:")
    badge_col1, badge_col2, badge_col3 = st.columns(3)
    
    with badge_col1:
        st.markdown("⭐ **Adventure Hero**")
        st.markdown("*Completed the full quest*")
    
    with badge_col2:
        if success_rate >= 0.67:
            st.markdown("🧠 **Smart Thinker**")
            st.markdown("*Answered most questions correctly*")
        else:
            st.markdown("💪 **Brave Learner**")
            st.markdown("*Tried your best on every question*")
    
    with badge_col3:
        if any(result.difficulty_level == DifficultyLevel.HARD for result in session.question_results):
            st.markdown("🚀 **Challenge Master**")
            st.markdown("*Tackled hard questions*")
        else:
            st.markdown("🌟 **Growing Explorer**")
            st.markdown("*Building skills step by step*")


def create_new_story_session():
    """Create a new multi-question story session."""
    if ('theme' in st.session_state and 'child_name' in st.session_state and 
        'learning_focus' in st.session_state and 'multi_story_generator' in st.session_state):
        
        # Create new session
        session = st.session_state.multi_story_generator.create_story_session(
            st.session_state.child_name,
            st.session_state.theme,
            st.session_state.learning_focus
        )
        
        st.session_state.story_session = session
        st.session_state.waiting_for_answer = False
        st.session_state.current_question_start_time = time.time()
        
        return True
    return False


def main():
    st.set_page_config(
        page_title="Ainia Adventure Stories - Enhanced",
        page_icon="🏰",
        layout="centered"
    )
    
    # Custom CSS for enhanced interface
    st.markdown("""
    <style>
    /* Main app styling */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Header styling */
    h1 {
        color: #FF6B6B !important;
        font-family: 'Comic Sans MS', cursive, sans-serif !important;
        text-align: center !important;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Enhanced progress styling */
    .progress-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        color: white;
        text-align: center;
    }
    
    /* Story content styling */
    .story-content {
        background: linear-gradient(135deg, #FFF9E6, #F0F8FF) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        border: 3px solid #FFE66D !important;
        margin: 1rem 0 !important;
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
    }
    
    /* Adventure header */
    .adventure-header {
        color: #FF6B6B !important;
        font-family: 'Comic Sans MS', cursive, sans-serif !important;
        text-align: center !important;
        font-size: 2rem !important;
        margin: 1rem 0 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #FFE66D) !important;
        border: none !important;
        border-radius: 20px !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        padding: 0.75rem 1.5rem !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(45deg, #4ECDC4, #45B7B8) !important;
        font-size: 1.4rem !important;
        padding: 1rem 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1>🏰 Ainia Adventure Stories!</h1>', unsafe_allow_html=True)
    st.markdown('<h3>✨ Create your own magical adventure story! ✨</h3>', unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        st.error("🔑 **API Key Missing!** Please set up your OpenAI API key to continue.")
        st.stop()
    
    # Initialize managers
    tts_manager = TextToSpeechManager()
    drawing_canvas = DrawingCanvas()
    
    # Check if we have an active story session (including completed ones)
    if st.session_state.story_session is not None:
        session = st.session_state.story_session
        
        # Display progress indicator
        display_progress_indicator(session)
        
        # Display completed parts with their Q&A
        if session.question_results:
            display_completed_parts_with_qa(session, tts_manager)
        
        # Use a consistent index based on answered questions
        questions_answered = len(session.question_results)
        questions_generated = len(session.questions)
        
        # Check if we need to generate the next part
        if questions_answered < 3 and questions_generated <= questions_answered:
            with st.spinner(f"🪄 Creating part {questions_answered + 1} of your adventure..."):
                story_part, question_data, explanation = st.session_state.multi_story_generator.generate_next_story_part(session)
                
                # Add to session
                session.story_parts.append(story_part)
                session.questions.append(question_data)
                
                st.session_state.current_question_start_time = time.time()
                st.session_state.waiting_for_answer = True
                st.rerun()
        
        # Check if we should show feedback first
        showing_feedback = display_answer_feedback()
        
        # Display current story part and question if we have one and haven't answered it yet and not showing feedback
        if not showing_feedback and questions_answered < len(session.questions) and questions_answered < 3:
            # Show the current story part
            display_current_story_part(session, tts_manager)
            # Show the question for the current part
            current_question_data = session.questions[questions_answered]
            display_question_section(session, current_question_data)
        
        # Check if story is complete
        if session.is_complete():
            display_story_completion(session)
            
            # Drawing Canvas Section (only after completion)
            st.markdown("")
            st.markdown('<div class="adventure-header">🎨 Draw Your Adventure! 🎨</div>', unsafe_allow_html=True)
            
            # Create drawing prompt based on theme and child name
            child_name_canvas = session.child_name
            theme = session.theme
            drawing_prompt = f"Draw your favorite scene from {child_name_canvas}'s complete {theme} adventure!"
            
            # Drawing canvas with styled container
            st.markdown(f'''
            <div style="
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                padding: 2rem;
                border-radius: 20px;
                color: white;
                margin: 1rem 0;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            ">
                <h2 style="color: white; margin-bottom: 1rem; text-align: center; font-size: 2rem;">
                    ✏️ Time to Create Your Masterpiece! ✏️
                </h2>
            </div>
            ''', unsafe_allow_html=True)
            
            # Create the drawing canvas
            child_drawing = drawing_canvas.create_drawing_canvas(drawing_prompt, width=600, height=400)
            
            # Save artwork button
            if child_drawing is not None:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("💾 Save My Amazing Artwork! 💾", use_container_width=True, key="save_artwork"):
                        filepath = drawing_canvas.save_child_artwork(child_drawing, child_name_canvas, theme)
                        if filepath:
                            st.success(f"🎉 Your incredible artwork has been saved! You're such a talented artist, {child_name_canvas}! 🎨")
                            st.balloons()
                            # Show a preview of the saved image
                            st.image(child_drawing, caption=f"{child_name_canvas}'s {theme} Adventure Art", use_container_width=True)
                        else:
                            st.error("😔 Oops! We couldn't save your artwork right now. But it looks amazing!")
            
            st.markdown("") # Spacer
            
            # Show detailed results for parents
            with st.expander("📊 Detailed Results (For Parents)", expanded=False):
                st.markdown("### Question-by-Question Results:")
                for i, result in enumerate(session.question_results, 1):
                    status_icon = "✅" if result.is_correct else "❌"
                    difficulty_icon = {"EASY": "🟢", "MEDIUM": "🟡", "HARD": "🔴"}.get(result.difficulty_level.name, "🟢")
                    
                    st.markdown(f"""
                    **Question {i}:** {status_icon} {difficulty_icon}
                    - **Difficulty:** {result.difficulty_level.name.title()}
                    - **Question:** {result.question_text[:100]}...
                    - **Child's Answer:** {result.user_answer}
                    - **Correct Answer:** {result.correct_answer}
                    - **Response Time:** {result.response_time:.1f}s
                    """)
                
                # Show adaptive difficulty information for parents
                st.markdown("---")
                st.markdown("### 🎯 Adaptive Difficulty System:")
                st.markdown("""
                The system automatically adjusts question difficulty based on your child's performance:
                - **Correct answer** → Next question becomes slightly harder to encourage growth
                - **Incorrect answer** → Next question becomes slightly easier to build confidence
                - **Final difficulty level:** Represents your child's appropriate challenge level
                """)
                
                if len(session.question_results) > 1:
                    st.markdown("### 📈 Difficulty Progression:")
                    difficulty_progression = []
                    for i, result in enumerate(session.question_results):
                        difficulty_progression.append(f"Q{i+1}: {result.difficulty_level.name}")
                    st.markdown(" → ".join(difficulty_progression))
            
            # Reset button
            st.markdown("")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🎠 Start Another Adventure! 🎠", use_container_width=True):
                    # Clear session state for new adventure
                    st.session_state.story_session = None
                    if 'theme' in st.session_state:
                        del st.session_state.theme
                    if 'last_answer_result' in st.session_state:
                        del st.session_state.last_answer_result
                    st.rerun()
    
    else:
        # Story setup interface
        st.markdown('<div class="adventure-header">🎭 Choose Your Adventure! 🎭</div>', unsafe_allow_html=True)
        
        # Theme selection
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🐉 DRAGONS\n\nFly with magical dragons!", use_container_width=True, key="dragon_btn"):
                st.session_state.theme = "dragons"
                st.success("🐉 Dragons chosen! Get ready for an epic quest!")
                time.sleep(0.5)
        
        with col2:
            if st.button("🏴‍☠️ PIRATES\n\nSail the seven seas!", use_container_width=True, key="pirate_btn"):
                st.session_state.theme = "pirates"
                st.success("🏴‍☠️ Pirates chosen! Adventure on the high seas awaits!")
                time.sleep(0.5)
        
        with col3:
            if st.button("👑 PRINCESSES\n\nRule a magical kingdom!", use_container_width=True, key="princess_btn"):
                st.session_state.theme = "princesses"
                st.success("👑 Princesses chosen! Your royal adventure begins!")
                time.sleep(0.5)
        
        # Character setup
        st.markdown("")
        st.markdown('<div class="adventure-header">👋 Tell Us About You! 👋</div>', unsafe_allow_html=True)
        
        child_name = st.text_input(
            "🌟 What's your name, brave adventurer?",
            placeholder="Type your awesome name here!",
            help="This will make your story extra special and personal!"
        )
        
        learning_focus = st.selectbox(
            "🎯 What exciting skill do you want to practice today?",
            ["🔢 counting and addition", "📚 vocabulary", "🧩 problem solving"],
            help="Don't worry - learning will be fun and feel like part of your adventure!"
        )
        
        # Start adventure button
        st.markdown("")
        if st.button("🚀 Begin My Adventure! 🚀", type="primary", use_container_width=True):
            if not child_name:
                st.error("🙋‍♀️ Please tell us your name first!")
            elif 'theme' not in st.session_state:
                st.error("🎭 Don't forget to pick your favorite adventure theme!")
            else:
                # Store session data
                st.session_state.child_name = child_name
                st.session_state.learning_focus = learning_focus
                
                # Create new story session
                if create_new_story_session():
                    st.balloons()
                    st.success(f"🎉 Amazing! Your adventure is starting, {child_name}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("😔 Something went wrong starting your adventure. Please try again!")
        
        # Instructions for new users
        if 'theme' not in st.session_state:
            st.markdown("")
            st.markdown('<div class="adventure-header">✨ What Makes This Special? ✨</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **🎯 Your Own Story**
                - Adventure story created just for you
                - Each part builds on the previous one
                - Complete adventure with beginning, middle, and end
                """)
            with col2:
                st.markdown("""
                **🧠 Fun Learning**
                - Answer questions to continue your story
                - Learn while you play
                - Perfect mix of adventure and education!
                """)
            
            st.info("🌟 **Ready for a personalized adventure?** Choose your theme above to begin!")


if __name__ == "__main__":
    main()