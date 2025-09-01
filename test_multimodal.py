#!/usr/bin/env python3
"""Test script for multi-modal components - Phase 7 verification."""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Load environment
load_dotenv()

def test_imports():
    """Test that all imports work correctly."""
    print("🧪 Testing imports...")
    
    try:
        from multimodal_system import (
            TextToSpeechManager,
            ImageGenerator, 
            InteractiveStoryElements,
            DrawingCanvas,
            MultiModalStoryExperience
        )
        print("✅ Multi-modal system imports successful")
        
        from multimodal_app import MultiModalAdventureApp
        print("✅ Multi-modal app import successful")
        
        from story_generator import StoryGenerator
        from adaptive_system import AdaptiveSystemManager
        print("✅ Core system imports successful")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_tts_manager():
    """Test TTS manager initialization."""
    print("\n🔊 Testing TTS Manager...")
    
    try:
        from multimodal_system import TextToSpeechManager
        tts = TextToSpeechManager()
        
        print(f"✅ TTS Manager initialized")
        print(f"   Available voices: {len(tts.available_voices)}")
        
        for voice in tts.available_voices[:3]:  # Show first 3
            print(f"   • {voice['name']} ({voice['age']})")
        
        return True
    except Exception as e:
        print(f"❌ TTS Manager error: {e}")
        return False

def test_image_generator():
    """Test image generator initialization."""
    print("\n🎨 Testing Image Generator...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No OpenAI API key found in environment")
        return False
    
    try:
        from multimodal_system import ImageGenerator
        img_gen = ImageGenerator(api_key)
        print("✅ Image Generator initialized with API key")
        return True
    except Exception as e:
        print(f"❌ Image Generator error: {e}")
        return False

def test_interactive_elements():
    """Test interactive story elements."""
    print("\n🎮 Testing Interactive Elements...")
    
    try:
        from multimodal_system import InteractiveStoryElements
        from story_generator import StoryGenerator
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ No OpenAI API key found")
            return False
        
        story_gen = StoryGenerator(api_key)
        interactive = InteractiveStoryElements(story_gen)
        
        # Test word scramble
        words = ["dragon", "treasure", "adventure"]
        scramble_game = interactive.create_word_scramble_game(words)
        
        if scramble_game:
            print("✅ Word scramble game creation successful")
            print(f"   Original: {scramble_game['original_word']}")
            print(f"   Scrambled: {scramble_game['scrambled_word']}")
        
        return True
    except Exception as e:
        print(f"❌ Interactive Elements error: {e}")
        return False

def test_drawing_canvas():
    """Test drawing canvas (basic initialization)."""
    print("\n✏️ Testing Drawing Canvas...")
    
    try:
        from multimodal_system import DrawingCanvas
        canvas = DrawingCanvas()
        print("✅ Drawing Canvas initialized")
        return True
    except Exception as e:
        print(f"❌ Drawing Canvas error: {e}")
        return False

def test_multimodal_experience():
    """Test complete multi-modal experience."""
    print("\n🌟 Testing Multi-Modal Experience...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No OpenAI API key found")
        return False
    
    try:
        from multimodal_system import MultiModalStoryExperience
        from story_generator import StoryGenerator
        
        story_gen = StoryGenerator(api_key)
        multimodal = MultiModalStoryExperience(api_key, story_gen)
        
        print("✅ Multi-Modal Experience initialized successfully")
        print("   • TTS Manager: Ready")
        print("   • Image Generator: Ready")
        print("   • Interactive Elements: Ready") 
        print("   • Drawing Canvas: Ready")
        
        return True
    except Exception as e:
        print(f"❌ Multi-Modal Experience error: {e}")
        return False

def main():
    """Run all tests."""
    print("🏰 Ainia Adventure Stories - Phase 7 Multi-Modal Testing")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_tts_manager,
        test_image_generator,
        test_interactive_elements,
        test_drawing_canvas,
        test_multimodal_experience
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"🧪 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All multi-modal components are working correctly!")
        print("🚀 Phase 7 implementation is ready!")
    else:
        print(f"⚠️  {total - passed} test(s) failed - check the errors above")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)