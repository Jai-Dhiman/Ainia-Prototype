"""Multi-Question Story System with Real-Time Adaptive Difficulty."""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import time
from openai import OpenAI


class DifficultyLevel(Enum):
    """Real-time difficulty levels within a single story session."""
    EASY = 1
    MEDIUM = 2
    HARD = 3


class QuestionStatus(Enum):
    """Status of individual questions."""
    NOT_STARTED = "not_started"
    CURRENT = "current"
    COMPLETED_CORRECT = "completed_correct"
    COMPLETED_INCORRECT = "completed_incorrect"


@dataclass
class QuestionResult:
    """Result of a single question attempt."""
    question_number: int
    question_text: str
    user_answer: str
    correct_answer: str
    is_correct: bool
    difficulty_level: DifficultyLevel
    response_time: float
    timestamp: float
    explanation: str = ""
    

@dataclass
class StorySession:
    """Complete story session with multiple questions and adaptive difficulty."""
    story_id: str
    child_name: str
    theme: str
    learning_focus: str
    current_question: int
    difficulty_level: DifficultyLevel
    story_parts: List[str]
    questions: List[Dict]
    question_results: List[QuestionResult]
    session_start_time: float
    status: str = "in_progress"  # in_progress, completed, abandoned
    
    def __post_init__(self):
        if not self.story_parts:
            self.story_parts = []
        if not self.questions:
            self.questions = []
        if not self.question_results:
            self.question_results = []
    
    def get_current_story_text(self) -> str:
        """Get the cumulative story text up to current question."""
        return " ".join(self.story_parts[:self.current_question + 1])
    
    def get_progress_percentage(self) -> int:
        """Get completion percentage."""
        return int((len(self.question_results) / 3) * 100)
    
    def is_complete(self) -> bool:
        """Check if all 3 questions are complete."""
        return len(self.question_results) >= 3
    
    def get_success_rate(self) -> float:
        """Get current success rate in this session."""
        if not self.question_results:
            return 0.0
        correct_count = sum(1 for result in self.question_results if result.is_correct)
        return correct_count / len(self.question_results)


class AdaptiveDifficultyManager:
    """Manages real-time difficulty adjustment within story sessions."""
    
    def __init__(self):
        self.difficulty_parameters = {
            "math": {
                DifficultyLevel.EASY: {
                    "number_range": (1, 5),
                    "operations": ["addition"],
                    "max_numbers": 2,
                    "context": "simple counting"
                },
                DifficultyLevel.MEDIUM: {
                    "number_range": (1, 10),
                    "operations": ["addition", "subtraction"],
                    "max_numbers": 3,
                    "context": "basic arithmetic"
                },
                DifficultyLevel.HARD: {
                    "number_range": (5, 20),
                    "operations": ["addition", "subtraction", "multiplication"],
                    "max_numbers": 4,
                    "context": "multi-step problems"
                }
            },
            "vocabulary": {
                DifficultyLevel.EASY: {
                    "word_length": (3, 5),
                    "complexity": "simple",
                    "examples": ["big", "run", "happy", "blue", "cat"]
                },
                DifficultyLevel.MEDIUM: {
                    "word_length": (5, 8),
                    "complexity": "moderate",
                    "examples": ["adventure", "treasure", "magical", "courage"]
                },
                DifficultyLevel.HARD: {
                    "word_length": (8, 12),
                    "complexity": "advanced",
                    "examples": ["magnificent", "extraordinary", "perseverance"]
                }
            },
            "problem solving": {
                DifficultyLevel.EASY: {
                    "steps": 1,
                    "complexity": "direct solution",
                    "context": "obvious problem"
                },
                DifficultyLevel.MEDIUM: {
                    "steps": 2,
                    "complexity": "requires thinking",
                    "context": "moderate challenge"
                },
                DifficultyLevel.HARD: {
                    "steps": 3,
                    "complexity": "creative solution",
                    "context": "complex scenario"
                }
            }
        }
    
    def adjust_difficulty(self, current_level: DifficultyLevel, was_correct: bool, 
                         question_number: int) -> DifficultyLevel:
        """Adjust difficulty based on previous answer and question position."""
        if was_correct:
            # Increase difficulty for next question if correct
            if current_level == DifficultyLevel.EASY:
                return DifficultyLevel.MEDIUM
            elif current_level == DifficultyLevel.MEDIUM and question_number < 3:
                return DifficultyLevel.HARD
            else:
                return current_level  # Stay at current level
        else:
            # Decrease difficulty for next question if incorrect
            if current_level == DifficultyLevel.HARD:
                return DifficultyLevel.MEDIUM
            elif current_level == DifficultyLevel.MEDIUM:
                return DifficultyLevel.EASY
            else:
                return current_level  # Already at easiest level
    
    def get_difficulty_params(self, learning_focus: str, level: DifficultyLevel) -> Dict:
        """Get parameters for generating questions at specified difficulty."""
        clean_focus = learning_focus.replace("🔢 ", "").replace("📚 ", "").replace("🧩 ", "")
        
        # Map different focus names to parameter keys
        if "counting" in clean_focus.lower() or "addition" in clean_focus.lower() or "math" in clean_focus.lower():
            param_key = "math"
        elif "vocabulary" in clean_focus.lower():
            param_key = "vocabulary"
        elif "problem" in clean_focus.lower():
            param_key = "problem solving"
        else:
            param_key = clean_focus.lower()
        
        return self.difficulty_parameters.get(param_key, {}).get(level, {})


class MultiQuestionStoryGenerator:
    """Generates cohesive multi-question stories with adaptive difficulty."""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.difficulty_manager = AdaptiveDifficultyManager()
    
    def create_story_session(self, child_name: str, theme: str, learning_focus: str) -> StorySession:
        """Create a new multi-question story session."""
        story_id = f"{theme}_{learning_focus}_{int(time.time())}"
        
        return StorySession(
            story_id=story_id,
            child_name=child_name,
            theme=theme,
            learning_focus=learning_focus,
            current_question=0,
            difficulty_level=DifficultyLevel.EASY,  # Always start easy
            story_parts=[],
            questions=[],
            question_results=[],
            session_start_time=time.time()
        )
    
    def generate_next_story_part(self, session: StorySession) -> Tuple[str, Dict, str]:
        """Generate the next part of the story with embedded question."""
        question_num = session.current_question + 1
        
        # Get difficulty parameters
        difficulty_params = self.difficulty_manager.get_difficulty_params(
            session.learning_focus, session.difficulty_level
        )
        
        # Build context-aware prompt
        prompt = self._build_story_continuation_prompt(
            session, question_num, difficulty_params
        )
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7,
                timeout=30
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse the response
            story_data = self._parse_story_response(content)
            if not story_data:
                return self._generate_fallback_story_part(session, question_num)
            
            # Generate explanation
            explanation = self._generate_explanation(session, story_data, question_num)
            
            return story_data["story_part"], story_data, explanation
            
        except Exception as e:
            return self._generate_fallback_story_part(session, question_num)
    
    def _build_story_continuation_prompt(self, session: StorySession, question_num: int, 
                                       difficulty_params: Dict) -> str:
        """Build prompt for continuing the story with appropriate difficulty."""
        
        # Get previous story context
        previous_story = " ".join(session.story_parts)
        previous_context = f"\n\nPrevious story: {previous_story}" if previous_story else ""
        
        # Difficulty context
        difficulty_context = self._get_difficulty_context(session.learning_focus, 
                                                         session.difficulty_level, 
                                                         difficulty_params)
        
        # Position context
        position_context = {
            1: "This is the beginning of the adventure. Set up the story world and introduce the first challenge.",
            2: "This is the middle of the adventure. Build on the previous part and escalate the excitement.",
            3: "This is the climactic part of the adventure. Bring the story to a satisfying conclusion."
        }
        
        prompt = f"""
        Continue creating an adventure story for {session.child_name} (age 5-9) with theme: {session.theme}.
        
        {position_context.get(question_num, "")}
        
        Story Requirements:
        1. Create Part {question_num} of 3 total parts
        2. Include one {session.learning_focus} challenge naturally in this part
        3. {difficulty_context}
        4. Make it age-appropriate, positive, and engaging
        5. End this part with a clear question for {session.child_name} to answer
        
        {previous_context}
        
        Return ONLY valid JSON in this exact format:
        {{
            "story_part": "Story text for this part...",
            "question": "Clear question for the child",
            "correct_answer": "The correct answer",
            "explanation": "Why this answer is correct",
            "difficulty_level": "{session.difficulty_level.name.lower()}",
            "part_number": {question_num}
        }}
        """
        
        return prompt
    
    def _get_difficulty_context(self, learning_focus: str, level: DifficultyLevel, 
                              params: Dict) -> str:
        """Get context string for difficulty level."""
        clean_focus = learning_focus.replace("🔢 ", "").replace("📚 ", "").replace("🧩 ", "")
        
        if "math" in clean_focus.lower() or "counting" in clean_focus.lower():
            if level == DifficultyLevel.EASY:
                return "Make the math problem simple with numbers 1-5 and basic addition."
            elif level == DifficultyLevel.MEDIUM:
                return "Make the math problem moderate with numbers 1-10 and addition or subtraction."
            else:
                return "Make the math problem challenging with larger numbers and multiple steps."
        
        elif "vocabulary" in clean_focus.lower():
            if level == DifficultyLevel.EASY:
                return "Use a simple, common word that children know (3-5 letters)."
            elif level == DifficultyLevel.MEDIUM:
                return "Use a moderately complex word (5-8 letters) that expands vocabulary."
            else:
                return "Use an advanced, sophisticated word that challenges vocabulary."
        
        else:  # problem solving
            if level == DifficultyLevel.EASY:
                return "Make the problem simple with an obvious, direct solution."
            elif level == DifficultyLevel.MEDIUM:
                return "Make the problem require some thinking with 2 possible solutions."
            else:
                return "Make the problem complex requiring creative, multi-step thinking."
    
    def _parse_story_response(self, content: str) -> Optional[Dict]:
        """Parse JSON response from OpenAI."""
        try:
            # Try to parse as JSON directly
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    return None
            return None
    
    def _generate_fallback_story_part(self, session: StorySession, question_num: int) -> Tuple[str, Dict, str]:
        """Generate fallback story part if API call fails."""
        fallback_stories = {
            "dragons": f"Part {question_num}: {session.child_name} continues the dragon adventure...",
            "pirates": f"Part {question_num}: Captain {session.child_name} sails toward the next challenge...",
            "princesses": f"Part {question_num}: Princess {session.child_name} faces a new quest..."
        }
        
        story_part = fallback_stories.get(session.theme, 
                                         f"Part {question_num}: {session.child_name} continues the adventure...")
        
        question_data = {
            "story_part": story_part,
            "question": f"What do you think {session.child_name} should do next?",
            "correct_answer": "Any creative answer",
            "explanation": "Great thinking!",
            "difficulty_level": session.difficulty_level.name.lower(),
            "part_number": question_num
        }
        
        return story_part, question_data, "Story generated with backup system."
    
    def _generate_explanation(self, session: StorySession, story_data: Dict, question_num: int) -> str:
        """Generate explanation for parent dashboard."""
        return f"""
        **AI Story Part {question_num} for {session.child_name}:**
        
        🎭 **Theme Continuation:** {session.theme.title()} adventure continues building on previous parts.
        
        📚 **Learning Focus:** {session.learning_focus} embedded naturally at {session.difficulty_level.name.lower()} difficulty level.
        
        🧠 **Adaptive Logic:** Difficulty {'increased' if question_num > 1 and session.difficulty_level.value > 1 else 'maintained'} based on previous performance.
        
        🎯 **Question Design:** Part {question_num}/3 designed to maintain story flow while testing learning objectives.
        
        ✨ **Engagement:** Story progression keeps {session.child_name} invested in the complete adventure.
        """
    
    def process_answer(self, session: StorySession, user_answer: str, 
                      response_time: float) -> Tuple[bool, QuestionResult]:
        """Process user answer and determine if correct."""
        # Use the number of questions answered to get the correct question
        current_question_index = len(session.question_results)
        current_question = session.questions[current_question_index]
        correct_answer = current_question.get("correct_answer", "").strip().lower()
        user_answer_clean = str(user_answer).strip().lower()
        
        # Check if answer is correct
        is_correct = self._check_answer(user_answer_clean, correct_answer, session.learning_focus)
        
        # Create result record
        result = QuestionResult(
            question_number=current_question_index + 1,
            question_text=current_question.get("question", ""),
            user_answer=str(user_answer),
            correct_answer=current_question.get("correct_answer", ""),
            is_correct=is_correct,
            difficulty_level=session.difficulty_level,
            response_time=response_time,
            timestamp=time.time(),
            explanation=current_question.get("explanation", "")
        )
        
        # Add result to session
        session.question_results.append(result)
        
        # Update current_question index to keep it in sync
        session.current_question = len(session.question_results)
        
        # Adjust difficulty for next question (if not the last question)
        if len(session.question_results) < 3:  # Don't adjust after last question
            session.difficulty_level = self.difficulty_manager.adjust_difficulty(
                session.difficulty_level, is_correct, len(session.question_results)
            )
        
        # Mark session as completed if all questions are done
        if len(session.question_results) >= 3:
            session.status = "completed"
        
        return is_correct, result
    
    def _check_answer(self, user_answer: str, correct_answer: str, learning_focus: str) -> bool:
        """Check if user answer is correct based on learning focus."""
        clean_focus = learning_focus.replace("🔢 ", "").replace("📚 ", "").replace("🧩 ", "")
        
        if "math" in clean_focus.lower() or "counting" in clean_focus.lower():
            try:
                return float(user_answer) == float(correct_answer)
            except (ValueError, TypeError):
                return user_answer == correct_answer
        else:
            # For vocabulary and problem solving, accept close matches
            return user_answer in correct_answer or correct_answer in user_answer
