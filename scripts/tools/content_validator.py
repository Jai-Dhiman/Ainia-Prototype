"""Educational content quality validation for Ainia Adventure Stories."""

import re
import sys
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from demo_personas import DemoScenarioRunner
from learning_integrator import LearningIntegrator
from safety_validator import SafetyValidator


@dataclass
class ContentQualityMetrics:
    """Metrics for evaluating content quality."""
    age_appropriate_score: float
    educational_value_score: float
    engagement_score: float
    safety_score: float
    learning_alignment_score: float
    overall_score: float
    issues: List[str]
    recommendations: List[str]


class EducationalContentValidator:
    """Validates educational content quality and age-appropriateness."""
    
    def __init__(self):
        self.age_groups = {
            'early_childhood': (5, 6),    # Kindergarten
            'primary_lower': (7, 8),      # Grades 1-2  
            'primary_upper': (9, 10)      # Grades 3-4
        }
        
        # Age-appropriate vocabulary levels
        self.vocabulary_levels = {
            'early_childhood': {
                'max_syllables': 2,
                'max_word_length': 8,
                'complex_words_threshold': 0.05,  # Max 5% complex words
                'appropriate_words': ['friend', 'help', 'magic', 'treasure', 'adventure', 'kind', 'brave']
            },
            'primary_lower': {
                'max_syllables': 3,
                'max_word_length': 10,
                'complex_words_threshold': 0.10,
                'appropriate_words': ['mysterious', 'discover', 'challenge', 'journey', 'courage', 'wisdom']
            },
            'primary_upper': {
                'max_syllables': 4,
                'max_word_length': 12,
                'complex_words_threshold': 0.15,
                'appropriate_words': ['extraordinary', 'perseverance', 'determination', 'collaboration']
            }
        }
        
        # Learning objective patterns
        self.learning_patterns = {
            'counting_addition': {
                'math_keywords': ['count', 'add', 'total', 'altogether', 'how many', 'plus'],
                'number_range': (1, 20),  # Age-appropriate number range
                'operation_complexity': 'basic'
            },
            'vocabulary': {
                'vocab_keywords': ['word', 'means', 'definition', 'what does', 'vocabulary'],
                'context_clues': True,
                'word_complexity': 'age_appropriate'
            },
            'problem_solving': {
                'problem_keywords': ['problem', 'solution', 'how can', 'what if', 'help'],
                'logical_thinking': True,
                'creative_thinking': True
            }
        }
    
    def get_age_group(self, age: int) -> str:
        """Determine age group for given age."""
        for group, (min_age, max_age) in self.age_groups.items():
            if min_age <= age <= max_age:
                return group
        return 'primary_upper'  # Default for older kids
    
    def count_syllables(self, word: str) -> int:
        """Estimate syllable count in a word."""
        word = word.lower()
        vowels = 'aeiouy'
        syllables = 0
        prev_was_vowel = False
        
        for char in word:
            if char in vowels:
                if not prev_was_vowel:
                    syllables += 1
                prev_was_vowel = True
            else:
                prev_was_vowel = False
        
        # Handle silent e
        if word.endswith('e') and syllables > 1:
            syllables -= 1
        
        return max(1, syllables)  # Every word has at least 1 syllable
    
    def analyze_vocabulary_complexity(self, text: str, age_group: str) -> Dict:
        """Analyze vocabulary complexity for age group."""
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0, 'issues': ['No words found in text']}
        
        vocab_criteria = self.vocabulary_levels[age_group]
        
        # Analyze word complexity
        complex_words = 0
        long_words = 0
        high_syllable_words = 0
        
        for word in words:
            syllables = self.count_syllables(word)
            word_length = len(word)
            
            if syllables > vocab_criteria['max_syllables']:
                high_syllable_words += 1
            
            if word_length > vocab_criteria['max_word_length']:
                long_words += 1
            
            # Consider word complex if it's long OR has many syllables
            if (syllables > vocab_criteria['max_syllables'] or 
                word_length > vocab_criteria['max_word_length']):
                complex_words += 1
        
        complex_word_ratio = complex_words / total_words
        
        # Calculate score (lower complexity ratio = higher score)
        if complex_word_ratio <= vocab_criteria['complex_words_threshold']:
            vocab_score = 1.0
        elif complex_word_ratio <= vocab_criteria['complex_words_threshold'] * 2:
            vocab_score = 0.7
        else:
            vocab_score = 0.4
        
        issues = []
        if complex_word_ratio > vocab_criteria['complex_words_threshold']:
            issues.append(f"Vocabulary too complex: {complex_word_ratio:.1%} complex words (max {vocab_criteria['complex_words_threshold']:.1%})")
        
        return {
            'score': vocab_score,
            'total_words': total_words,
            'complex_words': complex_words,
            'complex_word_ratio': complex_word_ratio,
            'long_words': long_words,
            'high_syllable_words': high_syllable_words,
            'issues': issues
        }
    
    def validate_learning_integration(self, text: str, learning_focus: str) -> Dict:
        """Validate that learning objectives are properly integrated."""
        text_lower = text.lower()
        
        if 'counting' in learning_focus or 'addition' in learning_focus:
            patterns = self.learning_patterns['counting_addition']
            
            # Check for math keywords
            math_keywords_found = sum(1 for keyword in patterns['math_keywords'] 
                                    if keyword in text_lower)
            
            # Look for numbers in appropriate range
            numbers = re.findall(r'\b(\d+)\b', text)
            appropriate_numbers = [int(n) for n in numbers 
                                 if patterns['number_range'][0] <= int(n) <= patterns['number_range'][1]]
            
            # Check for clear math problem
            has_math_problem = bool(re.search(r'how many|\? *$', text_lower))
            
            score = 0.0
            if math_keywords_found >= 2:
                score += 0.4
            if len(appropriate_numbers) >= 2:
                score += 0.4
            if has_math_problem:
                score += 0.2
            
            issues = []
            if math_keywords_found < 2:
                issues.append("Insufficient math vocabulary integration")
            if len(appropriate_numbers) < 2:
                issues.append("Math problem needs appropriate numbers for age group")
            if not has_math_problem:
                issues.append("No clear math question posed")
            
            return {
                'score': score,
                'math_keywords_found': math_keywords_found,
                'numbers_found': len(numbers),
                'appropriate_numbers': len(appropriate_numbers),
                'has_math_problem': has_math_problem,
                'issues': issues
            }
        
        elif 'vocabulary' in learning_focus:
            patterns = self.learning_patterns['vocabulary']
            
            vocab_keywords_found = sum(1 for keyword in patterns['vocab_keywords'] 
                                     if keyword in text_lower)
            
            # Look for vocabulary challenge
            has_vocab_challenge = bool(re.search(r'what does.*mean|word.*is|vocabulary', text_lower))
            
            # Check for context clues
            has_context_clues = bool(re.search(r'because|since|like|such as|means', text_lower))
            
            score = 0.0
            if vocab_keywords_found >= 1:
                score += 0.4
            if has_vocab_challenge:
                score += 0.4
            if has_context_clues:
                score += 0.2
            
            issues = []
            if vocab_keywords_found < 1:
                issues.append("Insufficient vocabulary focus")
            if not has_vocab_challenge:
                issues.append("No clear vocabulary challenge presented")
            
            return {
                'score': score,
                'vocab_keywords_found': vocab_keywords_found,
                'has_vocab_challenge': has_vocab_challenge,
                'has_context_clues': has_context_clues,
                'issues': issues
            }
        
        elif 'problem solving' in learning_focus:
            patterns = self.learning_patterns['problem_solving']
            
            problem_keywords_found = sum(1 for keyword in patterns['problem_keywords'] 
                                       if keyword in text_lower)
            
            # Look for problem-solving scenario
            has_problem_scenario = bool(re.search(r'problem|challenge|help.*how|what.*do', text_lower))
            
            # Check for creative thinking prompts
            has_creative_prompt = bool(re.search(r'what if|imagine|creative|different way', text_lower))
            
            score = 0.0
            if problem_keywords_found >= 2:
                score += 0.4
            if has_problem_scenario:
                score += 0.4
            if has_creative_prompt:
                score += 0.2
            
            issues = []
            if problem_keywords_found < 2:
                issues.append("Insufficient problem-solving language")
            if not has_problem_scenario:
                issues.append("No clear problem-solving scenario presented")
            
            return {
                'score': score,
                'problem_keywords_found': problem_keywords_found,
                'has_problem_scenario': has_problem_scenario,
                'has_creative_prompt': has_creative_prompt,
                'issues': issues
            }
        
        return {'score': 0.0, 'issues': ['Unknown learning focus']}
    
    def assess_engagement_factors(self, text: str) -> Dict:
        """Assess factors that make content engaging for children."""
        text_lower = text.lower()
        
        # Positive engagement indicators
        engagement_words = ['adventure', 'exciting', 'magic', 'treasure', 'friend', 'fun', 'amazing', 'wonderful']
        engagement_count = sum(1 for word in engagement_words if word in text_lower)
        
        # Story elements
        has_character = bool(re.search(r'\b[A-Z][a-z]+\b', text))  # Proper nouns (likely characters)
        has_action = bool(re.search(r'went|found|discovered|helped|saved|explored', text_lower))
        has_dialogue = '"' in text or "'" in text
        has_question = '?' in text
        
        # Narrative structure
        has_beginning = bool(re.search(r'^(once|there was|in a|long ago)', text_lower))
        has_ending = bool(re.search(r'(the end|finally|at last|lived happily)$', text_lower))
        
        # Calculate engagement score
        score = 0.0
        if engagement_count >= 2:
            score += 0.3
        if has_character:
            score += 0.2
        if has_action:
            score += 0.2
        if has_question:
            score += 0.2
        if has_dialogue:
            score += 0.1
        
        issues = []
        recommendations = []
        
        if engagement_count < 2:
            issues.append("Limited engaging vocabulary")
            recommendations.append("Add more exciting and positive words")
        
        if not has_action:
            issues.append("Story lacks action elements")
            recommendations.append("Include more action verbs and dynamic events")
        
        if not has_question:
            issues.append("No interactive questions for child")
            recommendations.append("Add questions to engage the child directly")
        
        return {
            'score': min(score, 1.0),
            'engagement_words': engagement_count,
            'has_character': has_character,
            'has_action': has_action,
            'has_dialogue': has_dialogue,
            'has_question': has_question,
            'issues': issues,
            'recommendations': recommendations
        }
    
    def validate_content_quality(self, text: str, child_age: int, 
                               learning_focus: str, theme: str) -> ContentQualityMetrics:
        """Comprehensive content quality validation."""
        age_group = self.get_age_group(child_age)
        
        # Run all validations
        vocab_analysis = self.analyze_vocabulary_complexity(text, age_group)
        learning_analysis = self.validate_learning_integration(text, learning_focus)
        engagement_analysis = self.assess_engagement_factors(text)
        
        # Safety validation
        safety_validator = SafetyValidator()
        safety_score = 1.0 if safety_validator.check_safety_principles(text) else 0.0
        
        # Calculate overall scores
        age_appropriate_score = vocab_analysis['score']
        educational_value_score = learning_analysis['score']
        engagement_score = engagement_analysis['score']
        learning_alignment_score = learning_analysis['score']
        
        # Overall score (weighted average)
        overall_score = (
            age_appropriate_score * 0.25 +
            educational_value_score * 0.30 +
            engagement_score * 0.25 +
            safety_score * 0.20
        )
        
        # Collect all issues and recommendations
        all_issues = []
        all_issues.extend(vocab_analysis.get('issues', []))
        all_issues.extend(learning_analysis.get('issues', []))
        all_issues.extend(engagement_analysis.get('issues', []))
        
        all_recommendations = []
        all_recommendations.extend(engagement_analysis.get('recommendations', []))
        
        if safety_score < 1.0:
            all_issues.append("Content failed safety validation")
        
        return ContentQualityMetrics(
            age_appropriate_score=age_appropriate_score,
            educational_value_score=educational_value_score,
            engagement_score=engagement_score,
            safety_score=safety_score,
            learning_alignment_score=learning_alignment_score,
            overall_score=overall_score,
            issues=all_issues,
            recommendations=all_recommendations
        )
    
    def generate_quality_report(self, metrics: ContentQualityMetrics, 
                              child_name: str, theme: str, learning_focus: str) -> str:
        """Generate a detailed quality assessment report."""
        report = f"\n📋 CONTENT QUALITY REPORT - {child_name}\n"
        report += f"Theme: {theme.title()}, Learning Focus: {learning_focus.title()}\n"
        report += "=" * 50 + "\n"
        
        # Overall assessment
        if metrics.overall_score >= 0.8:
            report += "🌟 OVERALL QUALITY: EXCELLENT\n"
        elif metrics.overall_score >= 0.6:
            report += "👍 OVERALL QUALITY: GOOD\n"
        elif metrics.overall_score >= 0.4:
            report += "⚠️ OVERALL QUALITY: NEEDS IMPROVEMENT\n"
        else:
            report += "❌ OVERALL QUALITY: POOR\n"
        
        report += f"Overall Score: {metrics.overall_score:.2f}/1.00\n\n"
        
        # Detailed scores
        report += "📊 DETAILED SCORES:\n"
        report += f"   Age Appropriateness: {metrics.age_appropriate_score:.2f}/1.00\n"
        report += f"   Educational Value: {metrics.educational_value_score:.2f}/1.00\n"
        report += f"   Engagement Factor: {metrics.engagement_score:.2f}/1.00\n"
        report += f"   Safety Score: {metrics.safety_score:.2f}/1.00\n"
        report += f"   Learning Alignment: {metrics.learning_alignment_score:.2f}/1.00\n\n"
        
        # Issues found
        if metrics.issues:
            report += "⚠️ ISSUES IDENTIFIED:\n"
            for i, issue in enumerate(metrics.issues, 1):
                report += f"   {i}. {issue}\n"
            report += "\n"
        
        # Recommendations
        if metrics.recommendations:
            report += "💡 RECOMMENDATIONS:\n"
            for i, rec in enumerate(metrics.recommendations, 1):
                report += f"   {i}. {rec}\n"
            report += "\n"
        
        return report


def run_educational_content_validation():
    """Run educational content validation on all personas."""
    print("📚 Starting Educational Content Quality Validation...")
    print("=" * 60)
    
    validator = EducationalContentValidator()
    demo_runner = DemoScenarioRunner()
    personas = demo_runner.get_personas()
    learning_integrator = LearningIntegrator()
    
    validation_results = []
    
    for persona in personas:
        print(f"\n🧪 Validating content for {persona.name} (age {persona.age})...")
        
        # Generate sample content for validation
        if "counting" in persona.learning_focus or "addition" in persona.learning_focus:
            sample_content = learning_integrator.embed_math_challenge(persona.preferred_theme, persona.name)
        elif "vocabulary" in persona.learning_focus:
            sample_content = learning_integrator.embed_vocabulary_challenge(persona.preferred_theme, persona.name)
        else:
            sample_content = learning_integrator.embed_problem_solving_challenge(persona.preferred_theme, persona.name)
        
        if sample_content:
            # Validate content quality
            metrics = validator.validate_content_quality(
                sample_content, 
                persona.age, 
                persona.learning_focus, 
                persona.preferred_theme
            )
            
            # Generate report
            report = validator.generate_quality_report(
                metrics, 
                persona.name, 
                persona.preferred_theme, 
                persona.learning_focus
            )
            
            print(report)
            
            validation_results.append({
                'persona': persona.name,
                'metrics': metrics,
                'content': sample_content[:100] + "..." if len(sample_content) > 100 else sample_content
            })
        
        else:
            print(f"❌ Failed to generate content for {persona.name}")
    
    # Generate summary report
    print("\n" + "=" * 60)
    print("📈 VALIDATION SUMMARY")
    print("=" * 60)
    
    if validation_results:
        avg_overall_score = sum(r['metrics'].overall_score for r in validation_results) / len(validation_results)
        avg_educational_score = sum(r['metrics'].educational_value_score for r in validation_results) / len(validation_results)
        avg_engagement_score = sum(r['metrics'].engagement_score for r in validation_results) / len(validation_results)
        avg_age_appropriate_score = sum(r['metrics'].age_appropriate_score for r in validation_results) / len(validation_results)
        
        print(f"\n🎯 Average Scores:")
        print(f"   Overall Quality: {avg_overall_score:.2f}/1.00")
        print(f"   Educational Value: {avg_educational_score:.2f}/1.00")
        print(f"   Engagement: {avg_engagement_score:.2f}/1.00")
        print(f"   Age Appropriateness: {avg_age_appropriate_score:.2f}/1.00")
        
        # Quality assessment
        if avg_overall_score >= 0.8:
            print("\n🏆 ASSESSMENT: Content quality is EXCELLENT across all personas!")
        elif avg_overall_score >= 0.6:
            print("\n👍 ASSESSMENT: Content quality is GOOD with room for minor improvements")
        else:
            print("\n🔧 ASSESSMENT: Content quality needs improvement")
        
        # Count issues
        total_issues = sum(len(r['metrics'].issues) for r in validation_results)
        print(f"\n⚠️ Total Issues Found: {total_issues}")
        
        if total_issues == 0:
            print("✅ No content quality issues detected!")
    
    return validation_results


if __name__ == "__main__":
    run_educational_content_validation()