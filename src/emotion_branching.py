"""Emotion-based story branching and achievement system for Ainia Adventure Stories."""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json


class EmotionState(Enum):
    """Child's emotional engagement states."""
    EXCITED = "excited"
    CURIOUS = "curious"
    CONFIDENT = "confident"
    FRUSTRATED = "frustrated"
    BORED = "bored"
    NEUTRAL = "neutral"


class StoryBranch(Enum):
    """Different story branches based on emotion."""
    ENCOURAGING = "encouraging"
    CHALLENGING = "challenging"
    COMFORTING = "comforting"
    ENERGIZING = "energizing"
    SIMPLIFYING = "simplifying"


@dataclass
class EmotionMetrics:
    """Track emotional engagement over time."""
    current_emotion: EmotionState = EmotionState.NEUTRAL
    confidence_level: float = 0.5
    excitement_level: float = 0.5
    frustration_level: float = 0.0
    engagement_duration: float = 0.0
    recent_emotions: List[str] = None
    
    def __post_init__(self):
        if self.recent_emotions is None:
            self.recent_emotions = []


@dataclass
class Achievement:
    """Individual achievement tracking."""
    id: str
    title: str
    description: str
    category: str  # 'learning', 'engagement', 'creativity', 'persistence'
    earned_date: float
    story_context: Dict
    celebration_message: str


class EmotionDetector:
    """Detect child's emotional state from interactions."""
    
    def __init__(self):
        self.emotion_indicators = {
            EmotionState.EXCITED: {
                'keywords': ['wow', 'amazing', 'awesome', 'cool', 'yes', '!', 'love', 'fantastic'],
                'response_patterns': ['multiple_exclamations', 'long_responses', 'immediate_response'],
                'threshold': 0.7
            },
            EmotionState.CURIOUS: {
                'keywords': ['why', 'how', 'what', 'where', 'tell me more', '?', 'interesting'],
                'response_patterns': ['questions', 'exploration_requests'],
                'threshold': 0.6
            },
            EmotionState.CONFIDENT: {
                'keywords': ['easy', 'know', 'sure', 'definitely', 'of course', 'obviously'],
                'response_patterns': ['quick_correct_answers', 'detailed_responses'],
                'threshold': 0.8
            },
            EmotionState.FRUSTRATED: {
                'keywords': ['hard', 'difficult', 'don\'t know', 'confused', 'help', 'stuck'],
                'response_patterns': ['slow_response', 'short_answers', 'repeated_errors'],
                'threshold': 0.7
            },
            EmotionState.BORED: {
                'keywords': ['boring', 'tired', 'whatever', 'ok', 'fine', 'done'],
                'response_patterns': ['minimal_responses', 'declining_engagement'],
                'threshold': 0.6
            }
        }
    
    def detect_emotion(self, interaction_data: Dict, historical_emotions: List[str]) -> EmotionState:
        """Detect current emotional state from interaction."""
        response_text = interaction_data.get('response', '').lower()
        response_time = interaction_data.get('response_time', 15.0)
        is_correct = interaction_data.get('correct', False)
        session_duration = interaction_data.get('session_duration', 0)
        
        emotion_scores = {}
        
        for emotion, indicators in self.emotion_indicators.items():
            score = 0.0
            
            # Keyword analysis
            keyword_count = sum(1 for keyword in indicators['keywords'] 
                              if keyword in response_text)
            if keyword_count > 0:
                score += 0.4 * (keyword_count / len(indicators['keywords']))
            
            # Response pattern analysis
            score += self._analyze_response_patterns(
                interaction_data, indicators['response_patterns']
            ) * 0.6
            
            emotion_scores[emotion] = score
        
        # Apply contextual adjustments
        emotion_scores = self._apply_contextual_adjustments(
            emotion_scores, interaction_data, historical_emotions
        )
        
        # Find dominant emotion
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        dominant_score = emotion_scores[dominant_emotion]
        
        # Only return emotion if confidence is above threshold
        threshold = self.emotion_indicators[dominant_emotion]['threshold']
        if dominant_score >= threshold:
            return dominant_emotion
        
        return EmotionState.NEUTRAL
    
    def _analyze_response_patterns(self, interaction_data: Dict, patterns: List[str]) -> float:
        """Analyze response patterns for emotion detection."""
        response_text = interaction_data.get('response', '')
        response_time = interaction_data.get('response_time', 15.0)
        is_correct = interaction_data.get('correct', False)
        
        pattern_score = 0.0
        
        for pattern in patterns:
            if pattern == 'multiple_exclamations' and response_text.count('!') > 1:
                pattern_score += 0.3
            elif pattern == 'long_responses' and len(response_text) > 50:
                pattern_score += 0.2
            elif pattern == 'immediate_response' and response_time < 5.0:
                pattern_score += 0.3
            elif pattern == 'questions' and '?' in response_text:
                pattern_score += 0.4
            elif pattern == 'quick_correct_answers' and is_correct and response_time < 10.0:
                pattern_score += 0.4
            elif pattern == 'slow_response' and response_time > 30.0:
                pattern_score += 0.3
            elif pattern == 'short_answers' and len(response_text) < 10:
                pattern_score += 0.2
            elif pattern == 'minimal_responses' and len(response_text) < 5:
                pattern_score += 0.4
        
        return min(1.0, pattern_score)
    
    def _apply_contextual_adjustments(self, emotion_scores: Dict, 
                                   interaction_data: Dict, 
                                   historical_emotions: List[str]) -> Dict:
        """Apply contextual adjustments to emotion scores."""
        # Recent emotion momentum
        if historical_emotions:
            recent_emotion = historical_emotions[-1]
            if recent_emotion in emotion_scores:
                emotion_scores[recent_emotion] *= 1.2  # Boost recent emotion
        
        # Performance context
        is_correct = interaction_data.get('correct', False)
        if is_correct:
            emotion_scores[EmotionState.CONFIDENT] *= 1.3
            emotion_scores[EmotionState.EXCITED] *= 1.1
            emotion_scores[EmotionState.FRUSTRATED] *= 0.7
        else:
            emotion_scores[EmotionState.FRUSTRATED] *= 1.2
            emotion_scores[EmotionState.CONFIDENT] *= 0.6
        
        return emotion_scores


class StoryBranchingEngine:
    """Generate appropriate story branches based on emotional state."""
    
    def __init__(self):
        self.branching_strategies = {
            EmotionState.EXCITED: {
                'branch': StoryBranch.CHALLENGING,
                'modifications': {
                    'increase_complexity': True,
                    'add_bonus_challenges': True,
                    'celebratory_tone': True,
                    'energy_level': 'high'
                }
            },
            EmotionState.CURIOUS: {
                'branch': StoryBranch.ENERGIZING,
                'modifications': {
                    'add_mysteries': True,
                    'include_exploration': True,
                    'ask_questions': True,
                    'detailed_descriptions': True
                }
            },
            EmotionState.CONFIDENT: {
                'branch': StoryBranch.CHALLENGING,
                'modifications': {
                    'leadership_roles': True,
                    'complex_decisions': True,
                    'multiple_solutions': True,
                    'responsibility_themes': True
                }
            },
            EmotionState.FRUSTRATED: {
                'branch': StoryBranch.COMFORTING,
                'modifications': {
                    'reduce_complexity': True,
                    'provide_hints': True,
                    'encouraging_tone': True,
                    'break_into_steps': True
                }
            },
            EmotionState.BORED: {
                'branch': StoryBranch.ENERGIZING,
                'modifications': {
                    'surprise_elements': True,
                    'interactive_choices': True,
                    'humor_injection': True,
                    'pace_acceleration': True
                }
            },
            EmotionState.NEUTRAL: {
                'branch': StoryBranch.ENCOURAGING,
                'modifications': {
                    'balanced_approach': True,
                    'gentle_challenges': True,
                    'positive_reinforcement': True
                }
            }
        }
    
    def get_story_modifications(self, emotion_state: EmotionState, 
                              current_story_params: Dict) -> Dict:
        """Get story modifications based on emotional state."""
        if emotion_state not in self.branching_strategies:
            emotion_state = EmotionState.NEUTRAL
        
        strategy = self.branching_strategies[emotion_state]
        modifications = strategy['modifications'].copy()
        
        # Add emotion context to story parameters
        enhanced_params = current_story_params.copy()
        enhanced_params.update({
            'emotion_branch': strategy['branch'].value,
            'emotion_state': emotion_state.value,
            'story_modifications': modifications
        })
        
        return enhanced_params
    
    def generate_emotion_appropriate_prompt_additions(self, emotion_state: EmotionState) -> str:
        """Generate prompt additions based on emotional state."""
        prompt_additions = {
            EmotionState.EXCITED: """
                The child is very excited! Make the story extra engaging with:
                - Celebratory language and exclamation points
                - More challenging but achievable tasks
                - Bonus surprises and discoveries
                - High energy and adventure
            """,
            EmotionState.CURIOUS: """
                The child is curious and wants to explore! Include:
                - Mysterious elements to investigate
                - Detailed world-building descriptions
                - Questions that encourage deeper thinking
                - Opportunities for discovery and learning
            """,
            EmotionState.CONFIDENT: """
                The child feels confident! Provide:
                - Leadership opportunities in the story
                - More complex challenges they can handle
                - Choices that matter and have consequences
                - Recognition of their growing abilities
            """,
            EmotionState.FRUSTRATED: """
                The child seems frustrated. Be extra supportive:
                - Break challenges into smaller, manageable steps
                - Provide gentle hints and encouragement
                - Use a warm, reassuring tone
                - Celebrate small victories along the way
            """,
            EmotionState.BORED: """
                The child seems less engaged. Add excitement:
                - Unexpected plot twists and surprises
                - Interactive elements and choices
                - Humor and playful elements
                - Faster pacing and dynamic action
            """,
            EmotionState.NEUTRAL: """
                Maintain balanced engagement:
                - Mix of challenge and support
                - Positive, encouraging tone
                - Appropriate complexity for their level
                - Clear structure with achievable goals
            """
        }
        
        return prompt_additions.get(emotion_state, prompt_additions[EmotionState.NEUTRAL])


class AchievementSystem:
    """Comprehensive achievement tracking and milestone system."""
    
    def __init__(self):
        self.achievement_definitions = {
            # Learning achievements
            'first_story_complete': Achievement(
                'first_story_complete', 'First Adventure Complete!', 
                'Completed your very first adventure story', 'learning', 
                0, {}, '🎉 Amazing! You completed your first adventure!'
            ),
            'math_master_beginner': Achievement(
                'math_master_beginner', 'Math Explorer', 
                'Solved 5 math problems correctly', 'learning', 
                0, {}, '🧮 You\'re becoming a math explorer!'
            ),
            'vocabulary_builder': Achievement(
                'vocabulary_builder', 'Word Collector', 
                'Learned 10 new vocabulary words', 'learning', 
                0, {}, '📚 You\'re collecting words like treasures!'
            ),
            'problem_solver': Achievement(
                'problem_solver', 'Puzzle Master', 
                'Solved challenging problems in stories', 'learning', 
                0, {}, '🧩 You\'re excellent at solving puzzles!'
            ),
            
            # Engagement achievements
            'story_enthusiast': Achievement(
                'story_enthusiast', 'Story Enthusiast', 
                'Completed 10 adventure stories', 'engagement', 
                0, {}, '📖 You absolutely love adventure stories!'
            ),
            'theme_explorer': Achievement(
                'theme_explorer', 'Theme Explorer', 
                'Tried all different story themes', 'engagement', 
                0, {}, '🗺️ You\'ve explored every magical realm!'
            ),
            'quick_thinker': Achievement(
                'quick_thinker', 'Quick Thinker', 
                'Answered challenges in under 10 seconds', 'engagement', 
                0, {}, '⚡ Lightning fast thinking!'
            ),
            
            # Creativity achievements
            'creative_responses': Achievement(
                'creative_responses', 'Creative Storyteller', 
                'Gave unique and creative responses', 'creativity', 
                0, {}, '🎨 Your imagination is incredible!'
            ),
            'question_asker': Achievement(
                'question_asker', 'Curious Explorer', 
                'Asked thoughtful questions during stories', 'creativity', 
                0, {}, '❓ Your curiosity makes stories even better!'
            ),
            
            # Persistence achievements
            'never_give_up': Achievement(
                'never_give_up', 'Never Give Up', 
                'Kept trying until you succeeded', 'persistence', 
                0, {}, '💪 Your determination is inspiring!'
            ),
            'challenge_seeker': Achievement(
                'challenge_seeker', 'Challenge Seeker', 
                'Chose harder difficulty levels', 'persistence', 
                0, {}, '🎯 You love challenging yourself!'
            ),
            'improvement_champion': Achievement(
                'improvement_champion', 'Improvement Champion', 
                'Showed consistent improvement over time', 'persistence', 
                0, {}, '📈 You\'re getting better every day!'
            )
        }
        
        self.milestone_thresholds = {
            'stories_completed': [1, 5, 10, 25, 50],
            'math_problems_solved': [1, 5, 10, 20, 50],
            'vocabulary_words_learned': [5, 10, 25, 50, 100],
            'consecutive_correct': [3, 5, 10, 15, 25],
            'themes_explored': [2, 3, 5, 7, 10],
            'session_streak': [3, 7, 14, 30, 60]  # Days
        }
    
    def check_for_new_achievements(self, profile, interaction_data: Dict) -> List[Achievement]:
        """Check if interaction earns new achievements."""
        new_achievements = []
        
        # Update profile statistics
        self._update_achievement_stats(profile, interaction_data)
        
        # Check each achievement type
        for achievement_id, achievement_template in self.achievement_definitions.items():
            if achievement_id not in profile.achievements:
                if self._check_achievement_criteria(achievement_id, profile, interaction_data):
                    new_achievement = Achievement(
                        id=achievement_template.id,
                        title=achievement_template.title,
                        description=achievement_template.description,
                        category=achievement_template.category,
                        earned_date=time.time(),
                        story_context=interaction_data,
                        celebration_message=achievement_template.celebration_message
                    )
                    new_achievements.append(new_achievement)
                    profile.achievements.append(achievement_id)
        
        return new_achievements
    
    def _update_achievement_stats(self, profile, interaction_data: Dict):
        """Update profile statistics for achievement tracking."""
        if not hasattr(profile, 'achievement_stats'):
            profile.achievement_stats = {
                'stories_completed': 0,
                'math_problems_solved': 0,
                'vocabulary_words_learned': 0,
                'consecutive_correct': 0,
                'current_streak': 0,
                'themes_explored': set(),
                'quick_responses': 0,
                'creative_responses': 0,
                'questions_asked': 0,
                'challenges_overcome': 0,
                'session_dates': []
            }
        
        stats = profile.achievement_stats
        
        # Update based on interaction
        if interaction_data.get('story_completed', False):
            stats['stories_completed'] += 1
        
        if interaction_data.get('correct', False):
            stats['current_streak'] += 1
            if 'math' in interaction_data.get('learning_focus', ''):
                stats['math_problems_solved'] += 1
        else:
            stats['current_streak'] = 0
        
        if interaction_data.get('new_words_learned', 0) > 0:
            stats['vocabulary_words_learned'] += interaction_data['new_words_learned']
        
        theme = interaction_data.get('theme', '')
        if theme:
            stats['themes_explored'].add(theme)
        
        if interaction_data.get('response_time', 15) < 10:
            stats['quick_responses'] += 1
        
        if self._is_creative_response(interaction_data.get('response', '')):
            stats['creative_responses'] += 1
        
        if '?' in interaction_data.get('response', ''):
            stats['questions_asked'] += 1
        
        # Track session dates for streak calculation
        today = time.strftime('%Y-%m-%d')
        if today not in stats['session_dates']:
            stats['session_dates'].append(today)
    
    def _check_achievement_criteria(self, achievement_id: str, profile, interaction_data: Dict) -> bool:
        """Check if specific achievement criteria are met."""
        if not hasattr(profile, 'achievement_stats'):
            return False
        
        stats = profile.achievement_stats
        
        criteria_map = {
            'first_story_complete': lambda: stats['stories_completed'] >= 1,
            'math_master_beginner': lambda: stats['math_problems_solved'] >= 5,
            'vocabulary_builder': lambda: stats['vocabulary_words_learned'] >= 10,
            'problem_solver': lambda: stats['stories_completed'] >= 3 and 
                                    profile.learning_metrics.success_rate > 0.8,
            'story_enthusiast': lambda: stats['stories_completed'] >= 10,
            'theme_explorer': lambda: len(stats['themes_explored']) >= 3,
            'quick_thinker': lambda: stats['quick_responses'] >= 5,
            'creative_responses': lambda: stats['creative_responses'] >= 3,
            'question_asker': lambda: stats['questions_asked'] >= 5,
            'never_give_up': lambda: stats['challenges_overcome'] >= 3,
            'challenge_seeker': lambda: profile.difficulty_level.value >= 3,
            'improvement_champion': lambda: len(profile.interaction_history) >= 10 and
                                          self._check_improvement_trend(profile)
        }
        
        return criteria_map.get(achievement_id, lambda: False)()
    
    def _is_creative_response(self, response: str) -> bool:
        """Check if response shows creativity."""
        creative_indicators = [
            'imagine', 'pretend', 'what if', 'maybe', 'could be',
            'different way', 'another idea', 'creative', 'unique'
        ]
        response_lower = response.lower()
        return any(indicator in response_lower for indicator in creative_indicators) or len(response) > 30
    
    def _check_improvement_trend(self, profile) -> bool:
        """Check if child is showing improvement over time."""
        if len(profile.interaction_history) < 10:
            return False
        
        recent_success = sum(1 for i in profile.interaction_history[-5:] if i.get('correct', False))
        early_success = sum(1 for i in profile.interaction_history[:5] if i.get('correct', False))
        
        return recent_success > early_success
    
    def get_progress_towards_achievements(self, profile) -> Dict:
        """Get progress towards unearned achievements."""
        if not hasattr(profile, 'achievement_stats'):
            return {}
        
        progress = {}
        stats = profile.achievement_stats
        
        for achievement_id, achievement in self.achievement_definitions.items():
            if achievement_id not in profile.achievements:
                # Calculate progress percentage
                if achievement_id == 'math_master_beginner':
                    progress[achievement_id] = {
                        'progress': min(100, (stats['math_problems_solved'] / 5) * 100),
                        'current': stats['math_problems_solved'],
                        'target': 5,
                        'title': achievement.title
                    }
                elif achievement_id == 'vocabulary_builder':
                    progress[achievement_id] = {
                        'progress': min(100, (stats['vocabulary_words_learned'] / 10) * 100),
                        'current': stats['vocabulary_words_learned'],
                        'target': 10,
                        'title': achievement.title
                    }
                elif achievement_id == 'story_enthusiast':
                    progress[achievement_id] = {
                        'progress': min(100, (stats['stories_completed'] / 10) * 100),
                        'current': stats['stories_completed'],
                        'target': 10,
                        'title': achievement.title
                    }
        
        return progress


class EmotionAdaptiveManager:
    """Main manager for emotion-based adaptation and achievements."""
    
    def __init__(self):
        self.emotion_detector = EmotionDetector()
        self.branching_engine = StoryBranchingEngine()
        self.achievement_system = AchievementSystem()
    
    def process_interaction_emotions(self, profile, interaction_data: Dict) -> Dict:
        """Process emotional aspects of interaction and return adaptive parameters."""
        # Detect current emotion
        historical_emotions = getattr(profile, 'recent_emotions', [])
        current_emotion = self.emotion_detector.detect_emotion(interaction_data, historical_emotions)
        
        # Update emotion history
        if not hasattr(profile, 'emotion_metrics'):
            profile.emotion_metrics = EmotionMetrics()
        
        profile.emotion_metrics.current_emotion = current_emotion
        profile.emotion_metrics.recent_emotions.append(current_emotion.value)
        
        # Keep only last 10 emotions
        if len(profile.emotion_metrics.recent_emotions) > 10:
            profile.emotion_metrics.recent_emotions = profile.emotion_metrics.recent_emotions[-10:]
        
        # Check for achievements
        new_achievements = self.achievement_system.check_for_new_achievements(profile, interaction_data)
        
        # Get story modifications based on emotion
        current_params = interaction_data.get('story_params', {})
        adaptive_params = self.branching_engine.get_story_modifications(current_emotion, current_params)
        
        # Get prompt additions for emotional context
        prompt_additions = self.branching_engine.generate_emotion_appropriate_prompt_additions(current_emotion)
        
        return {
            'detected_emotion': current_emotion.value,
            'new_achievements': [asdict(achievement) for achievement in new_achievements],
            'story_modifications': adaptive_params,
            'prompt_additions': prompt_additions,
            'achievement_progress': self.achievement_system.get_progress_towards_achievements(profile)
        }