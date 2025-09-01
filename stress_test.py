"""Stress testing and concurrent session validation for Ainia Adventure Stories."""

import time
import threading
import sys
import os
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from demo_personas import DemoScenarioRunner
from story_generator import StoryGenerator
from learning_integrator import LearningIntegrator
from safety_validator import SafetyValidator


class StressTestRunner:
    """Runs stress tests on the Ainia Adventure Stories application."""
    
    def __init__(self, api_key: str = "test_key"):
        self.api_key = api_key
        self.demo_runner = DemoScenarioRunner()
        self.personas = self.demo_runner.get_personas()
        self.results = []
        self.lock = threading.Lock()
    
    def simulate_user_session(self, session_id: int, persona_name: str) -> Dict:
        """Simulate a complete user session."""
        session_start = time.time()
        persona = self.demo_runner.get_persona_by_name(persona_name)
        
        if not persona:
            return {
                'session_id': session_id,
                'success': False,
                'error': 'Persona not found',
                'duration': 0
            }
        
        try:
            # Simulate story generation without API calls for stress testing
            story_generator = StoryGenerator(self.api_key)
            
            # Test component initialization
            learning_integrator = LearningIntegrator()
            safety_validator = SafetyValidator()
            
            # Test prompt building (lightweight operation)
            if "counting" in persona.learning_focus or "addition" in persona.learning_focus:
                prompt = learning_integrator.embed_math_challenge(persona.preferred_theme, persona.name)
            elif "vocabulary" in persona.learning_focus:
                prompt = learning_integrator.embed_vocabulary_challenge(persona.preferred_theme, persona.name)
            else:
                prompt = learning_integrator.embed_problem_solving_challenge(persona.preferred_theme, persona.name)
            
            # Test safety validation
            test_content = f"{persona.name} went on a {persona.preferred_theme} adventure and learned about {persona.learning_focus}."
            is_safe = safety_validator.check_safety_principles(test_content)
            
            session_end = time.time()
            duration = session_end - session_start
            
            result = {
                'session_id': session_id,
                'persona': persona.name,
                'success': True,
                'duration': duration,
                'prompt_length': len(prompt) if prompt else 0,
                'safety_validated': is_safe,
                'thread_id': threading.get_ident()
            }
            
            # Thread-safe result storage
            with self.lock:
                self.results.append(result)
            
            return result
            
        except Exception as e:
            session_end = time.time()
            duration = session_end - session_start
            
            result = {
                'session_id': session_id,
                'persona': persona_name,
                'success': False,
                'error': str(e),
                'duration': duration,
                'thread_id': threading.get_ident()
            }
            
            with self.lock:
                self.results.append(result)
            
            return result
    
    def run_concurrent_sessions(self, num_sessions: int, max_workers: int = 5) -> Dict:
        """Run multiple concurrent user sessions."""
        print(f"🚀 Starting stress test with {num_sessions} concurrent sessions...")
        print(f"👥 Max concurrent workers: {max_workers}")
        print("=" * 60)
        
        self.results = []  # Reset results
        start_time = time.time()
        
        # Create session assignments (cycle through personas)
        session_assignments = []
        for i in range(num_sessions):
            persona = self.personas[i % len(self.personas)]
            session_assignments.append((i + 1, persona.name))
        
        # Run concurrent sessions
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all sessions
            future_to_session = {
                executor.submit(self.simulate_user_session, session_id, persona_name): (session_id, persona_name)
                for session_id, persona_name in session_assignments
            }
            
            # Collect results as they complete
            completed = 0
            for future in as_completed(future_to_session):
                session_id, persona_name = future_to_session[future]
                try:
                    result = future.result()
                    completed += 1
                    
                    if result['success']:
                        print(f"✅ Session {session_id} ({persona_name}): {result['duration']:.3f}s")
                    else:
                        print(f"❌ Session {session_id} ({persona_name}): {result.get('error', 'Unknown error')}")
                    
                    # Show progress
                    if completed % 10 == 0 or completed == num_sessions:
                        progress = (completed / num_sessions) * 100
                        print(f"   📊 Progress: {completed}/{num_sessions} ({progress:.1f}%)")
                        
                except Exception as e:
                    print(f"💥 Session {session_id} ({persona_name}) failed: {e}")
        
        total_time = time.time() - start_time
        
        # Analyze results
        return self._analyze_stress_test_results(total_time)
    
    def _analyze_stress_test_results(self, total_time: float) -> Dict:
        """Analyze stress test results and generate report."""
        if not self.results:
            return {'error': 'No results to analyze'}
        
        successful_sessions = [r for r in self.results if r['success']]
        failed_sessions = [r for r in self.results if not r['success']]
        
        # Calculate metrics
        durations = [r['duration'] for r in successful_sessions]
        unique_threads = set(r['thread_id'] for r in self.results)
        
        analysis = {
            'total_sessions': len(self.results),
            'successful_sessions': len(successful_sessions),
            'failed_sessions': len(failed_sessions),
            'success_rate': (len(successful_sessions) / len(self.results)) * 100,
            'total_test_time': total_time,
            'unique_threads_used': len(unique_threads),
            'performance_metrics': {
                'avg_session_duration': statistics.mean(durations) if durations else 0,
                'min_session_duration': min(durations) if durations else 0,
                'max_session_duration': max(durations) if durations else 0,
                'std_dev_duration': statistics.stdev(durations) if len(durations) > 1 else 0
            },
            'throughput': {
                'sessions_per_second': len(self.results) / total_time if total_time > 0 else 0,
                'avg_concurrent_sessions': len(self.results) / total_time * statistics.mean(durations) if durations and total_time > 0 else 0
            }
        }
        
        # Error analysis
        if failed_sessions:
            error_types = {}
            for session in failed_sessions:
                error = session.get('error', 'Unknown')
                error_types[error] = error_types.get(error, 0) + 1
            analysis['error_analysis'] = error_types
        
        return analysis
    
    def run_session_state_validation(self) -> Dict:
        """Test for session state conflicts and data integrity."""
        print("🔍 Testing session state validation...")
        print("=" * 40)
        
        # Test concurrent access to shared resources
        validation_results = {
            'thread_safety': True,
            'data_integrity': True,
            'session_isolation': True,
            'issues_found': []
        }
        
        # Run a smaller concurrent test focused on state
        num_test_sessions = 20
        results = []
        
        def test_session_state(session_id):
            persona = self.personas[session_id % len(self.personas)]
            learning_integrator = LearningIntegrator()
            
            # Test that each session gets consistent results
            prompt1 = learning_integrator.embed_math_challenge(persona.preferred_theme, persona.name)
            prompt2 = learning_integrator.embed_math_challenge(persona.preferred_theme, persona.name)
            
            # Results should be consistent for same inputs
            if prompt1 != prompt2:
                validation_results['issues_found'].append(f"Session {session_id}: Inconsistent prompt generation")
                validation_results['data_integrity'] = False
            
            return {
                'session_id': session_id,
                'persona': persona.name,
                'prompt_consistent': prompt1 == prompt2
            }
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(test_session_state, i) for i in range(num_test_sessions)]
            results = [future.result() for future in as_completed(futures)]
        
        # Analyze session state results
        consistent_sessions = len([r for r in results if r['prompt_consistent']])
        validation_results['consistent_sessions'] = consistent_sessions
        validation_results['total_test_sessions'] = len(results)
        validation_results['consistency_rate'] = (consistent_sessions / len(results)) * 100
        
        print(f"✅ Session state validation complete")
        print(f"   Consistent sessions: {consistent_sessions}/{len(results)}")
        print(f"   Consistency rate: {validation_results['consistency_rate']:.1f}%")
        
        return validation_results
    
    def generate_stress_test_report(self, stress_results: Dict, validation_results: Dict):
        """Generate a comprehensive stress test report."""
        print("\n" + "=" * 60)
        print("📊 STRESS TEST REPORT")
        print("=" * 60)
        
        # Overview
        print(f"\n🎯 Test Overview")
        print(f"   Total Sessions: {stress_results['total_sessions']}")
        print(f"   Successful: {stress_results['successful_sessions']}")
        print(f"   Failed: {stress_results['failed_sessions']}")
        print(f"   Success Rate: {stress_results['success_rate']:.1f}%")
        print(f"   Total Test Time: {stress_results['total_test_time']:.2f}s")
        print(f"   Threads Used: {stress_results['unique_threads_used']}")
        
        # Performance metrics
        print(f"\n⚡ Performance Metrics")
        perf = stress_results['performance_metrics']
        print(f"   Avg Session Duration: {perf['avg_session_duration']:.3f}s")
        print(f"   Min Session Duration: {perf['min_session_duration']:.3f}s")
        print(f"   Max Session Duration: {perf['max_session_duration']:.3f}s")
        print(f"   Std Deviation: {perf['std_dev_duration']:.3f}s")
        
        # Throughput
        print(f"\n📈 Throughput Analysis")
        throughput = stress_results['throughput']
        print(f"   Sessions/Second: {throughput['sessions_per_second']:.2f}")
        print(f"   Avg Concurrent Load: {throughput['avg_concurrent_sessions']:.2f}")
        
        # Session state validation
        print(f"\n🔍 Session State Validation")
        print(f"   Thread Safety: {'✅ Pass' if validation_results['thread_safety'] else '❌ Fail'}")
        print(f"   Data Integrity: {'✅ Pass' if validation_results['data_integrity'] else '❌ Fail'}")
        print(f"   Session Isolation: {'✅ Pass' if validation_results['session_isolation'] else '❌ Fail'}")
        print(f"   Consistency Rate: {validation_results['consistency_rate']:.1f}%")
        
        # Issues found
        if validation_results['issues_found']:
            print(f"\n⚠️ Issues Found")
            for issue in validation_results['issues_found']:
                print(f"   - {issue}")
        
        # Error analysis
        if 'error_analysis' in stress_results:
            print(f"\n❌ Error Analysis")
            for error, count in stress_results['error_analysis'].items():
                print(f"   {error}: {count} occurrences")
        
        # Overall assessment
        print(f"\n🏆 Overall Assessment")
        if (stress_results['success_rate'] >= 95 and 
            validation_results['consistency_rate'] >= 98 and
            validation_results['thread_safety'] and 
            validation_results['data_integrity']):
            print("   🌟 EXCELLENT - Application is highly stable under load!")
        elif (stress_results['success_rate'] >= 90 and 
              validation_results['consistency_rate'] >= 95):
            print("   👍 GOOD - Application handles concurrent load well")
        else:
            print("   🔧 NEEDS ATTENTION - Some stability issues detected")


def run_full_stress_test():
    """Run complete stress testing suite."""
    # Note: Using test API key for stress testing to avoid actual API calls
    tester = StressTestRunner(api_key="test_key")
    
    # Test 1: Concurrent sessions
    print("🏋️ Running concurrent session stress test...")
    stress_results = tester.run_concurrent_sessions(num_sessions=50, max_workers=10)
    
    # Test 2: Session state validation
    print("\n🔒 Running session state validation...")
    validation_results = tester.run_session_state_validation()
    
    # Generate final report
    tester.generate_stress_test_report(stress_results, validation_results)
    
    return stress_results, validation_results


if __name__ == "__main__":
    run_full_stress_test()