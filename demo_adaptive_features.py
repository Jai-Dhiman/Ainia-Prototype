"""Demonstration script for Phase 6 Enhanced Adaptive Learning Features."""

import time
import json
from datetime import datetime
from src.adaptive_system import (
    AdaptiveSystemManager, ChildProfile, DifficultyLevel, LearningStyle,
    LearningMetrics
)
from src.emotion_branching import (
    EmotionAdaptiveManager, EmotionState, Achievement
)
from src.progress_reporter import ProgressReportGenerator


def create_sample_interaction_data():
    """Create sample interaction data for demonstration."""
    return [
        {
            'theme': 'dragons',
            'learning_focus': 'math',
            'response': 'The dragon has 3 golden eggs and 2 silver eggs, so 3 + 2 = 5 eggs total!',
            'correct': True,
            'response_time': 8.5,
            'engagement_score': 0.9,
            'comprehension_score': 0.8,
            'session_duration': 420,
            'timestamp': time.time() - 7*24*3600,  # 1 week ago
            'story_completed': True,
            'confidence': 4
        },
        {
            'theme': 'pirates',
            'learning_focus': 'vocabulary',
            'response': 'The captain navigated using the compass to find the treasure island!',
            'correct': True,
            'response_time': 12.3,
            'engagement_score': 0.8,
            'comprehension_score': 0.9,
            'session_duration': 380,
            'timestamp': time.time() - 5*24*3600,  # 5 days ago
            'story_completed': True,
            'confidence': 5
        },
        {
            'theme': 'princesses',
            'learning_focus': 'problem_solving',
            'response': 'The princess could unite the kingdoms by organizing a peace festival where everyone shares their culture',
            'correct': True,
            'response_time': 25.7,
            'engagement_score': 0.95,
            'comprehension_score': 0.95,
            'session_duration': 520,
            'timestamp': time.time() - 3*24*3600,  # 3 days ago
            'story_completed': True,
            'confidence': 5
        },
        {
            'theme': 'dragons',
            'learning_focus': 'math',
            'response': 'um... 4?',
            'correct': False,
            'response_time': 35.2,
            'engagement_score': 0.4,
            'comprehension_score': 0.3,
            'session_duration': 180,
            'timestamp': time.time() - 1*24*3600,  # 1 day ago
            'story_completed': True,
            'confidence': 2
        },
        {
            'theme': 'pirates',
            'learning_focus': 'vocabulary',
            'response': 'The ship goes on water and finds stuff',
            'correct': False,
            'response_time': 15.8,
            'engagement_score': 0.6,
            'comprehension_score': 0.5,
            'session_duration': 320,
            'timestamp': time.time() - 0.5*24*3600,  # 12 hours ago
            'story_completed': True,
            'confidence': 3
        }
    ]


def demonstrate_adaptive_system():
    """Demonstrate the adaptive learning system capabilities."""
    print("🚀 PHASE 6 ENHANCED ADAPTIVE LEARNING FEATURES DEMONSTRATION")
    print("=" * 80)
    
    # Initialize managers
    adaptive_manager = AdaptiveSystemManager()
    emotion_manager = EmotionAdaptiveManager()
    report_generator = ProgressReportGenerator()
    
    print("\n1. 👶 CREATING ADAPTIVE CHILD PROFILE")
    print("-" * 50)
    
    # Create a sample child profile
    profile = adaptive_manager.get_or_create_profile("Emma", age=7)
    profile.learning_style = LearningStyle.VISUAL
    profile.difficulty_level = DifficultyLevel.INTERMEDIATE
    
    print(f"✅ Created profile for {profile.name}")
    print(f"   Age: {profile.age}")
    print(f"   Learning Style: {profile.learning_style.value}")
    print(f"   Difficulty Level: {profile.difficulty_level.name}")
    
    print("\n2. 📊 PROCESSING INTERACTION HISTORY")
    print("-" * 50)
    
    # Simulate interaction history
    sample_interactions = create_sample_interaction_data()
    
    for i, interaction in enumerate(sample_interactions):
        print(f"\nProcessing interaction {i+1}/{len(sample_interactions)}...")
        
        # Update profile with interaction
        adaptive_manager.update_profile_from_interaction(profile, interaction)
        
        # Process emotions
        emotion_results = emotion_manager.process_interaction_emotions(profile, interaction)
        
        print(f"   Theme: {interaction['theme'].title()}")
        print(f"   Learning Focus: {interaction['learning_focus'].title()}")
        print(f"   Detected Emotion: {emotion_results['detected_emotion'].title()}")
        print(f"   Response Correct: {'✅' if interaction['correct'] else '❌'}")
        
        if emotion_results['new_achievements']:
            print(f"   🏆 New Achievements: {len(emotion_results['new_achievements'])}")
            for achievement in emotion_results['new_achievements']:
                print(f"      - {achievement['title']}")
    
    print(f"\n3. 🧠 ADAPTIVE INTELLIGENCE ANALYSIS")
    print("-" * 50)
    
    # Show learning metrics
    metrics = profile.learning_metrics
    print(f"📈 Learning Metrics:")
    print(f"   Success Rate: {metrics.success_rate:.1%}")
    print(f"   Engagement Level: {metrics.engagement_level:.1%}")
    print(f"   Math Level: {metrics.math_level:.1f}/4.0")
    print(f"   Vocabulary Level: {metrics.vocabulary_level:.1f}/4.0")
    print(f"   Problem Solving Level: {metrics.problem_solving_level:.1f}/4.0")
    print(f"   Average Response Time: {metrics.response_time_avg:.1f}s")
    
    # Show difficulty adaptation
    print(f"\n🎯 Adaptive Difficulty:")
    print(f"   Current Level: {profile.difficulty_level.name}")
    print(f"   Learning Style: {profile.learning_style.value}")
    
    # Show interest graph
    if hasattr(profile, 'interest_graph'):
        print(f"\n🗺️ Theme Interest Graph:")
        for theme, weight in sorted(profile.interest_graph.items(), key=lambda x: x[1], reverse=True):
            print(f"   {theme.title()}: {weight:.2f}")
    
    print(f"\n4. 🎯 PERSONALIZED RECOMMENDATIONS")
    print("-" * 50)
    
    # Generate recommendations
    recommendations = adaptive_manager.get_recommendations(profile)
    
    print(f"📚 Generated {len(recommendations)} personalized recommendations:")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"\n   Recommendation {i}:")
        print(f"   Theme: {rec['theme'].title()}")
        print(f"   Learning Focus: {rec['learning_focus'].title()}")
        print(f"   Reason: {rec['reason']}")
        print(f"   Estimated Duration: {rec['estimated_duration']} minutes")
        print(f"   Confidence Score: {rec['confidence_score']:.1%}")
    
    print(f"\n5. 🎨 ADAPTIVE VOCABULARY SYSTEM")
    print("-" * 50)
    
    # Demonstrate vocabulary adaptation
    vocab_words = adaptive_manager.vocabulary_system.get_appropriate_vocabulary(profile, 'dragons')
    print(f"🐉 Age-appropriate vocabulary for Dragons theme:")
    print(f"   Level {int(profile.learning_metrics.vocabulary_level)}: {', '.join(vocab_words)}")
    
    # Show different difficulty levels
    for level in [1, 2, 3, 4]:
        test_profile = ChildProfile(name="Test", age=5+level)
        test_profile.learning_metrics.vocabulary_level = level
        words = adaptive_manager.vocabulary_system.get_appropriate_vocabulary(test_profile, 'dragons')
        print(f"   Level {level}: {', '.join(words[:5])}")  # Show first 5 words
    
    print(f"\n6. 😊 EMOTION-BASED STORY BRANCHING")
    print("-" * 50)
    
    # Demonstrate emotion detection and branching
    recent_interaction = sample_interactions[-1]  # Most recent interaction
    emotion_results = emotion_manager.process_interaction_emotions(profile, recent_interaction)
    
    print(f"🎭 Emotion Analysis:")
    print(f"   Detected Emotion: {emotion_results['detected_emotion'].title()}")
    print(f"   Story Modifications: {emotion_results['story_modifications']['emotion_branch']}")
    
    modifications = emotion_results['story_modifications']['story_modifications']
    print(f"   Adaptive Changes:")
    for key, value in modifications.items():
        if value:
            print(f"      - {key.replace('_', ' ').title()}: {'✅' if value else '❌'}")
    
    print(f"\n7. 🏆 ACHIEVEMENT SYSTEM")
    print("-" * 50)
    
    # Show achievements
    if hasattr(profile, 'achievements') and profile.achievements:
        print(f"🎉 Earned Achievements ({len(profile.achievements)}):")
        for achievement_id in profile.achievements:
            achievement_info = {
                'first_story_complete': '🎉 First Adventure Complete',
                'math_master_beginner': '🧮 Math Explorer',
                'vocabulary_builder': '📚 Word Collector',
                'story_enthusiast': '📖 Story Enthusiast',
                'theme_explorer': '🗺️ Theme Explorer'
            }
            print(f"   - {achievement_info.get(achievement_id, '⭐ Special Achievement')}")
    else:
        print("🌟 Ready to earn achievements!")
    
    # Show achievement progress
    if emotion_results.get('achievement_progress'):
        print(f"\n🎯 Achievement Progress:")
        for achievement_id, progress in emotion_results['achievement_progress'].items():
            percentage = progress['progress']
            current = progress['current']
            target = progress['target']
            title = progress['title']
            print(f"   {title}: {current}/{target} ({percentage:.0f}%)")
    
    print(f"\n8. 📋 PROGRESS REPORT GENERATION")
    print("-" * 50)
    
    try:
        print("📊 Generating comprehensive progress report...")
        report_path = report_generator.generate_progress_report(profile, 'comprehensive')
        print(f"✅ Report generated successfully!")
        print(f"   File: {report_path}")
        print(f"   Size: {os.path.getsize(report_path) / 1024:.1f} KB")
        
        # Generate different report types
        print(f"\n📈 Generating additional report types...")
        summary_report = report_generator.generate_progress_report(profile, 'summary')
        achievement_report = report_generator.generate_progress_report(profile, 'achievement')
        
        print(f"   Summary Report: {summary_report}")
        print(f"   Achievement Report: {achievement_report}")
        
    except Exception as e:
        print(f"❌ Error generating reports: {str(e)}")
        print("   Note: PDF generation requires proper environment setup")
    
    print(f"\n9. 📊 ADAPTIVE STORY PARAMETERS")
    print("-" * 50)
    
    # Show how story generation would be adapted
    adaptive_params = adaptive_manager.get_adaptive_story_parameters(profile, 'dragons')
    print(f"🐉 Adaptive parameters for Dragons story:")
    print(f"   Difficulty Level: {adaptive_params['difficulty_level']}/4")
    print(f"   Learning Style: {adaptive_params['learning_style']}")
    print(f"   Vocabulary Words: {', '.join(adaptive_params['vocabulary_words'][:5])}")
    
    metrics_data = adaptive_params['learning_metrics']
    print(f"   Success Rate: {metrics_data['success_rate']:.1%}")
    print(f"   Engagement Level: {metrics_data['engagement_level']:.1%}")
    
    print(f"\n10. 🔮 FUTURE LEARNING PREDICTIONS")
    print("-" * 50)
    
    # Predict optimal next learning focuses
    print(f"🎯 Recommended Learning Path for {profile.name}:")
    
    if metrics.math_level < metrics.vocabulary_level:
        print(f"   📐 Focus on Math: Current level {metrics.math_level:.1f}, target {metrics.vocabulary_level:.1f}")
    elif metrics.vocabulary_level < metrics.problem_solving_level:
        print(f"   📚 Focus on Vocabulary: Current level {metrics.vocabulary_level:.1f}")
    else:
        print(f"   🧩 Advance Problem Solving: Ready for next level challenges")
    
    # Show engagement optimization
    if metrics.engagement_level > 0.8:
        print(f"   ⚡ High engagement detected - ready for challenging content")
    elif metrics.engagement_level < 0.6:
        print(f"   🎨 Engagement could improve - try different themes or interactive elements")
    
    print(f"\n" + "=" * 80)
    print(f"🎉 PHASE 6 DEMONSTRATION COMPLETE!")
    print(f"   Profile: {profile.name} (Age {profile.age})")
    print(f"   Interactions Processed: {len(sample_interactions)}")
    print(f"   Success Rate: {metrics.success_rate:.1%}")
    print(f"   Achievements Earned: {len(getattr(profile, 'achievements', []))}")
    print(f"   Recommendations Generated: {len(recommendations)}")
    print(f"   Adaptive Features: ✅ All systems operational!")
    print(f"=" * 80)


def demonstrate_multi_child_comparison():
    """Demonstrate system with multiple child profiles."""
    print(f"\n🔄 BONUS: MULTI-CHILD COMPARISON")
    print("-" * 50)
    
    adaptive_manager = AdaptiveSystemManager()
    
    # Create different child profiles
    profiles = [
        ("Alex", 5, LearningStyle.AUDITORY, DifficultyLevel.BEGINNER),
        ("Sophia", 8, LearningStyle.KINESTHETIC, DifficultyLevel.ADVANCED),
        ("Emma", 7, LearningStyle.VISUAL, DifficultyLevel.INTERMEDIATE)
    ]
    
    print("👨‍👩‍👧‍👦 Comparing Different Child Profiles:")
    
    for name, age, style, difficulty in profiles:
        profile = adaptive_manager.get_or_create_profile(name, age)
        profile.learning_style = style
        profile.difficulty_level = difficulty
        
        # Simulate some interactions
        if name == "Alex":  # Beginner, needs encouragement
            interaction = {
                'correct': True, 'engagement_score': 0.7, 'response_time': 15.0,
                'learning_focus': 'math', 'theme': 'dragons'
            }
        elif name == "Sophia":  # Advanced, ready for challenges
            interaction = {
                'correct': True, 'engagement_score': 0.95, 'response_time': 8.0,
                'learning_focus': 'problem_solving', 'theme': 'princesses'
            }
        else:  # Emma - intermediate
            interaction = {
                'correct': True, 'engagement_score': 0.85, 'response_time': 12.0,
                'learning_focus': 'vocabulary', 'theme': 'pirates'
            }
        
        adaptive_manager.update_profile_from_interaction(profile, interaction)
        recommendations = adaptive_manager.get_recommendations(profile)
        
        print(f"\n   👶 {name} (Age {age}):")
        print(f"      Learning Style: {style.value}")
        print(f"      Difficulty: {difficulty.name}")
        print(f"      Top Recommendation: {recommendations[0]['theme'].title()} - {recommendations[0]['learning_focus'].title()}")
        print(f"      Confidence: {recommendations[0]['confidence_score']:.1%}")


if __name__ == "__main__":
    import os
    
    # Set up basic requirements for demonstration
    print("🔧 Setting up demonstration environment...")
    
    demonstrate_adaptive_system()
    demonstrate_multi_child_comparison()
    
    print(f"\n💡 To see these features in action:")
    print(f"   1. Run: uv run streamlit run src/enhanced_app.py")
    print(f"   2. Navigate between Child View and Parent Dashboard")
    print(f"   3. Create stories and observe adaptive behavior")
    print(f"   4. Check Parent Dashboard for detailed analytics")
    
    print(f"\n🚀 Phase 6 Enhanced Adaptive Learning Features are ready for Day 7!")