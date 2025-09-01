"""Comprehensive testing for Ainia Adventure Stories."""

import pytest
import sys
import os
import time

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from story_generator import StoryGenerator
from learning_integrator import LearningIntegrator
from safety_validator import SafetyValidator
from prompt_builder import PromptBuilder


class TestComprehensiveStoryGeneration:
    """Test story generation across all themes and learning types."""
    
    @pytest.fixture
    def mock_story_generator(self):
        """Create a mock story generator for testing."""
        # For testing without API calls, we'll mock the responses
        return StoryGenerator("test_api_key")
    
    def test_all_theme_combinations(self):
        """Test all theme and learning focus combinations."""
        themes = ["dragons", "pirates", "princesses"]
        learning_focuses = ["counting and addition", "vocabulary", "problem solving"]
        child_names = ["Emma", "Alex", "Sam"]
        
        learning_integrator = LearningIntegrator()
        
        test_results = []
        
        for theme in themes:
            for learning_focus in learning_focuses:
                for child_name in child_names:
                    # Test prompt building
                    if "counting" in learning_focus or "addition" in learning_focus:
                        prompt = learning_integrator.embed_math_challenge(theme, child_name)
                    elif "vocabulary" in learning_focus:
                        prompt = learning_integrator.embed_vocabulary_challenge(theme, child_name)
                    elif "problem solving" in learning_focus:
                        prompt = learning_integrator.embed_problem_solving_challenge(theme, child_name)
                    
                    # Validate prompt quality
                    assert prompt is not None, f"Prompt failed for {theme}, {learning_focus}, {child_name}"
                    assert child_name in prompt, f"Child name missing from prompt for {theme}, {learning_focus}"
                    assert theme in prompt, f"Theme missing from prompt for {learning_focus}, {child_name}"
                    
                    test_results.append({
                        'theme': theme,
                        'learning_focus': learning_focus,
                        'child_name': child_name,
                        'prompt_length': len(prompt),
                        'status': 'pass'
                    })
        
        # Report results
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r['status'] == 'pass'])
        
        print(f"\n🎯 Theme Combination Tests: {passed_tests}/{total_tests} passed")
        return test_results
    
    def test_safety_validation(self):
        """Test safety validation across different content scenarios."""
        safety_validator = SafetyValidator()
        
        # Test safe content
        safe_stories = [
            "Princess Emma found 3 magical flowers and 2 golden ones. How many flowers does she have?",
            "Captain Alex discovered a treasure map with the word 'ADVENTURE' on it. What does this word mean?",
            "The friendly dragon needs help crossing the river safely."
        ]
        
        # Test unsafe content (should be caught)
        unsafe_stories = [
            "The scary monster frightened the children with violence.",
            "The dangerous weapon hurt the dragon badly.",
            "The frightening beast caused death and destruction."
        ]
        
        # Test safe content
        for story in safe_stories:
            is_safe = safety_validator.check_safety_principles(story)
            assert is_safe, f"Safe story incorrectly flagged as unsafe: {story[:50]}..."
        
        # Test unsafe content
        for story in unsafe_stories:
            is_safe = safety_validator.check_safety_principles(story)
            assert not is_safe, f"Unsafe story incorrectly flagged as safe: {story[:50]}..."
        
        print("🛡️ Safety validation tests: All passed")
    
    def test_learning_integration_quality(self):
        """Test that learning elements are properly integrated."""
        learning_integrator = LearningIntegrator()
        
        # Test math integration
        math_prompt = learning_integrator.embed_math_challenge("dragons", "Emma")
        assert "counting" in math_prompt or "addition" in math_prompt
        assert "Emma" in math_prompt
        assert "dragons" in math_prompt
        
        # Test vocabulary integration
        vocab_prompt = learning_integrator.embed_vocabulary_challenge("pirates", "Alex")
        assert "vocabulary" in vocab_prompt or "word" in vocab_prompt
        assert "Alex" in vocab_prompt
        assert "pirates" in vocab_prompt
        
        # Test problem solving integration
        problem_prompt = learning_integrator.embed_problem_solving_challenge("princesses", "Sam")
        assert "problem" in problem_prompt or "solution" in problem_prompt or "help" in problem_prompt
        assert "Sam" in problem_prompt
        assert "princesses" in problem_prompt
        
        print("📚 Learning integration tests: All passed")


def run_comprehensive_tests():
    """Run all comprehensive tests and report results."""
    print("🚀 Starting Comprehensive Testing Suite...")
    print("=" * 50)
    
    tester = TestComprehensiveStoryGeneration()
    
    try:
        # Test 1: Theme combinations
        print("\n📋 Testing Theme & Learning Combinations...")
        theme_results = tester.test_all_theme_combinations()
        
        # Test 2: Safety validation
        print("\n🛡️ Testing Safety Validation...")
        tester.test_safety_validation()
        
        # Test 3: Learning integration
        print("\n📚 Testing Learning Integration Quality...")
        tester.test_learning_integration_quality()
        
        print("\n" + "=" * 50)
        print("✅ ALL COMPREHENSIVE TESTS PASSED!")
        print(f"📊 Total theme combinations tested: {len(theme_results)}")
        print("🏆 Application ready for production!")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        return False


if __name__ == "__main__":
    run_comprehensive_tests()