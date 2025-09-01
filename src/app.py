"""Streamlit web application for Ainia Adventure Stories with Enhanced Adaptive Features."""

import streamlit as st
import os
import time
from dotenv import load_dotenv
from story_generator import StoryGenerator

# Import enhanced adaptive modules
from adaptive_system import AdaptiveSystemManager, ChildProfile, DifficultyLevel, LearningStyle
from emotion_branching import EmotionAdaptiveManager, EmotionState
from progress_reporter import ProgressReportGenerator

# Load environment variables
load_dotenv()


def main():
    st.set_page_config(
        page_title="Ainia Adventure Stories",
        page_icon="🏰",
        layout="centered"
    )
    
    # Custom CSS for child-friendly interface
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
    
    /* Subheader styling */
    .stMarkdown h3 {
        color: #4ECDC4 !important;
        font-family: 'Comic Sans MS', cursive, sans-serif !important;
        text-align: center !important;
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
    
    /* Theme button styling */
    .theme-button {
        font-size: 1.5rem !important;
        height: 80px !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 15px !important;
        border: 2px solid #4ECDC4 !important;
        font-size: 1.1rem !important;
        padding: 0.75rem !important;
    }
    
    .stSelectbox > div > div > div {
        border-radius: 15px !important;
        border: 2px solid #4ECDC4 !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #D4F4DD !important;
        border: 2px solid #4ECDC4 !important;
        border-radius: 15px !important;
        color: #2D5B2D !important;
    }
    
    /* Info message styling */
    .stInfo {
        background-color: #E1F5FE !important;
        border: 2px solid #4ECDC4 !important;
        border-radius: 15px !important;
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
    
    /* Instructions styling */
    .instructions {
        background: linear-gradient(135deg, #FFE5E5, #E5F3FF) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        border-left: 5px solid #FF6B6B !important;
    }
    
    /* Celebration styling */
    .celebration {
        font-size: 1.3rem !important;
        color: #FF6B6B !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1>🏰 Ainia Adventure Stories</h1>', unsafe_allow_html=True)
    st.markdown('<h3>✨ Choose your adventure and learn while you play! ✨</h3>', unsafe_allow_html=True)
    
    # Add some magical sparkles
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("⭐")
    with col2:
        st.markdown("🌟")
    with col3:
        st.markdown("✨")
    with col4:
        st.markdown("🌟")
    with col5:
        st.markdown("⭐")
    
    # Initialize story generator with enhanced error handling
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        st.error("🔑 **API Key Missing!** We need an OpenAI API key to create your magical stories.")
        with st.expander("🛠️ **How to Fix This (For Parents)**"):
            st.markdown("""
            **Steps to add your API key:**
            1. Copy the `.env.example` file to `.env`
            2. Get your OpenAI API key from [OpenAI's website](https://platform.openai.com/api-keys)
            3. Add it to the `.env` file like this: `OPENAI_API_KEY=your_key_here`
            4. Restart the application
            
            **Note:** Keep your API key private and never share it publicly.
            """)
        st.stop()
    
    story_gen = StoryGenerator(api_key)
    
    # Theme selection with enhanced styling
    st.markdown("")  # Add some space
    st.markdown('<div class="adventure-header">🎭 Pick Your Adventure Theme! 🎭</div>', unsafe_allow_html=True)
    st.markdown("")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🐉\n\nDRAGONS\n\nFly with magical dragons!", use_container_width=True, key="dragon_btn"):
            st.session_state.theme = "dragons"
            st.success("🐉 Dragons chosen! Get ready for a magical adventure!")
            time.sleep(0.5)  # Brief pause for effect
    
    with col2:
        if st.button("🏴‍☠️\n\nPIRATES\n\nSail the seven seas!", use_container_width=True, key="pirate_btn"):
            st.session_state.theme = "pirates"
            st.success("🏴‍☠️ Pirates chosen! Ahoy, adventure awaits!")
            time.sleep(0.5)  # Brief pause for effect
    
    with col3:
        if st.button("👑\n\nPRINCESSES\n\nRule a magical kingdom!", use_container_width=True, key="princess_btn"):
            st.session_state.theme = "princesses"
            st.success("👑 Princesses chosen! Your royal adventure begins!")
            time.sleep(0.5)  # Brief pause for effect
    
    # Enhanced input sections
    st.markdown("")
    st.markdown('<div class="adventure-header">👋 Tell Us About You! 👋</div>', unsafe_allow_html=True)
    
    # Child name input with emoji
    child_name = st.text_input(
        "🌟 What's your name, brave adventurer?", 
        placeholder="Type your awesome name here!",
        help="This will make your story extra special and personal!"
    )
    
    # Learning focus selection with emojis
    st.markdown("🎯 **What exciting skill do you want to practice today?**")
    learning_focus = st.selectbox(
        "",
        ["🔢 counting and addition", "📚 vocabulary", "🧩 problem solving"],
        help="Don't worry - learning will be fun and feel like part of your adventure!"
    )
    
    # Clean up learning focus for processing (remove emoji)
    learning_focus_clean = learning_focus.split(" ", 1)[1] if learning_focus else learning_focus
    
    # Enhanced generate story button
    st.markdown("")
    if st.button("🚀 Create My Magical Adventure! 🚀", type="primary", use_container_width=True):
        if not child_name:
            st.error("🙋‍♀️ Oops! Please tell us your name first so we can make your adventure super special!")
        elif 'theme' not in st.session_state:
            st.error("🎭 Don't forget to pick your favorite adventure theme!")
        else:
            # Create a more engaging loading experience
            with st.spinner("🪄 Creating your magical adventure... ✨"):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)  # Simulate progress
                    progress_bar.progress(i + 1)
                
                story_result = story_gen.generate_adventure(
                    st.session_state.theme, 
                    child_name, 
                    learning_focus_clean
                )
                
                progress_bar.empty()  # Remove progress bar
                
                if len(story_result) == 2:
                    story, parent_explanation = story_result
                    st.session_state.current_story = story
                    st.session_state.current_explanation = parent_explanation
                    st.session_state.child_name = child_name
                    st.session_state.learning_focus = learning_focus_clean
                    
                    # Show celebration
                    st.balloons()
                    st.success(f"🎉 Amazing! Your adventure is ready, {child_name}! 🎉")
                else:
                    st.error("😔 Oops! Something went wrong. Let's try creating your adventure again!")
    
    # Enhanced story display
    if 'current_story' in st.session_state:
        st.markdown("")
        st.markdown('<div class="adventure-header">📚 Your Amazing Adventure! 📚</div>', unsafe_allow_html=True)
        
        # Story content in a beautiful container
        st.markdown(f'''
        <div class="story-content">
            {st.session_state.current_story}
        </div>
        ''', unsafe_allow_html=True)
        
        # Enhanced interactive learning component
        st.markdown("")
        st.markdown('<div class="adventure-header">🎯 Now It\'s Your Turn to Shine! 🎯</div>', unsafe_allow_html=True)
        
        if "counting" in st.session_state.learning_focus or "addition" in st.session_state.learning_focus:
            # Enhanced math problem interaction
            st.markdown("🔢 **Time for some magical math!**")
            child_answer = st.number_input(
                "What's your answer, math wizard?", 
                min_value=0, 
                max_value=50, 
                step=1,
                help="Take your time and think it through!"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("✨ Check My Answer! ✨", type="primary", use_container_width=True):
                    # Simple validation - in a real app, you'd extract the correct answer from the story
                    if child_answer > 0:
                        # Multiple celebration effects
                        st.balloons()
                        st.success(f"🎉 AMAZING, {st.session_state.child_name}! You're a math superstar! 🌟")
                        st.markdown('<div class="celebration">🏆 Adventure Complete! You\'re getting smarter every day! 🏆</div>', unsafe_allow_html=True)
                        
                        # Fun achievement badges
                        st.markdown("**🏅 You earned these achievement badges:**")
                        badge_col1, badge_col2, badge_col3 = st.columns(3)
                        with badge_col1:
                            st.markdown("🧮 **Math Master**")
                        with badge_col2:
                            st.markdown("🎯 **Problem Solver**") 
                        with badge_col3:
                            st.markdown("⭐ **Adventure Hero**")
                    else:
                        st.info("🤔 Give it your best shot! Every great mathematician started with their first try!")
        
        elif "vocabulary" in st.session_state.learning_focus:
            # Enhanced vocabulary challenge interaction
            st.markdown("📚 **Let's explore the power of words!**")
            child_definition = st.text_area(
                "What do you think this special word means?", 
                placeholder="Share your thoughts here... there are no wrong answers!",
                help="Every guess helps you learn!"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🌟 Share My Thinking! 🌟", type="primary", use_container_width=True):
                    if child_definition.strip():
                        st.balloons()
                        st.success(f"💭 Brilliant thinking, {st.session_state.child_name}! Your mind is like a treasure chest! 📚")
                        st.markdown('<div class="celebration">🎓 Adventure Complete! You\'re building an amazing vocabulary! 🎓</div>', unsafe_allow_html=True)
                        
                        # Fun achievement badges
                        st.markdown("**🏅 You earned these achievement badges:**")
                        badge_col1, badge_col2, badge_col3 = st.columns(3)
                        with badge_col1:
                            st.markdown("📖 **Word Explorer**")
                        with badge_col2:
                            st.markdown("💭 **Deep Thinker**")
                        with badge_col3:
                            st.markdown("⭐ **Adventure Hero**")
                    else:
                        st.info("💭 Share any thoughts you have! Every idea is valuable and helps you grow!")
        
        elif "problem solving" in st.session_state.learning_focus:
            # Enhanced problem solving interaction
            st.markdown("🧩 **Time to be a creative problem solver!**")
            child_solution = st.text_area(
                "What's your creative solution, genius?", 
                placeholder="Describe your brilliant idea here...",
                help="Think outside the box - creativity is your superpower!"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 Share My Solution! 🚀", type="primary", use_container_width=True):
                    if child_solution.strip():
                        st.balloons()
                        st.success(f"🧠 WOW! {st.session_state.child_name}, you're an incredible problem solver! 🌟")
                        st.markdown('<div class="celebration">🎯 Adventure Complete! Your creativity knows no bounds! 🎯</div>', unsafe_allow_html=True)
                        
                        # Fun achievement badges  
                        st.markdown("**🏅 You earned these achievement badges:**")
                        badge_col1, badge_col2, badge_col3 = st.columns(3)
                        with badge_col1:
                            st.markdown("🧩 **Creative Genius**")
                        with badge_col2:
                            st.markdown("💡 **Solution Master**")
                        with badge_col3:
                            st.markdown("⭐ **Adventure Hero**")
                    else:
                        st.info("💡 Every great inventor started with one creative idea! Share yours!")
        
        # Enhanced parent explanation toggle
        st.markdown("")
        st.markdown("---")
        with st.expander("👨‍👩‍👧‍👦 **Parent Dashboard** - Understanding Your Child's Learning Journey", expanded=False):
            if 'current_explanation' in st.session_state:
                st.markdown("### 🔍 **How AI Crafted This Educational Experience**")
                st.markdown(st.session_state.current_explanation)
                st.markdown("---")
                st.markdown("### 📈 **Learning Benefits**")
                st.markdown(f"""
                - **Engagement**: Storytelling makes learning memorable and fun
                - **Personalization**: Using {st.session_state.child_name}'s name creates connection
                - **Skill Development**: Practicing {st.session_state.learning_focus} in context
                - **Confidence Building**: Positive reinforcement encourages continued learning
                - **Critical Thinking**: Open-ended questions promote deeper understanding
                """)
        
        # Enhanced reset button
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎪 Create Another Amazing Adventure! 🎪", use_container_width=True):
                # Clear session state for new adventure
                keys_to_clear = ['current_story', 'current_explanation', 'theme']
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
    
    # Enhanced theme selection display
    if 'theme' in st.session_state:
        theme_emojis = {"dragons": "🐉", "pirates": "🏴‍☠️", "princesses": "👑"}
        st.success(f"{theme_emojis.get(st.session_state.theme, '🎭')} **Adventure theme selected:** {st.session_state.theme.title()} - Great choice!")
        
    # Enhanced instructions for first-time users
    if 'current_story' not in st.session_state and 'theme' not in st.session_state:
        st.markdown("")
        st.markdown('<div class="instructions">', unsafe_allow_html=True)
        st.markdown('<div class="adventure-header">🎯 How to Start Your Adventure! 🎯</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("""
            **🎭 Step 1:** Pick your theme
            **👋 Step 2:** Tell us your name  
            **🎯 Step 3:** Choose your learning focus
            """)
        with col2:
            st.markdown("""
            **🚀 Step 4:** Create your adventure!
            **🤔 Step 5:** Solve the fun challenge
            **🎉 Step 6:** Celebrate your success!
            """)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Fun motivational message
        st.markdown("")
        st.info("🌟 **Ready to become the hero of your own learning adventure?** Every great story starts with a brave choice! 🌟")


if __name__ == "__main__":
    main()