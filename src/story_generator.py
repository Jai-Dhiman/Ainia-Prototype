"""Story generation with GPT-4o and safety validation."""

import os
import hashlib
import time
import json
from openai import OpenAI
from learning_integrator import LearningIntegrator
from prompt_builder import PromptBuilder
from safety_validator import SafetyValidator


class StoryGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.safety_keywords = ["age-appropriate", "positive", "educational"]
        self.cache = {}  # In-memory cache for API responses
        self.cache_expiry = 3600  # Cache expires after 1 hour
        
    def _generate_cache_key(self, theme, child_name, learning_focus):
        """Generate a unique cache key for the request."""
        # Use theme and learning focus for caching, but not child name for privacy
        cache_string = f"{theme}_{learning_focus}"
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_entry):
        """Check if cache entry is still valid."""
        return time.time() - cache_entry['timestamp'] < self.cache_expiry
    
    def _get_cached_story(self, cache_key, child_name):
        """Get cached story and personalize it with child name."""
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            cached_data = self.cache[cache_key]
            # Personalize cached story with actual child name
            personalized_story = cached_data['story'].replace(
                cached_data['original_child_name'], 
                child_name
            )
            personalized_explanation = cached_data['explanation'].replace(
                cached_data['original_child_name'], 
                child_name
            )
            return personalized_story, personalized_explanation
        return None, None
    
    def generate_adventure(self, theme, child_name, learning_focus):
        prompt_builder = PromptBuilder()
        prompt = prompt_builder.build_prompt(theme, child_name, learning_focus)
        
        # Input validation
        if not theme or not child_name or not learning_focus:
            return "🤔 Oops! We need your theme, name, and learning focus to create your adventure!", None
        
        if len(child_name.strip()) < 2:
            return "😊 Please enter a name with at least 2 letters so we can make your story special!", None
        
        # Check cache first to reduce API calls
        cache_key = self._generate_cache_key(theme, child_name, learning_focus)
        cached_story, cached_explanation = self._get_cached_story(cache_key, child_name)
        if cached_story and cached_explanation:
            return cached_story, cached_explanation
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7,
                timeout=30  # Add timeout to prevent hanging
            )
            
            if not response.choices or not response.choices[0].message.content:
                return "🎭 The story magic didn't work this time. Let's try creating your adventure again!", None
            
            story_content = response.choices[0].message.content
            
            # Enhanced safety validation
            safety_validator = SafetyValidator()
            is_safe, parent_explanation = safety_validator.validate_and_explain(
                story_content, theme, learning_focus, child_name
            )
            
            if not is_safe:
                return "🛡️ Our safety wizards want to make sure your story is perfect. Let's try again!", None
            
            # Store in cache for future use
            self.cache[cache_key] = {
                'story': story_content,
                'explanation': parent_explanation,
                'original_child_name': child_name,
                'timestamp': time.time()
            }
            
            return story_content, parent_explanation
            
        except Exception as e:
            # User-friendly error messages
            error_msg = str(e).lower()
            if "api key" in error_msg or "authentication" in error_msg:
                return "🔑 There's an issue with the API key. Please ask a grown-up to check the setup!", None
            elif "timeout" in error_msg or "connection" in error_msg:
                return "🌐 The internet connection is a bit slow. Let's try again in a moment!", None
            elif "rate limit" in error_msg:
                return "⏱️ Too many stories are being created right now. Let's wait a moment and try again!", None
            else:
                return "🎪 Something unexpected happened, but don't worry! Let's try creating your adventure again!", None
    
    def build_constitutional_prompt(self, theme, child_name, learning_focus):
        return f"""
        Create a short adventure story for {child_name} (age 5-9) with theme: {theme}.
        Include exactly one {learning_focus} problem naturally in the story.
        Make it safe, positive, and engaging. End with the learning challenge.
        
        Safety guidelines:
        - Age-appropriate for 5-9 year olds
        - No scary or violent content
        - Positive messaging and growth mindset
        - Inclusive representation
        
        The story should be 2-3 paragraphs long and end with a simple question for the child to answer.
        """
    
    def validate_content_safety(self, content):
        # Simple content validation - can be expanded later
        unsafe_words = ["scary", "frightening", "violent", "dangerous"]
        for word in unsafe_words:
            if word.lower() in content.lower():
                return "Story content needs review - please try again."
        return content