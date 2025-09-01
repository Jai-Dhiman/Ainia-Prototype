"""Demo personas and scenarios for Ainia Adventure Stories."""

import streamlit as st
import time
from typing import Dict, List, Tuple


class ChildPersona:
    """Represents a child persona with specific characteristics."""
    
    def __init__(self, name: str, age: int, interests: List[str], 
                 learning_level: str, preferred_theme: str, 
                 learning_focus: str, description: str):
        self.name = name
        self.age = age
        self.interests = interests
        self.learning_level = learning_level
        self.preferred_theme = preferred_theme
        self.learning_focus = learning_focus
        self.description = description


class DemoScenarioRunner:
    """Runs demo scenarios for different child personas."""
    
    def __init__(self):
        self.personas = self._create_personas()
    
    def _create_personas(self) -> List[ChildPersona]:
        """Create diverse child personas for demo purposes."""
        return [
            ChildPersona(
                name="Emma",
                age=5,
                interests=["dragons", "magic", "friendship"],
                learning_level="beginner",
                preferred_theme="dragons",
                learning_focus="counting and addition",
                description="A curious 5-year-old who loves magical creatures and is just starting to learn basic math. She enjoys colorful stories and gets excited about dragons and fairy tales."
            ),
            ChildPersona(
                name="Alex",
                age=7,
                interests=["adventures", "pirates", "treasure hunting"],
                learning_level="intermediate",
                preferred_theme="pirates",
                learning_focus="vocabulary",
                description="An adventurous 7-year-old who dreams of sailing the seas. He's developing strong reading skills and loves learning new words, especially adventure-related vocabulary."
            ),
            ChildPersona(
                name="Sophia",
                age=9,
                interests=["problem solving", "royalty", "helping others"],
                learning_level="advanced",
                preferred_theme="princesses",
                learning_focus="problem solving",
                description="A thoughtful 9-year-old who enjoys complex stories and solving puzzles. She's interested in leadership and helping others, with strong analytical thinking skills."
            )
        ]
    
    def get_personas(self) -> List[ChildPersona]:
        """Get all available personas."""
        return self.personas
    
    def get_persona_by_name(self, name: str) -> ChildPersona:
        """Get a specific persona by name."""
        for persona in self.personas:
            if persona.name.lower() == name.lower():
                return persona
        return None
    
    def run_demo_scenario(self, persona: ChildPersona, story_generator) -> Tuple[str, str, Dict]:
        """Run a complete demo scenario for a persona."""
        print(f"🎭 Running demo scenario for {persona.name}...")
        
        # Generate story for the persona
        story, explanation = story_generator.generate_adventure(
            persona.preferred_theme,
            persona.name,
            persona.learning_focus
        )
        
        # Collect metrics
        metrics = {
            'persona_name': persona.name,
            'age': persona.age,
            'theme': persona.preferred_theme,
            'learning_focus': persona.learning_focus,
            'learning_level': persona.learning_level,
            'story_length': len(story) if story else 0,
            'story_generated': bool(story and explanation)
        }
        
        return story, explanation, metrics
    
    def display_persona_info(self, persona: ChildPersona):
        """Display persona information in Streamlit."""
        st.markdown(f"### 👶 Meet {persona.name} (Age {persona.age})")
        st.markdown(f"**Description:** {persona.description}")
        st.markdown(f"**Interests:** {', '.join(persona.interests)}")
        st.markdown(f"**Learning Level:** {persona.learning_level.title()}")
        st.markdown(f"**Favorite Theme:** {persona.preferred_theme.title()} 🎭")
        st.markdown(f"**Learning Focus:** {persona.learning_focus.title()} 📚")
    
    def run_all_demo_scenarios(self, story_generator) -> Dict:
        """Run demo scenarios for all personas."""
        print("🚀 Running demo scenarios for all personas...")
        print("=" * 60)
        
        all_results = {
            'scenarios': [],
            'summary': {
                'total_personas': len(self.personas),
                'successful_generations': 0,
                'failed_generations': 0
            }
        }
        
        for persona in self.personas:
            try:
                story, explanation, metrics = self.run_demo_scenario(persona, story_generator)
                
                scenario_result = {
                    'persona': persona,
                    'story': story,
                    'explanation': explanation,
                    'metrics': metrics,
                    'success': bool(story and explanation)
                }
                
                all_results['scenarios'].append(scenario_result)
                
                if scenario_result['success']:
                    all_results['summary']['successful_generations'] += 1
                    print(f"✅ {persona.name}: Story generated successfully")
                else:
                    all_results['summary']['failed_generations'] += 1
                    print(f"❌ {persona.name}: Story generation failed")
                
                # Brief pause between scenarios
                time.sleep(1)
                
            except Exception as e:
                print(f"💥 Error with {persona.name}: {e}")
                all_results['summary']['failed_generations'] += 1
        
        print("\n" + "=" * 60)
        print(f"📊 Demo Results Summary:")
        print(f"   Total Personas: {all_results['summary']['total_personas']}")
        print(f"   Successful: {all_results['summary']['successful_generations']}")
        print(f"   Failed: {all_results['summary']['failed_generations']}")
        
        success_rate = (all_results['summary']['successful_generations'] / 
                       all_results['summary']['total_personas']) * 100
        print(f"   Success Rate: {success_rate:.1f}%")
        
        return all_results


def create_demo_interface():
    """Create a Streamlit interface for demo personas."""
    st.markdown("## 🎭 Demo Personas")
    st.markdown("Explore how the app works with different types of children!")
    
    demo_runner = DemoScenarioRunner()
    personas = demo_runner.get_personas()
    
    # Persona selection
    persona_names = [persona.name for persona in personas]
    selected_name = st.selectbox("Choose a demo persona:", persona_names)
    
    if selected_name:
        selected_persona = demo_runner.get_persona_by_name(selected_name)
        demo_runner.display_persona_info(selected_persona)
        
        # Auto-populate form fields
        st.markdown("---")
        st.markdown("### 🎯 Persona's Adventure Preferences")
        st.markdown(f"**Theme:** {selected_persona.preferred_theme}")
        st.markdown(f"**Learning Focus:** {selected_persona.learning_focus}")
        
        if st.button(f"🚀 Generate {selected_persona.name}'s Adventure!", type="primary"):
            st.session_state.theme = selected_persona.preferred_theme
            st.session_state.demo_child_name = selected_persona.name
            st.session_state.demo_learning_focus = selected_persona.learning_focus
            st.success(f"🎉 Ready to create {selected_persona.name}'s personalized adventure!")


if __name__ == "__main__":
    # Test the demo personas
    demo_runner = DemoScenarioRunner()
    personas = demo_runner.get_personas()
    
    print("🎭 Demo Personas Created:")
    print("=" * 30)
    
    for persona in personas:
        print(f"\n👶 {persona.name} (Age {persona.age})")
        print(f"   Theme: {persona.preferred_theme}")
        print(f"   Learning: {persona.learning_focus}")
        print(f"   Level: {persona.learning_level}")
        print(f"   Description: {persona.description[:50]}...")
    
    print(f"\n✅ {len(personas)} personas ready for demo!")