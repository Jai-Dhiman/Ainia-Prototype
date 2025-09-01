"""Performance testing and benchmarking for Ainia Adventure Stories."""

import time
import sys
import os
import statistics
from functools import wraps

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from learning_integrator import LearningIntegrator
from safety_validator import SafetyValidator
from prompt_builder import PromptBuilder


def benchmark(func):
    """Decorator to benchmark function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        return result, execution_time
    return wrapper


class PerformanceTester:
    """Performance testing and optimization analysis."""
    
    def __init__(self):
        self.learning_integrator = LearningIntegrator()
        self.safety_validator = SafetyValidator()
        self.prompt_builder = PromptBuilder()
        
    @benchmark
    def test_prompt_generation(self, theme, child_name, learning_focus, iterations=10):
        """Benchmark prompt generation speed."""
        for _ in range(iterations):
            self.prompt_builder.build_prompt(theme, child_name, learning_focus)
        return f"Generated {iterations} prompts"
    
    @benchmark
    def test_safety_validation(self, content, iterations=100):
        """Benchmark safety validation speed."""
        for _ in range(iterations):
            self.safety_validator.check_safety_principles(content)
        return f"Validated {iterations} content pieces"
    
    @benchmark
    def test_learning_integration(self, iterations=50):
        """Benchmark learning integration speed."""
        themes = ["dragons", "pirates", "princesses"]
        child_names = ["Emma", "Alex", "Sam"]
        
        for _ in range(iterations):
            for theme in themes:
                for child_name in child_names:
                    self.learning_integrator.embed_math_challenge(theme, child_name)
        
        return f"Generated {iterations * len(themes) * len(child_names)} learning prompts"
    
    def run_performance_analysis(self):
        """Run comprehensive performance analysis."""
        print("🚀 Performance Analysis Starting...")
        print("=" * 60)
        
        results = {}
        
        # Test 1: Prompt Generation Performance
        print("\n📝 Testing Prompt Generation Performance...")
        prompt_results = []
        for i in range(5):  # 5 test runs
            _, exec_time = self.test_prompt_generation("dragons", "Emma", "counting and addition", 20)
            prompt_results.append(exec_time)
        
        results['prompt_generation'] = {
            'avg_time_ms': statistics.mean(prompt_results),
            'min_time_ms': min(prompt_results),
            'max_time_ms': max(prompt_results),
            'std_dev_ms': statistics.stdev(prompt_results) if len(prompt_results) > 1 else 0
        }
        
        # Test 2: Safety Validation Performance
        print("🛡️ Testing Safety Validation Performance...")
        test_content = "Princess Emma found 3 magical flowers and 2 golden ones. How many flowers does she have?"
        safety_results = []
        for i in range(5):
            _, exec_time = self.test_safety_validation(test_content, 200)
            safety_results.append(exec_time)
        
        results['safety_validation'] = {
            'avg_time_ms': statistics.mean(safety_results),
            'min_time_ms': min(safety_results),
            'max_time_ms': max(safety_results),
            'std_dev_ms': statistics.stdev(safety_results) if len(safety_results) > 1 else 0
        }
        
        # Test 3: Learning Integration Performance
        print("📚 Testing Learning Integration Performance...")
        learning_results = []
        for i in range(3):
            _, exec_time = self.test_learning_integration(20)
            learning_results.append(exec_time)
        
        results['learning_integration'] = {
            'avg_time_ms': statistics.mean(learning_results),
            'min_time_ms': min(learning_results),
            'max_time_ms': max(learning_results),
            'std_dev_ms': statistics.stdev(learning_results) if len(learning_results) > 1 else 0
        }
        
        # Display Results
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE ANALYSIS RESULTS")
        print("=" * 60)
        
        for component, metrics in results.items():
            print(f"\n🎯 {component.replace('_', ' ').title()}")
            print(f"   Average Time: {metrics['avg_time_ms']:.2f}ms")
            print(f"   Min Time:     {metrics['min_time_ms']:.2f}ms")
            print(f"   Max Time:     {metrics['max_time_ms']:.2f}ms")
            print(f"   Std Dev:      {metrics['std_dev_ms']:.2f}ms")
        
        # Performance Assessment
        print("\n🏆 PERFORMANCE ASSESSMENT")
        print("-" * 30)
        
        # Assess each component
        assessments = []
        
        if results['prompt_generation']['avg_time_ms'] < 50:
            assessments.append("✅ Prompt Generation: Excellent (<50ms)")
        elif results['prompt_generation']['avg_time_ms'] < 100:
            assessments.append("⚠️ Prompt Generation: Good (<100ms)")
        else:
            assessments.append("❌ Prompt Generation: Needs optimization (>100ms)")
        
        if results['safety_validation']['avg_time_ms'] < 100:
            assessments.append("✅ Safety Validation: Excellent (<100ms)")
        elif results['safety_validation']['avg_time_ms'] < 200:
            assessments.append("⚠️ Safety Validation: Good (<200ms)")
        else:
            assessments.append("❌ Safety Validation: Needs optimization (>200ms)")
        
        if results['learning_integration']['avg_time_ms'] < 200:
            assessments.append("✅ Learning Integration: Excellent (<200ms)")
        elif results['learning_integration']['avg_time_ms'] < 400:
            assessments.append("⚠️ Learning Integration: Good (<400ms)")
        else:
            assessments.append("❌ Learning Integration: Needs optimization (>400ms)")
        
        for assessment in assessments:
            print(assessment)
        
        # Overall performance score
        excellent_count = len([a for a in assessments if "✅" in a])
        good_count = len([a for a in assessments if "⚠️" in a])
        needs_work_count = len([a for a in assessments if "❌" in a])
        
        if excellent_count == 3:
            print("\n🌟 OVERALL PERFORMANCE: EXCELLENT - Ready for production!")
        elif excellent_count + good_count == 3:
            print("\n👍 OVERALL PERFORMANCE: GOOD - Minor optimizations possible")
        else:
            print("\n🔧 OVERALL PERFORMANCE: NEEDS OPTIMIZATION")
        
        return results


def run_performance_tests():
    """Run all performance tests."""
    tester = PerformanceTester()
    return tester.run_performance_analysis()


if __name__ == "__main__":
    run_performance_tests()