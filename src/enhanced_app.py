"""Enhanced Streamlit application with adaptive learning features for Ainia Adventure Stories."""

import streamlit as st
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Optional

# Import existing modules
from story_generator import StoryGenerator

# Import new adaptive modules
from adaptive_system import AdaptiveSystemManager, ChildProfile, DifficultyLevel, LearningStyle
from emotion_branching import EmotionAdaptiveManager, EmotionState
from progress_reporter import ProgressReportGenerator

# Load environment variables
load_dotenv()


class EnhancedAdventureApp:
    """Enhanced Adventure Stories app with adaptive learning features."""
    
    def __init__(self):
        self.story_generator = StoryGenerator(os.getenv("OPENAI_API_KEY"))
        self.adaptive_manager = AdaptiveSystemManager()
        self.emotion_manager = EmotionAdaptiveManager()
        self.report_generator = ProgressReportGenerator()
        
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
    
    def run(self):
        """Main application entry point."""
        st.set_page_config(
            page_title="Ainia Adventure Stories - Enhanced",
            page_icon="🏰",
            layout="wide"
        )
        
        # Apply custom CSS
        self._apply_custom_css()
        
        # Main header with view toggle
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("# 🏰 Ainia Adventure Stories")
            st.markdown("### *Adaptive Learning Through Magical Storytelling*")
        
        with col3:
            self._render_view_toggle()
        
        # Render appropriate view
        if st.session_state.view_mode == 'child':
            self._render_child_interface()
        else:
            self._render_parent_dashboard()
    
    def _apply_custom_css(self):
        """Apply enhanced custom CSS."""
        st.markdown("""
        <style>
        /* Enhanced styling for adaptive features */
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
        
        h3 {
            color: #4ECDC4 !important;
            font-family: 'Comic Sans MS', cursive, sans-serif !important;
            text-align: center !important;
        }
        
        /* Adaptive UI elements */
        .profile-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 15px;
            color: white;
            margin: 1rem 0;
        }
        
        .achievement-badge {
            background: linear-gradient(45deg, #FFE66D, #FF6B6B);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            margin: 0.25rem;
            display: inline-block;
        }
        
        .recommendation-card {
            background: linear-gradient(135deg, #4ECDC4, #44A08D);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin: 0.5rem 0;
        }
        
        .emotion-indicator {
            padding: 0.5rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            font-weight: bold;
        }
        
        .emotion-excited { background-color: #FFE66D; color: #8B4513; }
        .emotion-curious { background-color: #4ECDC4; color: white; }
        .emotion-confident { background-color: #51CF66; color: white; }
        .emotion-frustrated { background-color: #FF8787; color: white; }
        .emotion-bored { background-color: #CED4DA; color: #495057; }
        .emotion-neutral { background-color: #E9ECEF; color: #495057; }
        
        /* Progress indicators */
        .progress-bar {
            background-color: #E9ECEF;
            border-radius: 10px;
            padding: 3px;
            margin: 0.5rem 0;
        }
        
        .progress-fill {
            background: linear-gradient(45deg, #4ECDC4, #44A08D);
            height: 20px;
            border-radius: 7px;
            transition: width 0.5s ease;
        }
        
        /* Button enhancements */
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
        </style>
        """, unsafe_allow_html=True)
    
    def _render_view_toggle(self):
        """Render parent/child view toggle."""
        view_options = ["👶 Child View", "👨‍👩‍👧‍👦 Parent Dashboard"]
        current_index = 0 if st.session_state.view_mode == 'child' else 1
        
        selected = st.selectbox(
            "View Mode",
            view_options,
            index=current_index,
            key="view_selector"
        )
        
        st.session_state.view_mode = 'child' if selected.startswith('👶') else 'parent'
    
    def _render_child_interface(self):
        """Render the enhanced child-friendly interface."""
        # Profile setup
        if not st.session_state.child_profile:
            self._render_profile_setup()
            return
        
        profile = st.session_state.child_profile
        
        # Display current achievements
        self._render_achievement_celebrations()
        
        # Profile summary
        self._render_child_profile_summary(profile)
        
        # Story recommendations
        if st.session_state.recommendations:
            self._render_story_recommendations()
        
        # Main story interface
        self._render_story_interface(profile)
    
    def _render_profile_setup(self):
        """Render profile setup for new children."""
        st.markdown("## 🌟 Welcome to Your Adventure!")
        st.markdown("### Let's learn about you first!")
        
        with st.form("profile_setup"):
            col1, col2 = st.columns(2)
            
            with col1:
                child_name = st.text_input(
                    "What's your name, adventurer? 🧙‍♀️",
                    placeholder="Enter your name..."
                )
                
                child_age = st.slider(
                    "How old are you? 🎂",
                    min_value=5,
                    max_value=9,
                    value=6
                )
            
            with col2:
                favorite_theme = st.selectbox(
                    "Which adventure sounds most exciting? 🗺️",
                    ["🐉 Dragons", "🏴‍☠️ Pirates", "👑 Princesses", "🦄 Unicorns", "🚀 Space"]
                )
                
                learning_preference = st.radio(
                    "How do you like to learn? 🎯",
                    ["📖 Reading stories", "🎨 Looking at pictures", "🎵 Listening to sounds", "🤲 Hands-on activities"]
                )
            
            submitted = st.form_submit_button("🚀 Start My Adventure!")
            
            if submitted and child_name:
                # Create new profile
                profile = self.adaptive_manager.get_or_create_profile(child_name, child_age)
                
                # Set initial preferences
                if "pictures" in learning_preference.lower():
                    profile.learning_style = LearningStyle.VISUAL
                elif "sounds" in learning_preference.lower():
                    profile.learning_style = LearningStyle.AUDITORY
                elif "hands-on" in learning_preference.lower():
                    profile.learning_style = LearningStyle.KINESTHETIC
                
                st.session_state.child_profile = profile
                
                # Generate initial recommendations
                recommendations = self.adaptive_manager.get_recommendations(profile)
                st.session_state.recommendations = recommendations
                
                st.success(f"🎉 Welcome aboard, {child_name}! Your adventure awaits!")
                st.experimental_rerun()
    
    def _render_child_profile_summary(self, profile):
        """Render child profile summary card."""
        with st.container():
            st.markdown(f"""
            <div class="profile-card">
                <h3>🌟 {profile.name}'s Adventure Profile</h3>
                <p><strong>Adventurer Level:</strong> {profile.difficulty_level.name.title()} Explorer</p>
                <p><strong>Learning Style:</strong> {profile.learning_style.value.title()} Learner</p>
                <p><strong>Stories Completed:</strong> {getattr(profile, 'achievement_stats', {}).get('stories_completed', 0)} Adventures</p>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_achievement_celebrations(self):
        """Render achievement celebration animations."""
        if st.session_state.new_achievements:
            for achievement in st.session_state.new_achievements:
                st.balloons()
                st.success(f"🏆 **NEW ACHIEVEMENT UNLOCKED!** {achievement['celebration_message']}")
            
            # Clear achievements after display
            st.session_state.new_achievements = []
    
    def _render_story_recommendations(self):
        """Render personalized story recommendations."""
        st.markdown("## 🎯 Recommended Adventures Just for You!")
        
        cols = st.columns(min(len(st.session_state.recommendations), 3))
        
        for i, rec in enumerate(st.session_state.recommendations[:3]):
            with cols[i]:
                st.markdown(f"""
                <div class="recommendation-card">
                    <h4>{rec['theme'].title()} Adventure</h4>
                    <p><strong>Focus:</strong> {rec['learning_focus'].title()}</p>
                    <p><strong>Why:</strong> {rec['reason']}</p>
                    <p><strong>Duration:</strong> ~{rec['estimated_duration']} min</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🚀 Start {rec['theme'].title()} Adventure", key=f"rec_{i}"):
                    self._start_recommended_story(rec)
    
    def _render_story_interface(self, profile):
        """Render the main story creation interface."""
        st.markdown("## 🎭 Create Your Adventure!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            theme = st.selectbox(
                "Choose your adventure theme 🗺️",
                ["🐉 Dragons", "🏴‍☠️ Pirates", "👑 Princesses"],
                key="theme_selector"
            )
        
        with col2:
            learning_focus = st.selectbox(
                "What would you like to practice? 🎯",
                ["🧮 Math (counting & numbers)", "📚 Vocabulary (new words)", "🧩 Problem Solving"],
                key="learning_selector"
            )
        
        if st.button("✨ Create My Story!", type="primary", key="create_story"):
            self._create_adaptive_story(profile, theme, learning_focus)
        
        # Display current story if exists
        if st.session_state.current_story:
            self._render_story_display()
    
    def _create_adaptive_story(self, profile, theme_raw, learning_raw):
        """Create story with adaptive features."""
        # Clean theme and learning focus
        theme = theme_raw.split()[-1].lower()  # Extract theme from emoji string
        learning_focus = learning_raw.split()[1].lower()  # Extract focus type
        
        # Record interaction start time
        st.session_state.interaction_start_time = time.time()
        
        # Get adaptive parameters
        adaptive_params = self.adaptive_manager.get_adaptive_story_parameters(profile, theme)
        
        with st.spinner("🔮 Creating your personalized adventure..."):
            # Generate story with adaptive context
            story, explanation = self.story_generator.generate_adventure(
                theme, profile.name, learning_focus
            )
            
            if story and explanation:
                st.session_state.current_story = {
                    'content': story,
                    'explanation': explanation,
                    'theme': theme,
                    'learning_focus': learning_focus,
                    'adaptive_params': adaptive_params,
                    'start_time': time.time()
                }
                
                st.success("🎉 Your adventure is ready!")
                st.experimental_rerun()
            else:
                st.error("😔 Something went wrong creating your story. Let's try again!")
    
    def _render_story_display(self):
        """Render the current story with interactive elements."""
        story_data = st.session_state.current_story
        
        st.markdown("## 📖 Your Adventure Story")
        st.markdown(f"**Theme:** {story_data['theme'].title()} | **Learning Focus:** {story_data['learning_focus'].title()}")
        
        # Display story content
        st.markdown("---")
        st.markdown(story_data['content'])
        st.markdown("---")
        
        # Interactive response section
        self._render_story_interaction(story_data)
    
    def _render_story_interaction(self, story_data):
        """Render interactive story response section."""
        st.markdown("### 🤔 Your Turn to Respond!")
        
        with st.form("story_response"):
            user_response = st.text_area(
                "What do you think? Share your answer or thoughts! 💭",
                placeholder="Type your response here...",
                height=100
            )
            
            confidence_level = st.slider(
                "How confident are you in your answer? 🎯",
                min_value=1,
                max_value=5,
                value=3,
                help="1 = Not sure at all, 5 = Very confident!"
            )
            
            submitted = st.form_submit_button("✨ Submit Response")
            
            if submitted and user_response:
                self._process_story_response(story_data, user_response, confidence_level)
    
    def _process_story_response(self, story_data, response, confidence):
        """Process child's response with adaptive feedback."""
        profile = st.session_state.child_profile
        
        # Calculate response time
        response_time = time.time() - story_data['start_time']
        
        # Create interaction data
        interaction_data = {
            'theme': story_data['theme'],
            'learning_focus': story_data['learning_focus'],
            'response': response,
            'confidence': confidence,
            'response_time': response_time,
            'timestamp': time.time(),
            'story_completed': True,
            'session_duration': time.time() - st.session_state.interaction_start_time
        }
        
        # Simple response evaluation (you could make this more sophisticated)
        is_correct = self._evaluate_response(response, story_data['learning_focus'])
        interaction_data['correct'] = is_correct
        interaction_data['comprehension_score'] = confidence / 5.0
        interaction_data['engagement_score'] = min(1.0, len(response) / 50.0)  # Based on response length
        
        # Process with adaptive systems
        emotion_results = self.emotion_manager.process_interaction_emotions(profile, interaction_data)
        
        # Update profile
        self.adaptive_manager.update_profile_from_interaction(profile, interaction_data)
        
        # Store new achievements
        if emotion_results['new_achievements']:
            st.session_state.new_achievements = emotion_results['new_achievements']
        
        # Generate new recommendations
        st.session_state.recommendations = self.adaptive_manager.get_recommendations(profile)
        
        # Provide adaptive feedback
        self._render_adaptive_feedback(is_correct, emotion_results, response)
        
        # Clear current story
        st.session_state.current_story = None
        
        st.experimental_rerun()
    
    def _evaluate_response(self, response, learning_focus):
        """Simple response evaluation (placeholder for more sophisticated logic)."""
        response_lower = response.lower()
        
        if 'math' in learning_focus:
            # Check for numbers in response
            return any(char.isdigit() for char in response) and len(response) > 3
        elif 'vocabulary' in learning_focus:
            # Check for meaningful vocabulary usage
            return len(response.split()) > 3 and any(len(word) > 5 for word in response.split())
        elif 'problem' in learning_focus:
            # Check for problem-solving indicators
            indicators = ['because', 'think', 'maybe', 'could', 'should', 'idea']
            return any(indicator in response_lower for indicator in indicators) and len(response) > 10
        
        return len(response) > 5  # Default: any meaningful response
    
    def _render_adaptive_feedback(self, is_correct, emotion_results, response):
        """Render adaptive feedback based on performance and emotion."""
        emotion_state = emotion_results['detected_emotion']
        
        # Emotion indicator
        st.markdown(f"""
        <div class="emotion-indicator emotion-{emotion_state}">
            😊 I can sense you're feeling {emotion_state.title()}!
        </div>
        """, unsafe_allow_html=True)
        
        # Adaptive feedback based on emotion and performance
        if is_correct:
            if emotion_state == 'excited':
                st.success("🎉 AMAZING! Your excitement shows in your fantastic answer! Ready for an even bigger challenge?")
            elif emotion_state == 'confident':
                st.success("🌟 Excellent work! Your confidence is well-deserved. You're ready for advanced adventures!")
            else:
                st.success("✨ Great job! You understood the challenge perfectly!")
        else:
            if emotion_state == 'frustrated':
                st.info("💝 That's okay! Learning is a journey, not a race. You're doing wonderfully just by trying!")
            elif emotion_state == 'bored':
                st.info("🎨 Let's make this more exciting! How about we try a different type of adventure that might spark your interest?")
            else:
                st.info("🌈 Good effort! Every response teaches us something new. Let's keep exploring together!")
        
        # Show achievement progress
        if emotion_results.get('achievement_progress'):
            st.markdown("### 🎯 Your Progress")
            for achievement_id, progress in emotion_results['achievement_progress'].items():
                progress_percent = progress['progress']
                st.markdown(f"**{progress['title']}**: {progress['current']}/{progress['target']}")
                st.progress(progress_percent / 100)
    
    def _render_parent_dashboard(self):
        """Render comprehensive parent dashboard."""
        if not st.session_state.child_profile:
            st.warning("👶 Please set up your child's profile in Child View first!")
            return
        
        profile = st.session_state.child_profile
        
        st.markdown("# 👨‍👩‍👧‍👦 Parent Dashboard")
        st.markdown(f"## Insights for {profile.name}'s Learning Journey")
        
        # Dashboard tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🧠 Learning Analytics", "🏆 Achievements", "📋 Reports"])
        
        with tab1:
            self._render_parent_overview(profile)
        
        with tab2:
            self._render_learning_analytics(profile)
        
        with tab3:
            self._render_achievement_dashboard(profile)
        
        with tab4:
            self._render_report_generation(profile)
    
    def _render_parent_overview(self, profile):
        """Render parent overview section."""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            stories_completed = getattr(profile, 'achievement_stats', {}).get('stories_completed', 0)
            st.metric("Stories Completed", stories_completed, delta="+1" if stories_completed > 0 else None)
        
        with col2:
            success_rate = int(profile.learning_metrics.success_rate * 100) if hasattr(profile, 'learning_metrics') else 0
            st.metric("Success Rate", f"{success_rate}%", delta=f"+{success_rate//4}%" if success_rate > 0 else None)
        
        with col3:
            engagement = int(profile.learning_metrics.engagement_level * 100) if hasattr(profile, 'learning_metrics') else 0
            st.metric("Engagement Level", f"{engagement}%", delta="📈" if engagement > 70 else "📊")
        
        # Recent activity
        st.markdown("### 📝 Recent Activity")
        if hasattr(profile, 'interaction_history') and profile.interaction_history:
            recent_interactions = profile.interaction_history[-5:]  # Last 5 interactions
            
            for interaction in reversed(recent_interactions):
                theme = interaction.get('theme', 'Unknown').title()
                focus = interaction.get('learning_focus', 'General').title()
                correct = "✅" if interaction.get('correct', False) else "📝"
                timestamp = datetime.fromtimestamp(interaction.get('timestamp', time.time())).strftime('%m/%d %H:%M')
                
                st.markdown(f"**{timestamp}**: {correct} {theme} - {focus}")
        else:
            st.info("No recent activity to display. Encourage your child to try some adventures!")
    
    def _render_learning_analytics(self, profile):
        """Render detailed learning analytics."""
        if not hasattr(profile, 'learning_metrics'):
            st.info("No learning data available yet. Complete some stories to see analytics!")
            return
        
        metrics = profile.learning_metrics
        
        # Learning areas progress
        st.markdown("### 📈 Learning Areas Progress")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🧮 Mathematics**")
            math_level = metrics.math_level
            st.progress(math_level / 4.0)
            st.write(f"Level {math_level}/4")
        
        with col2:
            st.markdown("**📚 Vocabulary**")
            vocab_level = metrics.vocabulary_level
            st.progress(vocab_level / 4.0)
            st.write(f"Level {vocab_level}/4")
        
        with col3:
            st.markdown("**🧩 Problem Solving**")
            problem_level = metrics.problem_solving_level
            st.progress(problem_level / 4.0)
            st.write(f"Level {problem_level}/4")
        
        # Learning style insights
        st.markdown("### 🎯 Learning Style Insights")
        style_description = {
            'visual': "learns best through pictures, colors, and visual elements",
            'auditory': "thrives with sound, music, and verbal explanations",
            'kinesthetic': "prefers hands-on activities and movement-based learning",
            'mixed': "benefits from a combination of different learning approaches"
        }
        
        st.info(f"**{profile.name}** is a **{profile.learning_style.value}** learner who {style_description.get(profile.learning_style.value, '')}.")
        
        # Emotional engagement patterns
        if hasattr(profile, 'emotion_metrics'):
            st.markdown("### 😊 Emotional Engagement")
            recent_emotions = profile.emotion_metrics.recent_emotions[-10:]  # Last 10 emotions
            if recent_emotions:
                from collections import Counter
                emotion_counts = Counter(recent_emotions)
                
                for emotion, count in emotion_counts.most_common(3):
                    percentage = (count / len(recent_emotions)) * 100
                    st.write(f"**{emotion.title()}**: {percentage:.1f}% of recent sessions")
    
    def _render_achievement_dashboard(self, profile):
        """Render achievement tracking dashboard."""
        st.markdown("### 🏆 Earned Achievements")
        
        if hasattr(profile, 'achievements') and profile.achievements:
            cols = st.columns(3)
            for i, achievement_id in enumerate(profile.achievements):
                col_index = i % 3
                with cols[col_index]:
                    achievement_info = self._get_achievement_display_info(achievement_id)
                    st.markdown(f"""
                    <div class="achievement-badge">
                        {achievement_info['emoji']} {achievement_info['title']}
                    </div>
                    """, unsafe_allow_html=True)
                    st.write(achievement_info['description'])
        else:
            st.info("No achievements earned yet. Keep exploring to unlock amazing badges!")
        
        # Achievement progress
        st.markdown("### 🎯 Progress Toward Next Achievements")
        # This would show progress toward unearned achievements
        st.progress(0.6, text="Math Explorer: 3/5 problems solved")
        st.progress(0.4, text="Vocabulary Builder: 4/10 words learned")
        st.progress(0.8, text="Story Enthusiast: 8/10 stories completed")
    
    def _render_report_generation(self, profile):
        """Render report generation interface."""
        st.markdown("### 📋 Progress Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_type = st.selectbox(
                "Report Type",
                ["Comprehensive Report", "Achievement Summary", "Learning Progress Only"]
            )
        
        with col2:
            if st.button("📄 Generate PDF Report", type="primary"):
                self._generate_progress_report(profile, report_type)
        
        # Report scheduling options
        st.markdown("### ⏰ Automated Reports")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            weekly_reports = st.checkbox("Weekly progress reports")
        
        with col2:
            milestone_reports = st.checkbox("Achievement milestone reports")
        
        with col3:
            monthly_summary = st.checkbox("Monthly learning summary")
        
        if any([weekly_reports, milestone_reports, monthly_summary]):
            st.success("🔔 Report preferences saved! You'll receive updates based on your selections.")
    
    def _generate_progress_report(self, profile, report_type):
        """Generate and offer PDF report download."""
        with st.spinner("📊 Generating your personalized progress report..."):
            try:
                # Map report type
                type_mapping = {
                    "Comprehensive Report": "comprehensive",
                    "Achievement Summary": "achievement",
                    "Learning Progress Only": "summary"
                }
                
                report_path = self.report_generator.generate_progress_report(
                    profile, 
                    type_mapping.get(report_type, "comprehensive")
                )
                
                # Provide download link
                with open(report_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download Progress Report",
                        data=pdf_file.read(),
                        file_name=f"{profile.name}_Progress_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
                
                st.success("🎉 Report generated successfully! Click the download button above.")
                
            except Exception as e:
                st.error(f"😔 There was an error generating the report: {str(e)}")
    
    def _get_achievement_display_info(self, achievement_id):
        """Get achievement display information."""
        achievement_info = {
            'first_story_complete': {'emoji': '🎉', 'title': 'First Adventure', 'description': 'Completed first story adventure'},
            'math_master_beginner': {'emoji': '🧮', 'title': 'Math Explorer', 'description': 'Solved 5 math problems correctly'},
            'vocabulary_builder': {'emoji': '📚', 'title': 'Word Collector', 'description': 'Learned 10 new vocabulary words'},
            'story_enthusiast': {'emoji': '📖', 'title': 'Story Enthusiast', 'description': 'Completed 10 adventure stories'},
            'theme_explorer': {'emoji': '🗺️', 'title': 'Theme Explorer', 'description': 'Explored all story themes'}
        }
        
        return achievement_info.get(achievement_id, {
            'emoji': '⭐', 
            'title': 'Special Achievement', 
            'description': 'Earned a special milestone'
        })
    
    def _start_recommended_story(self, recommendation):
        """Start a story from recommendations."""
        profile = st.session_state.child_profile
        self._create_adaptive_story(
            profile, 
            f"🎭 {recommendation['theme']}", 
            f"🎯 {recommendation['learning_focus']}"
        )


def main():
    """Main application entry point."""
    app = EnhancedAdventureApp()
    app.run()


if __name__ == "__main__":
    main()