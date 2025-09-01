"""Advanced Personalization & Learning Adaptation System for Ainia Adventure Stories."""

import json
import time
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class LearningStyle(Enum):
    """Learning style preferences detected from child interactions."""
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    MIXED = "mixed"


class DifficultyLevel(Enum):
    """Dynamic difficulty levels."""
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


@dataclass
class LearningMetrics:
    """Tracks learning progress and engagement metrics."""
    reading_speed_wpm: float = 0.0
    comprehension_score: float = 0.0
    engagement_level: float = 0.0
    response_time_avg: float = 0.0
    success_rate: float = 0.0
    vocabulary_level: int = 1
    math_level: int = 1
    problem_solving_level: int = 1


@dataclass
class ChildProfile:
    """Comprehensive child profile with learning analytics."""
    name: str
    age: int
    learning_style: LearningStyle = LearningStyle.MIXED
    difficulty_level: DifficultyLevel = DifficultyLevel.BEGINNER
    preferred_themes: List[str] = None
    learning_metrics: LearningMetrics = None
    interaction_history: List[Dict] = None
    achievements: List[str] = None
    last_updated: float = None
    
    def __post_init__(self):
        if self.preferred_themes is None:
            self.preferred_themes = []
        if self.learning_metrics is None:
            self.learning_metrics = LearningMetrics()
        if self.interaction_history is None:
            self.interaction_history = []
        if self.achievements is None:
            self.achievements = []
        if self.last_updated is None:
            self.last_updated = time.time()


class DynamicDifficultyAdjuster:
    """Real-time difficulty adjustment based on child performance."""
    
    def __init__(self):
        self.difficulty_thresholds = {
            'success_rate_up': 0.85,  # Increase difficulty if success rate > 85%
            'success_rate_down': 0.60,  # Decrease difficulty if success rate < 60%
            'response_time_threshold': 30.0,  # Seconds
            'engagement_threshold': 0.70  # Engagement level threshold
        }
    
    def analyze_performance(self, profile: ChildProfile, recent_interactions: List[Dict]) -> DifficultyLevel:
        """Analyze recent performance and suggest difficulty adjustment."""
        if not recent_interactions:
            return profile.difficulty_level
        
        # Calculate recent performance metrics
        recent_success_rate = self._calculate_success_rate(recent_interactions[-5:])
        avg_response_time = self._calculate_avg_response_time(recent_interactions[-5:])
        engagement_level = self._calculate_engagement_level(recent_interactions[-3:])
        
        current_level = profile.difficulty_level.value
        
        # Difficulty adjustment logic
        if (recent_success_rate > self.difficulty_thresholds['success_rate_up'] and 
            engagement_level > self.difficulty_thresholds['engagement_threshold'] and
            avg_response_time < self.difficulty_thresholds['response_time_threshold']):
            # Child is performing well - increase difficulty
            new_level = min(4, current_level + 1)
        elif (recent_success_rate < self.difficulty_thresholds['success_rate_down'] or
              engagement_level < self.difficulty_thresholds['engagement_threshold']):
            # Child is struggling - decrease difficulty
            new_level = max(1, current_level - 1)
        else:
            # Maintain current difficulty
            new_level = current_level
        
        return DifficultyLevel(new_level)
    
    def _calculate_success_rate(self, interactions: List[Dict]) -> float:
        """Calculate success rate from recent interactions."""
        if not interactions:
            return 0.5
        
        successes = sum(1 for interaction in interactions if interaction.get('correct', False))
        return successes / len(interactions)
    
    def _calculate_avg_response_time(self, interactions: List[Dict]) -> float:
        """Calculate average response time."""
        if not interactions:
            return 15.0
        
        times = [interaction.get('response_time', 15.0) for interaction in interactions]
        return sum(times) / len(times)
    
    def _calculate_engagement_level(self, interactions: List[Dict]) -> float:
        """Calculate engagement level based on various factors."""
        if not interactions:
            return 0.5
        
        # Engagement factors: completion, response quality, session duration
        engagement_scores = []
        for interaction in interactions:
            score = 0.0
            if interaction.get('completed', False):
                score += 0.4
            if interaction.get('response_quality', 0) > 0.5:
                score += 0.3
            if interaction.get('session_duration', 0) > 300:  # 5+ minutes
                score += 0.3
            engagement_scores.append(score)
        
        return sum(engagement_scores) / len(engagement_scores)


class AdaptiveVocabularySystem:
    """Adaptive vocabulary introduction based on comprehension."""
    
    def __init__(self):
        self.vocabulary_levels = {
            1: {  # Ages 5-6
                'words': ['big', 'small', 'happy', 'sad', 'run', 'jump', 'red', 'blue'],
                'complexity': 'simple',
                'syllables': 1
            },
            2: {  # Ages 6-7
                'words': ['adventure', 'treasure', 'magical', 'courage', 'friendship', 'explore'],
                'complexity': 'moderate',
                'syllables': 2
            },
            3: {  # Ages 7-8
                'words': ['magnificent', 'mysterious', 'challenge', 'determined', 'discovery'],
                'complexity': 'intermediate',
                'syllables': 3
            },
            4: {  # Ages 8-9
                'words': ['extraordinary', 'magnificent', 'perseverance', 'imagination', 'accomplishment'],
                'complexity': 'advanced',
                'syllables': 4
            }
        }
    
    def get_appropriate_vocabulary(self, profile: ChildProfile, theme: str) -> List[str]:
        """Get age and skill-appropriate vocabulary for story."""
        vocab_level = min(4, max(1, int(profile.learning_metrics.vocabulary_level)))
        theme_words = self._get_theme_vocabulary(theme, vocab_level)
        base_words = self.vocabulary_levels[vocab_level]['words']
        
        return theme_words + base_words[:3]  # Limit to prevent overwhelm
    
    def _get_theme_vocabulary(self, theme: str, level: int) -> List[str]:
        """Get theme-specific vocabulary at appropriate level."""
        theme_vocab = {
            'dragons': {
                1: ['fire', 'cave', 'gold'],
                2: ['dragon', 'treasure', 'castle'],
                3: ['magnificent', 'breathe fire', 'guardian'],
                4: ['majestic', 'legendary', 'protective']
            },
            'pirates': {
                1: ['ship', 'sea', 'gold'],
                2: ['pirate', 'treasure', 'island'],
                3: ['adventure', 'navigation', 'courage'],
                4: ['expedition', 'cartographer', 'mariner']
            },
            'princesses': {
                1: ['crown', 'dress', 'nice'],
                2: ['princess', 'castle', 'kingdom'],
                3: ['royal', 'wisdom', 'leadership'],
                4: ['diplomacy', 'benevolent', 'governance']
            }
        }
        
        return theme_vocab.get(theme, {}).get(level, [])
    
    def assess_vocabulary_comprehension(self, response: str, target_words: List[str]) -> float:
        """Assess how well child understood vocabulary."""
        response_lower = response.lower()
        understood_words = sum(1 for word in target_words if word.lower() in response_lower)
        return understood_words / len(target_words) if target_words else 1.0


class LearningStyleDetector:
    """Detect learning style preferences from interaction patterns."""
    
    def __init__(self):
        self.visual_indicators = ['picture', 'see', 'look', 'color', 'bright', 'image']
        self.auditory_indicators = ['hear', 'sound', 'listen', 'music', 'voice', 'loud']
        self.kinesthetic_indicators = ['move', 'touch', 'feel', 'action', 'do', 'play']
    
    def detect_learning_style(self, profile: ChildProfile) -> LearningStyle:
        """Detect learning style from interaction history."""
        if not profile.interaction_history:
            return LearningStyle.MIXED
        
        visual_score = 0
        auditory_score = 0
        kinesthetic_score = 0
        
        for interaction in profile.interaction_history[-10:]:  # Analyze last 10 interactions
            response = interaction.get('response', '').lower()
            
            # Count indicators
            visual_score += sum(1 for indicator in self.visual_indicators if indicator in response)
            auditory_score += sum(1 for indicator in self.auditory_indicators if indicator in response)
            kinesthetic_score += sum(1 for indicator in self.kinesthetic_indicators if indicator in response)
        
        # Determine dominant style
        scores = {'visual': visual_score, 'auditory': auditory_score, 'kinesthetic': kinesthetic_score}
        max_score = max(scores.values())
        
        if max_score == 0:
            return LearningStyle.MIXED
        
        dominant_style = max(scores, key=scores.get)
        
        # Require significant difference to classify as single style
        total_score = sum(scores.values())
        if max_score / total_score < 0.5:
            return LearningStyle.MIXED
        
        return LearningStyle(dominant_style)


class InterestGraphBuilder:
    """Build and track child's interest patterns over time."""
    
    def __init__(self):
        self.theme_weights = {}
        self.interest_decay_factor = 0.95  # Daily decay to keep interests current
    
    def update_interest_graph(self, profile: ChildProfile, theme: str, engagement_score: float):
        """Update interest graph based on interaction."""
        if not hasattr(profile, 'interest_graph'):
            profile.interest_graph = {}
        
        current_weight = profile.interest_graph.get(theme, 0.0)
        # Update weight based on engagement (higher engagement = higher interest)
        new_weight = (current_weight * 0.8) + (engagement_score * 0.2)
        profile.interest_graph[theme] = new_weight
        
        # Apply decay to other themes to prioritize recent preferences
        for other_theme in profile.interest_graph:
            if other_theme != theme:
                profile.interest_graph[other_theme] *= self.interest_decay_factor
    
    def get_recommended_themes(self, profile: ChildProfile, num_recommendations: int = 3) -> List[str]:
        """Get theme recommendations based on interest graph."""
        if not hasattr(profile, 'interest_graph') or not profile.interest_graph:
            return ['dragons', 'pirates', 'princesses']  # Default themes
        
        # Sort themes by interest weight
        sorted_themes = sorted(
            profile.interest_graph.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [theme for theme, _ in sorted_themes[:num_recommendations]]


class RecommendationEngine:
    """Generate personalized story recommendations based on learning gaps."""
    
    def __init__(self):
        self.learning_objectives = {
            'math': ['counting', 'addition', 'subtraction', 'patterns', 'shapes'],
            'vocabulary': ['synonyms', 'definitions', 'context', 'spelling', 'rhyming'],
            'problem_solving': ['logic', 'creativity', 'critical_thinking', 'decision_making']
        }
    
    def generate_recommendations(self, profile: ChildProfile) -> List[Dict]:
        """Generate personalized story recommendations."""
        recommendations = []
        
        # Identify learning gaps
        learning_gaps = self._identify_learning_gaps(profile)
        
        # Get preferred themes
        interest_builder = InterestGraphBuilder()
        preferred_themes = interest_builder.get_recommended_themes(profile)
        
        # Generate recommendations addressing gaps with preferred themes
        for gap in learning_gaps[:3]:  # Top 3 gaps
            for theme in preferred_themes[:2]:  # Top 2 themes
                recommendation = {
                    'theme': theme,
                    'learning_focus': gap,
                    'difficulty_level': profile.difficulty_level.value,
                    'reason': f"Strengthen {gap} skills with {theme} adventures",
                    'estimated_duration': self._estimate_duration(profile, gap),
                    'confidence_score': self._calculate_confidence_score(profile, theme, gap)
                }
                recommendations.append(recommendation)
        
        # Sort by confidence score
        recommendations.sort(key=lambda x: x['confidence_score'], reverse=True)
        return recommendations[:5]  # Return top 5 recommendations
    
    def _identify_learning_gaps(self, profile: ChildProfile) -> List[str]:
        """Identify areas where child needs more practice."""
        gaps = []
        metrics = profile.learning_metrics
        
        # Check math skills
        if metrics.math_level < profile.age - 3:  # Behind expected level
            gaps.append('math')
        
        # Check vocabulary skills
        if metrics.vocabulary_level < profile.age - 4:
            gaps.append('vocabulary')
        
        # Check problem solving
        if metrics.problem_solving_level < profile.age - 4:
            gaps.append('problem_solving')
        
        # If no gaps, focus on strengths for continued growth
        if not gaps:
            if metrics.math_level >= metrics.vocabulary_level and metrics.math_level >= metrics.problem_solving_level:
                gaps.append('math')
            elif metrics.vocabulary_level >= metrics.problem_solving_level:
                gaps.append('vocabulary')
            else:
                gaps.append('problem_solving')
        
        return gaps
    
    def _estimate_duration(self, profile: ChildProfile, learning_focus: str) -> int:
        """Estimate story duration in minutes."""
        base_duration = 8  # Base 8 minutes
        
        # Adjust based on age and difficulty
        age_factor = (profile.age - 4) * 1.5
        difficulty_factor = profile.difficulty_level.value * 2
        
        return int(base_duration + age_factor + difficulty_factor)
    
    def _calculate_confidence_score(self, profile: ChildProfile, theme: str, learning_focus: str) -> float:
        """Calculate confidence score for recommendation."""
        score = 0.5  # Base score
        
        # Theme preference boost
        if hasattr(profile, 'interest_graph') and theme in profile.interest_graph:
            score += profile.interest_graph[theme] * 0.3
        
        # Learning need alignment
        gaps = self._identify_learning_gaps(profile)
        if learning_focus in gaps:
            score += 0.2
        
        # Success rate in similar content
        relevant_interactions = [
            i for i in profile.interaction_history
            if i.get('theme') == theme or i.get('learning_focus') == learning_focus
        ]
        if relevant_interactions:
            success_rate = sum(1 for i in relevant_interactions if i.get('correct', False)) / len(relevant_interactions)
            score += success_rate * 0.2
        
        return min(1.0, score)


class AdaptiveSystemManager:
    """Main manager for all adaptive learning features."""
    
    def __init__(self):
        self.difficulty_adjuster = DynamicDifficultyAdjuster()
        self.vocabulary_system = AdaptiveVocabularySystem()
        self.style_detector = LearningStyleDetector()
        self.interest_builder = InterestGraphBuilder()
        self.recommendation_engine = RecommendationEngine()
        self.profiles = {}  # In-memory profile storage
    
    def get_or_create_profile(self, child_name: str, age: int = 6) -> ChildProfile:
        """Get existing profile or create new one."""
        profile_key = self._generate_profile_key(child_name)
        
        if profile_key not in self.profiles:
            self.profiles[profile_key] = ChildProfile(
                name=child_name,
                age=age,
                learning_style=LearningStyle.MIXED,
                difficulty_level=DifficultyLevel.BEGINNER
            )
        
        return self.profiles[profile_key]
    
    def update_profile_from_interaction(self, profile: ChildProfile, interaction_data: Dict):
        """Update profile based on new interaction."""
        # Add interaction to history
        profile.interaction_history.append(interaction_data)
        
        # Update learning metrics
        self._update_learning_metrics(profile, interaction_data)
        
        # Update difficulty level
        new_difficulty = self.difficulty_adjuster.analyze_performance(profile, profile.interaction_history)
        profile.difficulty_level = new_difficulty
        
        # Update learning style
        profile.learning_style = self.style_detector.detect_learning_style(profile)
        
        # Update interest graph
        engagement_score = interaction_data.get('engagement_score', 0.5)
        theme = interaction_data.get('theme', 'unknown')
        self.interest_builder.update_interest_graph(profile, theme, engagement_score)
        
        # Update timestamp
        profile.last_updated = time.time()
    
    def get_adaptive_story_parameters(self, profile: ChildProfile, requested_theme: str) -> Dict:
        """Get adaptive parameters for story generation."""
        vocabulary_words = self.vocabulary_system.get_appropriate_vocabulary(profile, requested_theme)
        
        return {
            'difficulty_level': profile.difficulty_level.value,
            'learning_style': profile.learning_style.value,
            'vocabulary_words': vocabulary_words,
            'preferred_themes': getattr(profile, 'interest_graph', {}),
            'learning_metrics': asdict(profile.learning_metrics)
        }
    
    def get_recommendations(self, profile: ChildProfile) -> List[Dict]:
        """Get personalized story recommendations."""
        return self.recommendation_engine.generate_recommendations(profile)
    
    def _generate_profile_key(self, child_name: str) -> str:
        """Generate secure profile key."""
        return hashlib.sha256(child_name.lower().encode()).hexdigest()
    
    def generate_adaptive_story(self, child_profile: ChildProfile, theme: str, story_generator) -> Dict:
        """Generate an adaptive story based on child's profile and learning needs."""
        # Get adaptive parameters for story generation
        adaptive_params = self.get_adaptive_story_parameters(child_profile, theme)
        
        # Determine learning focus from child's profile
        learning_gaps = self.recommendation_engine._identify_learning_gaps(child_profile)
        learning_focus = learning_gaps[0] if learning_gaps else 'vocabulary'
        
        # Generate the story using the story generator
        story_text, explanation = story_generator.generate_adventure(
            theme=theme,
            child_name=child_profile.name,
            learning_focus=learning_focus
        )
        
        # Create story result dictionary
        story_result = {
            'story': story_text,
            'explanation': explanation,
            'vocabulary_focus': adaptive_params.get('vocabulary_words', []),
            'difficulty_level': adaptive_params.get('difficulty_level', 1),
            'learning_style': adaptive_params.get('learning_style', 'mixed'),
            'learning_focus': learning_focus
        }
        
        return story_result
    
    def _update_learning_metrics(self, profile: ChildProfile, interaction_data: Dict):
        """Update learning metrics based on interaction."""
        metrics = profile.learning_metrics
        
        # Update success rate (running average)
        if 'correct' in interaction_data:
            current_success = 1.0 if interaction_data['correct'] else 0.0
            metrics.success_rate = (metrics.success_rate * 0.9) + (current_success * 0.1)
        
        # Update response time
        if 'response_time' in interaction_data:
            response_time = interaction_data['response_time']
            metrics.response_time_avg = (metrics.response_time_avg * 0.8) + (response_time * 0.2)
        
        # Update comprehension score
        if 'comprehension_score' in interaction_data:
            comp_score = interaction_data['comprehension_score']
            metrics.comprehension_score = (metrics.comprehension_score * 0.8) + (comp_score * 0.2)
        
        # Update engagement level
        if 'engagement_score' in interaction_data:
            eng_score = interaction_data['engagement_score']
            metrics.engagement_level = (metrics.engagement_level * 0.8) + (eng_score * 0.2)
        
        # Update skill levels based on learning focus and success
        learning_focus = interaction_data.get('learning_focus', '')
        if interaction_data.get('correct', False):
            if 'math' in learning_focus.lower():
                metrics.math_level = min(4, metrics.math_level + 0.1)
            elif 'vocabulary' in learning_focus.lower():
                metrics.vocabulary_level = min(4, metrics.vocabulary_level + 0.1)
            elif 'problem' in learning_focus.lower():
                metrics.problem_solving_level = min(4, metrics.problem_solving_level + 0.1)