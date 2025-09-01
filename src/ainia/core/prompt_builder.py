"""Prompt building for different learning types."""

from .learning_integrator import LearningIntegrator


class PromptBuilder:
    def __init__(self):
        self.learning_integrator = LearningIntegrator()
        self.base_template = """
        Create a short adventure story for {child_name} (age 5-9) with theme: {theme}.
        Include exactly one {learning_type} problem naturally in the story.
        Make it safe, positive, and engaging. End with the learning challenge.
        """
    
    def build_prompt(self, theme, child_name, learning_type):
        if "counting" in learning_type or "addition" in learning_type:
            return self.learning_integrator.embed_math_challenge(theme, child_name)
        elif "vocabulary" in learning_type:
            return self.learning_integrator.embed_vocabulary_challenge(theme, child_name)
        elif "problem solving" in learning_type:
            return self.learning_integrator.embed_problem_solving_challenge(theme, child_name)
        else:
            return self.base_template.format(
                theme=theme, child_name=child_name, learning_type=learning_type
            )