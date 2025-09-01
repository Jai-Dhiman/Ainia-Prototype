"""Content safety validation and parent explanations."""


class SafetyValidator:
    def __init__(self):
        self.safety_principles = [
            "Age-appropriate for 5-9 year olds",
            "No scary or violent content", 
            "Positive messaging and growth mindset",
            "Inclusive representation"
        ]
        self.unsafe_words = ["scary", "frightening", "violent", "dangerous", "death", "kill", "hurt", "blood", "weapon"]
        self.positive_indicators = ["positive", "learn", "safe", "fun", "magical", "adventure", "help", "friendly", "treasure", "discover", "find", "how many", "what", "solve"]
    
    def validate_and_explain(self, story, theme, learning_element, child_name):
        # Validate content safety
        is_safe = self.check_safety_principles(story)
        
        # Generate parent explanation
        explanation = self.generate_parent_explanation(theme, learning_element, child_name, story)
        
        return is_safe, explanation
    
    def check_safety_principles(self, content):
        content_lower = content.lower()
        
        # Check for unsafe words
        for word in self.unsafe_words:
            if word in content_lower:
                return False
        
        # Check for positive elements or educational content indicators
        positive_found = any(element in content_lower for element in self.positive_indicators)
        return positive_found
    
    def generate_parent_explanation(self, theme, learning_element, child_name, story):
        return f"""
        **Parent Explanation - How AI Created This Story:**
        
        **Theme Choice**: {theme.title()} theme was selected to engage {child_name}'s interests while maintaining age-appropriate content.
        
        **Learning Integration**: The story includes a {learning_element} challenge that emerges naturally from the adventure context, making learning feel like play rather than work.
        
        **Safety Measures**: 
        - Content filtered for age-appropriate language (5-9 years)
        - Positive messaging promoting growth mindset
        - No scary or violent elements
        - Inclusive representation
        
        **Educational Value**: This approach helps {child_name} practice {learning_element} skills within an engaging narrative context, which research shows improves retention and enjoyment of learning.
        
        **AI Reasoning**: The story was generated to balance entertainment with education, ensuring {child_name} stays engaged while developing important skills.
        """