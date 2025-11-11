"""
Model Accuracy and Performance Testing Suite
Run comprehensive accuracy tests and performance benchmarks
"""

from services.visualization_assistant import VisualizationAssistant
from services.metrics_tracker import MetricsTracker, run_accuracy_benchmark
import time


def main():
    """Run all accuracy and performance tests."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "BIZVIZ MODEL ACCURACY & PERFORMANCE TEST" + " " * 23 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")
    
    # Initialize
    assistant = VisualizationAssistant()
    tracker = MetricsTracker()
    
    # Run accuracy benchmark
    print("=" * 80)
    print("PART 1: ACCURACY TESTING")
    print("=" * 80)
    accuracy_data = run_accuracy_benchmark(assistant)
    
    # Run performance tests
    print("\n" + "=" * 80)
    print("PART 2: PERFORMANCE TESTING")
    print("=" * 80)
    
    test_goals = [
        "Compare monthly sales across regions",
        "Show growth trend of revenue over 5 years",
        "Display distribution of customer ages",
        "Show market share percentages by product",
        "Analyze relationship between price and demand",
        "Compare Q1 vs Q2 performance",
        "Track changes over time",
        "How many customers in each age bracket",
        "What percentage of total revenue",
        "Correlation between temperature and sales"
    ]
    
    print("\nRunning 10 performance tests...")
    
    for i, goal in enumerate(test_goals, 1):
        start = time.time()
        result = assistant.analyze_data_goal(goal)
        elapsed_ms = (time.time() - start) * 1000
        
        tracker.track_intent_detection(goal, result['intent'], elapsed_ms)
        tracker.track_recommendations(result['intent'], result['recommendations'], elapsed_ms)
        
        print(f"✓ Test {i}/10 completed in {elapsed_ms:.2f}ms")
    
    # Print performance report
    print("\n" + tracker.generate_performance_report())
    
    # Export metrics
    metrics_file = tracker.export_metrics('model_metrics_report.json')
    print(f"📊 Full metrics report saved to: {metrics_file}")
    
    # Generate summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Accuracy: {accuracy_data['overall_accuracy']:.2f}%")
    print(f"✅ Test Cases: {accuracy_data['total']}")
    print(f"✅ Performance Tests: {len(test_goals)}")
    
    perf = tracker.calculate_performance_metrics()
    print(f"✅ Avg Response Time: {perf['intent_detection']['avg_time_ms']:.2f}ms")
    
    if accuracy_data['overall_accuracy'] >= 90 and perf['intent_detection']['meets_benchmark']:
        print("\n🎉 MODEL IS PRODUCTION-READY!")
    elif accuracy_data['overall_accuracy'] >= 80:
        print("\n✅ Model performs well, suitable for use")
    else:
        print("\n⚠️  Model may need refinement")
    
    print("=" * 80)


if __name__ == "__main__":
    main()
