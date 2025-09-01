"""Multi-modal enhanced Streamlit application for Ainia Adventure Stories - Phase 7."""

import streamlit as st
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Optional

# Import existing modules
from story_generator import StoryGenerator
from adaptive_system import AdaptiveSystemManager, ChildProfile, DifficultyLevel, LearningStyle
from emotion_branching import EmotionAdaptiveManager, EmotionState
from progress_reporter import ProgressReportGenerator

# Import new multi-modal system
from multimodal_system import MultiModalStoryExperience

# Load environment variables
load_dotenv()


class MultiModalAdventureApp:
    """Multi-modal Adventure Stories app with enhanced interactive features."""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("⚠️ OpenAI API key not found! Please check your .env file.")
            st.stop()
        
        self.story_generator = StoryGenerator(api_key)
        self.adaptive_manager = AdaptiveSystemManager()
        self.emotion_manager = EmotionAdaptiveManager()
        self.report_generator = ProgressReportGenerator()
        
        # Initialize multi-modal system
        self.multimodal_experience = MultiModalStoryExperience(api_key, self.story_generator)
        
        # Initialize session state
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if 'child_profile' not in st.session_state:
            st.session_state.child_profile = None
        if 'current_story' not in st.session_state:
            st.session_state.current_story = None
        if 'interaction_start_time' not in st.session_state:
            st.session_state.interaction_start_time = None
        if 'recommendations' not in st.session_state:
            st.session_state.recommendations = []
        if 'new_achievements' not in st.session_state:
            st.session_state.new_achievements = []
        if 'view_mode' not in st.session_state:
            st.session_state.view_mode = 'child'  # 'child' or 'parent'
        if 'multimodal_enabled' not in st.session_state:
            st.session_state.multimodal_enabled = True
    
    def run(self):
        """Main application entry point."""
        st.set_page_config(
            page_title="Ainia Adventure Stories - Multi-Modal",
            page_icon="🏰",
            layout="wide"
        )
        
        # Apply custom CSS
        self._apply_custom_css()
        
        # Main header with view toggle
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("# 🏰 Ainia Adventure Stories")
            st.markdown("### *Multi-Modal Learning Adventures*")
        
        with col3:
            self._render_view_toggle()
        
        # Multi-modal features toggle
        with st.sidebar:
            st.markdown("## 🎨 Experience Settings")
            st.session_state.multimodal_enabled = st.toggle(
                "🎵 Enable Multi-Modal Features", 
                value=st.session_state.multimodal_enabled,
                help="Includes voice, images, games, and drawing"
            )
        
        # Render appropriate view
        if st.session_state.view_mode == 'child':
            self._render_child_interface()
        else:
            self._render_parent_dashboard()
    
    def _apply_custom_css(self):
        """Apply enhanced custom CSS with multi-modal styling."""
        st.markdown("""
        <style>
        /* Multi-modal enhanced styling */
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
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        h3 {
            color: #4ECDC4 !important;
            font-family: 'Comic Sans MS', cursive, sans-serif !important;
            text-align: center !important;
        }
        
        /* Multi-modal containers */
        .audio-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 20px;
            color: white;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .image-container {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 1.5rem;
            border-radius: 20px;
            color: white;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .interactive-container {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 1.5rem;
            border-radius: 20px;
            color: white;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .drawing-container {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            padding: 1.5rem;
            border-radius: 20px;
            color: white;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        /* Enhanced button styling */
        .stButton > button {
            background: linear-gradient(45deg, #FF6B6B, #FFE66D) !important;
            border: none !important;
            border-radius: 25px !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 1.2rem !important;
            padding: 0.75rem 2rem !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
        }
        
        /* Voice selection styling */
        .voice-selector {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Interactive game styling */
        .game-container {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 2rem;
            border-radius: 20px;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        /* Drawing canvas styling */
        .canvas-container {
            border: 3px solid #FFE66D;
            border-radius: 15px;
            padding: 1rem;
            margin: 1rem 0;
            background: white;
        }
        
        /* Achievement animations */
        @keyframes bounce {
            0%, 20%, 60%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            80% { transform: translateY(-5px); }
        }
        
        .achievement-bounce {
            animation: bounce 1s ease-in-out;
        }
        
        /* Vocabulary card styling */
        .vocab-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 15px;
            color: white;
            margin: 0.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .vocab-card:hover {
            transform: scale(1.05);
        }
        
        /* Story display enhancements */
        .story-display {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            font-size: 1.2rem;
            line-height: 1.8;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        /* Progress indicators */
        .multimodal-progress {
            background: linear-gradient(90deg, #4ECDC4, #44A08D);
            height: 10px;
            border-radius: 5px;
            transition: width 0.8s ease;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding-left: 20px;
            padding-right: 20px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            color: #4ECDC4;
            font-weight: bold;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(45deg, #4ECDC4, #44A08D);
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def _render_view_toggle(self):
        """Render parent/child view toggle."""
        view_options = ["👶 Child Experience", "👨‍👩‍👧‍👦 Parent Dashboard"]
        current_index = 0 if st.session_state.view_mode == 'child' else 1
        
        selected = st.selectbox(
            "",
            view_options,
            index=current_index,
            key="view_selector",
            label_visibility="collapsed"
        )
        
        st.session_state.view_mode = 'child' if selected.startswith('👶') else 'parent'
    
    def _render_child_interface(self):
        """Render the enhanced multi-modal child interface."""
        # Profile setup
        if not st.session_state.child_profile:
            self._render_profile_setup()
            return
        
        profile = st.session_state.child_profile
        
        # Welcome message with audio option
        st.markdown(f"## 🌟 Welcome back, {profile.name}!")
        
        if st.session_state.multimodal_enabled:
            if st.button("🔊 Hear Your Welcome", key="welcome_audio"):
                welcome_text = f"Hello {profile.name}! Ready for another magical adventure?"
                self.multimodal_experience.tts_manager.create_audio_player(welcome_text)
        
        # Display achievements
        self._render_achievement_celebrations()
        
        # Theme selection with enhanced visuals
        self._render_enhanced_theme_selection()
        
        # Story generation and display
        if st.session_state.current_story:
            self._render_multimodal_story_experience()
    
    def _render_profile_setup(self):
        """Render profile setup with multi-modal enhancements."""
        st.markdown("## 🎭 Let's Create Your Adventure Profile!")
        
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("What's your name, young adventurer? 🌟", 
                                   placeholder="Enter your name here...")
                age = st.slider("How old are you?", 3, 12, 7)
                
            with col2:
                learning_style_options = {
                    "🎨 Visual Learner": LearningStyle.VISUAL,
                    "🎵 Audio Learner": LearningStyle.AUDITORY, 
                    "🤹 Hands-on Learner": LearningStyle.KINESTHETIC
                }
                
                learning_style_label = st.selectbox(
                    "How do you like to learn best?",
                    list(learning_style_options.keys())
                )
                learning_style = learning_style_options[learning_style_label]
            
            interests = st.multiselect(
                "What do you love? ❤️",
                ["🐉 Dragons", "🏰 Castles", "🧙‍♂️ Magic", "🦸‍♀️ Heroes", 
                 "🌟 Adventure", "📚 Books", "🎨 Art", "🎵 Music"]
            )
            
            if name and st.button("✨ Create My Adventure Profile!", key="create_profile"):
                # Create profile
                profile = ChildProfile(
                    name=name,
                    age=age,
                    learning_style=learning_style,
                    preferred_themes=interests,
                    difficulty_level=DifficultyLevel.INTERMEDIATE
                )
                
                st.session_state.child_profile = profile
                
                # Welcome audio if multi-modal enabled
                if st.session_state.multimodal_enabled:
                    welcome_text = f"Welcome to Ainia Adventures, {name}! I'm so excited to create magical stories just for you!"
                    self.multimodal_experience.tts_manager.create_audio_player(welcome_text)
                
                st.success(f"🎉 Welcome to your adventure world, {name}!")
                st.balloons()
                time.sleep(2)
                st.rerun()
    
    def _render_enhanced_theme_selection(self):
        """Render theme selection with multi-modal enhancements."""
        if st.session_state.current_story:
            return
        
        st.markdown("## 🌈 Choose Your Adventure Theme!")
        
        themes = {
            "🐉 Dragons": {
                "emoji": "🐉",
                "description": "Magical dragon adventures with treasure and friendship!",
                "color": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
            },
            "🏴‍☠️ Pirates": {
                "emoji": "🏴‍☠️", 
                "description": "High seas adventures with treasure maps and brave crews!",
                "color": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
            },
            "👸 Princesses": {
                "emoji": "👸",
                "description": "Royal adventures with castles, kindness, and magic!",
                "color": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
            },
            "🧙‍♂️ Wizards": {
                "emoji": "🧙‍♂️",
                "description": "Magical spells, enchanted forests, and wisdom quests!",
                "color": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
            }
        }
        
        # Create theme buttons
        cols = st.columns(2)
        for i, (theme_name, theme_data) in enumerate(themes.items()):
            with cols[i % 2]:
                if st.button(
                    f"{theme_data['emoji']} {theme_name.split(' ')[1]}",
                    key=f"theme_{theme_name}",
                    help=theme_data['description']
                ):
                    self._start_adventure(theme_name, theme_data)
        
        # Audio previews if multi-modal enabled
        if st.session_state.multimodal_enabled:
            st.markdown("### 🎧 Preview Theme Descriptions")
            for theme_name, theme_data in themes.items():
                if st.button(f"🔊 Hear about {theme_name}", key=f"preview_{theme_name}"):
                    self.multimodal_experience.tts_manager.create_audio_player(theme_data['description'])
    
    def _start_adventure(self, theme: str, theme_data: Dict):
        """Start a new adventure with the selected theme."""
        profile = st.session_state.child_profile
        st.session_state.interaction_start_time = time.time()
        
        with st.spinner("🎭 Creating your magical adventure..."):
            # Generate story using adaptive system
            story_result = self.adaptive_manager.generate_adaptive_story(
                child_profile=profile,
                theme=theme,
                story_generator=self.story_generator
            )
            
            if story_result:
                st.session_state.current_story = {
                    **story_result,
                    'theme': theme,
                    'theme_data': theme_data,
                    'generated_at': datetime.now().isoformat()
                }
                st.success("🎉 Your adventure is ready!")
                st.rerun()
    
    def _render_multimodal_story_experience(self):
        """Render the complete multi-modal story experience."""
        story_data = st.session_state.current_story
        theme = story_data['theme']
        profile = st.session_state.child_profile
        
        # Story header with restart option
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"## 📚 {profile.name}'s {theme.split(' ')[1]} Adventure")
        with col2:
            if st.button("🔄 New Adventure", key="restart_adventure"):
                st.session_state.current_story = None
                st.rerun()
        
        # Multi-modal story display
        if st.session_state.multimodal_enabled:
            self.multimodal_experience.create_enhanced_story_display(
                story_data, theme, profile.name
            )
        else:
            # Fallback to simple story display
            self._render_simple_story_display(story_data)
        
        # Learning assessment
        self._render_learning_assessment(story_data)
    
    def _render_simple_story_display(self, story_data: Dict):
        """Render simple story display when multi-modal is disabled."""
        story_text = story_data.get('story', '')
        
        st.markdown("### 📖 Your Adventure Story")
        st.markdown(f"""
        <div class="story-display">
        {story_text}
        </div>
        """, unsafe_allow_html=True)
    
    def _render_learning_assessment(self, story_data: Dict):
        """Render learning assessment and questions."""
        st.markdown("### 🧠 Learning Time!")
        
        learning_problem = story_data.get('learning_problem', {})
        if learning_problem:
            st.markdown(f"**Challenge:** {learning_problem.get('question', '')}")
            
            # Create input based on problem type
            problem_type = learning_problem.get('type', 'math')
            
            if problem_type == 'math':
                user_answer = st.number_input(
                    "Your answer:",
                    min_value=0,
                    max_value=100,
                    key="math_answer"
                )
            else:
                user_answer = st.text_input(
                    "Your answer:",
                    key="text_answer"
                )
            
            if st.button("✅ Check My Answer!", key="check_answer"):
                correct_answer = learning_problem.get('answer')
                
                if str(user_answer).lower().strip() == str(correct_answer).lower().strip():
                    st.success("🎉 Excellent work! You're so smart!")
                    st.balloons()
                    
                    # Audio celebration if enabled
                    if st.session_state.multimodal_enabled:
                        celebration_text = f"Fantastic job, {st.session_state.child_profile.name}! You got it right!"
                        self.multimodal_experience.tts_manager.create_audio_player(celebration_text)
                    
                    # Record success for adaptive system
                    self._record_learning_success()
                else:
                    st.info(f"Good try! The answer was: {correct_answer}")
                    hint = learning_problem.get('hint', '')
                    if hint:
                        st.markdown(f"💡 **Hint:** {hint}")
    
    def _record_learning_success(self):
        """Record learning success for adaptive system."""
        profile = st.session_state.child_profile
        if profile:
            # Update profile stats (simplified)
            profile.learning_metrics.success_rate = min(1.0, profile.learning_metrics.success_rate + 0.1)
            
            # Add interaction to history
            interaction = {
                'timestamp': time.time(),
                'correct': True,
                'response_time': 5.0,  # placeholder
                'engagement': 0.8  # placeholder
            }
            profile.interaction_history.append(interaction)
    
    def _render_achievement_celebrations(self):
        """Render achievement celebrations."""
        if st.session_state.new_achievements:
            for achievement in st.session_state.new_achievements:
                st.markdown(f"""
                <div class="achievement-badge achievement-bounce">
                    🏆 New Achievement: {achievement}
                </div>
                """, unsafe_allow_html=True)
            
            # Audio celebration if enabled
            if st.session_state.multimodal_enabled:
                achievement_text = f"Congratulations! You earned: {', '.join(st.session_state.new_achievements)}"
                self.multimodal_experience.tts_manager.create_audio_player(achievement_text)
            
            st.session_state.new_achievements = []
    
    def _render_parent_dashboard(self):
        """Render comprehensive parent dashboard."""
        st.markdown("## 👨‍👩‍👧‍👦 Parent Dashboard")
        
        if not st.session_state.child_profile:
            st.info("👶 Please create a child profile first by switching to Child Experience.")
            return
        
        profile = st.session_state.child_profile
        
        # Profile overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("👶 Child", profile.name)
            st.metric("🎂 Age", f"{profile.age} years")
            
        with col2:
            st.metric("🧠 Learning Style", profile.learning_style.value)
            st.metric("📊 Success Rate", f"{profile.learning_metrics.success_rate:.1%}")
            
        with col3:
            st.metric("🎯 Interactions", len(profile.interaction_history))
            st.metric("⭐ Current Level", profile.difficulty_level.value)
        
        # Multi-modal features usage
        if st.session_state.multimodal_enabled:
            st.markdown("### 🎨 Multi-Modal Features Active")
            st.success("✅ Voice narration, visual illustrations, interactive games, and drawing canvas are enabled")
        else:
            st.markdown("### 📝 Text-Only Mode")
            st.info("Enable multi-modal features in the sidebar for enhanced experience")
        
        # Current story analysis
        if st.session_state.current_story:
            st.markdown("### 📚 Current Story Analysis")
            story_data = st.session_state.current_story
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Theme:** {story_data['theme']}")
                st.write(f"**Generated:** {story_data['generated_at']}")
                st.write(f"**Learning Focus:** {story_data.get('learning_problem', {}).get('type', 'N/A')}")
            
            with col2:
                if 'vocabulary_words' in story_data:
                    st.write("**New Vocabulary:**")
                    for word in story_data['vocabulary_words']:
                        st.write(f"• {word}")
        
        # Generate progress report
        if st.button("📊 Generate Progress Report", key="generate_report"):
            self._generate_parent_report()
    
    def _generate_parent_report(self):
        """Generate comprehensive parent report."""
        profile = st.session_state.child_profile
        
        st.markdown("### 📋 Progress Report")
        
        report_data = {
            'child_name': profile.name,
            'age': profile.age,
            'learning_style': profile.learning_style.value,
            'success_rate': profile.learning_metrics.success_rate,
            'interactions': len(profile.interaction_history),
            'preferred_themes': profile.preferred_themes,
            'multimodal_enabled': st.session_state.multimodal_enabled
        }
        
        st.json(report_data)
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        success_rate = profile.learning_metrics.success_rate
        if success_rate > 0.8:
            st.success("🌟 Excellent progress! Consider increasing difficulty level.")
        elif success_rate < 0.5:
            st.info("💪 Building confidence. Continue with current level and provide extra encouragement.")
        else:
            st.success("📈 Good steady progress! Keep up the great work.")


def main():
    """Main application entry point."""
    app = MultiModalAdventureApp()
    app.run()


if __name__ == "__main__":
    main()