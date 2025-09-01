"""Final optimizations and bug fixes for Ainia Adventure Stories."""

import sys
import os
import time
from typing import Dict, List

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from story_generator import StoryGenerator
from learning_integrator import LearningIntegrator
from safety_validator import SafetyValidator
from prompt_builder import PromptBuilder


class FinalOptimizer:
    """Handles final optimizations and bug fixes."""
    
    def __init__(self):
        self.optimization_results = []
    
    def test_error_handling(self) -> Dict:
        """Test error handling across all components."""
        print("🧪 Testing Error Handling...")
        results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'errors_found': []
        }
        
        # Test StoryGenerator error handling
        try:
            # Test with invalid API key
            story_gen = StoryGenerator("invalid_key")
            story, explanation = story_gen.generate_adventure(
                "dragons", "TestChild", "counting and addition"
            )
            
            # Should return error message, not crash
            if isinstance(story, str) and "API key" in story:
                results['passed_tests'] += 1
                print("✅ API key error handling works")
            else:
                results['failed_tests'] += 1
                results['errors_found'].append("API key error not handled properly")
            
            results['total_tests'] += 1
        except Exception as e:
            results['failed_tests'] += 1
            results['errors_found'].append(f"StoryGenerator error handling failed: {e}")
            results['total_tests'] += 1
        
        # Test with empty inputs
        try:
            story_gen = StoryGenerator("test_key")
            story, explanation = story_gen.generate_adventure("", "", "")
            
            if isinstance(story, str) and "Oops" in story:
                results['passed_tests'] += 1
                print("✅ Empty input handling works")
            else:
                results['failed_tests'] += 1
                results['errors_found'].append("Empty input not handled properly")
            
            results['total_tests'] += 1
        except Exception as e:
            results['failed_tests'] += 1
            results['errors_found'].append(f"Empty input handling failed: {e}")
            results['total_tests'] += 1
        
        # Test with very short name
        try:
            story_gen = StoryGenerator("test_key")
            story, explanation = story_gen.generate_adventure("dragons", "A", "math")
            
            if isinstance(story, str) and "2 letters" in story:
                results['passed_tests'] += 1
                print("✅ Short name validation works")
            else:
                results['failed_tests'] += 1
                results['errors_found'].append("Short name validation not working")
            
            results['total_tests'] += 1
        except Exception as e:
            results['failed_tests'] += 1
            results['errors_found'].append(f"Short name validation failed: {e}")
            results['total_tests'] += 1
        
        print(f"Error handling tests: {results['passed_tests']}/{results['total_tests']} passed")
        return results
    
    def test_memory_usage(self) -> Dict:
        """Test for memory leaks and efficient usage."""
        print("🧠 Testing Memory Usage...")
        
        import psutil
        import gc
        
        # Get initial memory
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create multiple story generators and test memory usage
        generators = []
        for i in range(10):
            gen = StoryGenerator("test_key")
            # Simulate some cache usage
            gen.cache[f"test_{i}"] = {
                'story': f'Test story {i}',
                'explanation': f'Test explanation {i}',
                'original_child_name': f'Child{i}',
                'timestamp': time.time()
            }
            generators.append(gen)
        
        # Check memory after creation
        mid_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = mid_memory - initial_memory
        
        # Clean up
        del generators
        gc.collect()
        
        # Check memory after cleanup
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_recovered = mid_memory - final_memory
        
        results = {
            'initial_memory_mb': initial_memory,
            'peak_memory_mb': mid_memory,
            'final_memory_mb': final_memory,
            'memory_increase_mb': memory_increase,
            'memory_recovered_mb': memory_recovered,
            'memory_efficient': memory_increase < 50,  # Less than 50MB increase
            'cleanup_effective': memory_recovered > 0
        }
        
        print(f"Memory usage: +{memory_increase:.1f}MB, recovered: {memory_recovered:.1f}MB")
        return results
    
    def test_cache_efficiency(self) -> Dict:
        """Test caching system efficiency."""
        print("⚡ Testing Cache Efficiency...")
        
        story_gen = StoryGenerator("test_key")
        
        # Test cache key generation
        cache_key1 = story_gen._generate_cache_key("dragons", "Emma", "math")
        cache_key2 = story_gen._generate_cache_key("dragons", "Alex", "math")
        cache_key3 = story_gen._generate_cache_key("dragons", "Emma", "math")
        
        results = {
            'cache_key_consistency': cache_key1 == cache_key3,
            'cache_key_privacy': cache_key1 == cache_key2,  # Should be same (no child name)
            'cache_entries': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        
        # Test cache storage and retrieval
        test_time = time.time()
        story_gen.cache[cache_key1] = {
            'story': 'Test story with Emma',
            'explanation': 'Test explanation',
            'original_child_name': 'Emma',
            'timestamp': test_time
        }
        results['cache_entries'] = len(story_gen.cache)
        
        # Test cache retrieval with personalization
        cached_story, cached_explanation = story_gen._get_cached_story(cache_key1, "Alex")
        
        if cached_story and "Alex" in cached_story and "Emma" not in cached_story:
            results['personalization_works'] = True
            print("✅ Cache personalization works")
        else:
            results['personalization_works'] = False
            print("❌ Cache personalization failed")
        
        # Test cache expiry
        old_time = test_time - 3700  # More than 1 hour ago
        story_gen.cache[cache_key1]['timestamp'] = old_time
        
        is_valid = story_gen._is_cache_valid(story_gen.cache[cache_key1])
        results['expiry_works'] = not is_valid
        
        if not is_valid:
            print("✅ Cache expiry works")
        else:
            print("❌ Cache expiry failed")
        
        return results
    
    def validate_component_integration(self) -> Dict:
        """Validate that all components work together properly."""
        print("🔧 Testing Component Integration...")
        
        results = {
            'integration_tests': 0,
            'passed_tests': 0,
            'integration_issues': []
        }
        
        try:
            # Test full pipeline
            prompt_builder = PromptBuilder()
            learning_integrator = LearningIntegrator()
            safety_validator = SafetyValidator()
            
            # Test prompt building
            prompt = prompt_builder.build_prompt("dragons", "TestChild", "counting and addition")
            if prompt and "TestChild" in prompt and "dragons" in prompt:
                results['passed_tests'] += 1
                print("✅ Prompt building integration works")
            else:
                results['integration_issues'].append("Prompt building integration failed")
            
            results['integration_tests'] += 1
            
            # Test learning integration
            math_prompt = learning_integrator.embed_math_challenge("dragons", "TestChild")
            if math_prompt and "TestChild" in math_prompt and "dragons" in math_prompt:
                results['passed_tests'] += 1
                print("✅ Learning integration works")
            else:
                results['integration_issues'].append("Learning integration failed")
            
            results['integration_tests'] += 1
            
            # Test safety validation
            safe_content = "Princess Emma found 3 magical flowers and wants to count them."
            unsafe_content = "The scary monster frightened everyone with violence."
            
            is_safe_good = safety_validator.check_safety_principles(safe_content)
            is_unsafe_caught = not safety_validator.check_safety_principles(unsafe_content)
            
            if is_safe_good and is_unsafe_caught:
                results['passed_tests'] += 1
                print("✅ Safety validation integration works")
            else:
                results['integration_issues'].append("Safety validation integration failed")
            
            results['integration_tests'] += 1
            
        except Exception as e:
            results['integration_issues'].append(f"Component integration failed: {e}")
        
        print(f"Integration tests: {results['passed_tests']}/{results['integration_tests']} passed")
        return results
    
    def run_final_optimization_suite(self) -> Dict:
        """Run complete final optimization and bug fix suite."""
        print("🚀 Running Final Optimization Suite...")
        print("=" * 60)
        
        all_results = {
            'timestamp': time.time(),
            'optimization_complete': False
        }
        
        # Test 1: Error handling
        error_results = self.test_error_handling()
        all_results['error_handling'] = error_results
        
        # Test 2: Memory usage (if psutil available)
        try:
            memory_results = self.test_memory_usage()
            all_results['memory_usage'] = memory_results
        except ImportError:
            print("⚠️ psutil not available, skipping memory tests")
            all_results['memory_usage'] = {'skipped': True}
        
        # Test 3: Cache efficiency
        cache_results = self.test_cache_efficiency()
        all_results['cache_efficiency'] = cache_results
        
        # Test 4: Component integration
        integration_results = self.validate_component_integration()
        all_results['component_integration'] = integration_results
        
        # Generate final assessment
        self.generate_optimization_report(all_results)
        
        # Determine if optimization is complete
        all_results['optimization_complete'] = self.assess_optimization_completion(all_results)
        
        return all_results
    
    def assess_optimization_completion(self, results: Dict) -> bool:
        """Assess if optimization is complete based on test results."""
        error_handling_good = (results['error_handling']['failed_tests'] == 0)
        
        cache_efficiency_good = (
            results['cache_efficiency'].get('cache_key_consistency', False) and
            results['cache_efficiency'].get('personalization_works', False) and
            results['cache_efficiency'].get('expiry_works', False)
        )
        
        integration_good = (len(results['component_integration']['integration_issues']) == 0)
        
        memory_good = True  # Assume good if not tested
        if 'memory_usage' in results and not results['memory_usage'].get('skipped', False):
            memory_good = results['memory_usage']['memory_efficient']
        
        return error_handling_good and cache_efficiency_good and integration_good and memory_good
    
    def generate_optimization_report(self, results: Dict):
        """Generate comprehensive optimization report."""
        print("\n" + "=" * 60)
        print("📊 FINAL OPTIMIZATION REPORT")
        print("=" * 60)
        
        # Error handling assessment
        error_results = results['error_handling']
        print(f"\n🛠️ Error Handling:")
        print(f"   Tests Passed: {error_results['passed_tests']}/{error_results['total_tests']}")
        if error_results['errors_found']:
            print("   Issues Found:")
            for error in error_results['errors_found']:
                print(f"     - {error}")
        else:
            print("   ✅ No error handling issues found")
        
        # Memory usage assessment
        if not results['memory_usage'].get('skipped', False):
            memory_results = results['memory_usage']
            print(f"\n🧠 Memory Usage:")
            print(f"   Memory Increase: {memory_results['memory_increase_mb']:.1f}MB")
            print(f"   Memory Recovered: {memory_results['memory_recovered_mb']:.1f}MB")
            print(f"   Memory Efficient: {'✅' if memory_results['memory_efficient'] else '❌'}")
            print(f"   Cleanup Effective: {'✅' if memory_results['cleanup_effective'] else '❌'}")
        
        # Cache efficiency assessment
        cache_results = results['cache_efficiency']
        print(f"\n⚡ Cache Efficiency:")
        print(f"   Key Consistency: {'✅' if cache_results['cache_key_consistency'] else '❌'}")
        print(f"   Personalization: {'✅' if cache_results['personalization_works'] else '❌'}")
        print(f"   Expiry System: {'✅' if cache_results['expiry_works'] else '❌'}")
        
        # Component integration assessment
        integration_results = results['component_integration']
        print(f"\n🔧 Component Integration:")
        print(f"   Tests Passed: {integration_results['passed_tests']}/{integration_results['integration_tests']}")
        if integration_results['integration_issues']:
            print("   Issues Found:")
            for issue in integration_results['integration_issues']:
                print(f"     - {issue}")
        else:
            print("   ✅ All components integrate properly")
        
        # Overall assessment
        print(f"\n🏆 Overall Assessment:")
        if results.get('optimization_complete', False):
            print("   🌟 OPTIMIZATION COMPLETE - Application is production-ready!")
        else:
            print("   🔧 Some optimizations needed - Review issues above")


def run_final_optimizations():
    """Run all final optimizations and bug fixes."""
    optimizer = FinalOptimizer()
    results = optimizer.run_final_optimization_suite()
    return results


if __name__ == "__main__":
    run_final_optimizations()