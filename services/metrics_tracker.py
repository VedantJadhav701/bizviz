"""
Metrics Tracking and Model Evaluation Module
Tracks accuracy, performance, and model effectiveness for the BizViz Data Visualization Assistant
"""

import time
import json
from typing import Dict, List, Any, Tuple
from datetime import datetime
import pandas as pd
from collections import defaultdict


class MetricsTracker:
    """Tracks and analyzes model performance metrics."""
    
    def __init__(self):
        self.metrics = {
            'intent_detection': {
                'total_requests': 0,
                'by_intent': defaultdict(int),
                'confidence_scores': [],
                'processing_times': []
            },
            'recommendations': {
                'total_generated': 0,
                'by_chart_type': defaultdict(int),
                'average_response_time': []
            },
            'data_analysis': {
                'files_analyzed': 0,
                'total_rows_processed': 0,
                'insights_generated': 0,
                'charts_created': 0,
                'processing_times': [],
                'file_sizes': []
            },
            'errors': {
                'total_errors': 0,
                'by_type': defaultdict(int)
            }
        }
        
        # Ground truth for validation
        self.ground_truth = self._load_ground_truth()
        
        # Performance benchmarks
        self.benchmarks = {
            'intent_detection_time_ms': 50,  # Target: < 50ms
            'recommendation_time_ms': 100,    # Target: < 100ms
            'file_analysis_time_per_mb_ms': 1000  # Target: < 1 second per MB
        }
    
    def _load_ground_truth(self) -> List[Dict[str, str]]:
        """Load ground truth dataset for accuracy validation."""
        return [
            # Comparison intents
            {"goal": "Compare monthly sales across regions", "expected_intent": "comparison"},
            {"goal": "Compare Q1 vs Q2 performance", "expected_intent": "comparison"},
            {"goal": "Which product category performs better", "expected_intent": "comparison"},
            {"goal": "Difference between online and offline sales", "expected_intent": "comparison"},
            {"goal": "Ranking of stores by revenue", "expected_intent": "comparison"},
            
            # Trend intents
            {"goal": "Show growth trend of revenue over 5 years", "expected_intent": "trend"},
            {"goal": "Track changes in customer satisfaction over time", "expected_intent": "trend"},
            {"goal": "Display historical sales data month by month", "expected_intent": "trend"},
            {"goal": "Show progress of project completion over weeks", "expected_intent": "trend"},
            {"goal": "Year over year revenue growth", "expected_intent": "trend"},
            
            # Distribution intents
            {"goal": "Display distribution of customer ages", "expected_intent": "distribution"},
            {"goal": "How many customers in each income bracket", "expected_intent": "distribution"},
            {"goal": "Frequency of purchases by time of day", "expected_intent": "distribution"},
            {"goal": "Spread of test scores across students", "expected_intent": "distribution"},
            {"goal": "Range of product prices in catalog", "expected_intent": "distribution"},
            
            # Proportion intents
            {"goal": "Show market share percentages by product", "expected_intent": "proportion"},
            {"goal": "What percentage of total revenue comes from each region", "expected_intent": "proportion"},
            {"goal": "Composition of expenses by category", "expected_intent": "proportion"},
            {"goal": "Share of budget allocated to each department", "expected_intent": "proportion"},
            {"goal": "Portion of customers by subscription type", "expected_intent": "proportion"},
            
            # Relationship intents
            {"goal": "Analyze relationship between price and demand", "expected_intent": "relationship"},
            {"goal": "Correlation between temperature and ice cream sales", "expected_intent": "relationship"},
            {"goal": "Examine impact of advertising spend on revenue", "expected_intent": "relationship"},
            {"goal": "How does employee count affect productivity", "expected_intent": "relationship"},
            {"goal": "Association between study hours and exam scores", "expected_intent": "relationship"},
        ]
    
    def track_intent_detection(self, data_goal: str, detected_intent: str, 
                               processing_time_ms: float, confidence: float = None) -> None:
        """Track intent detection metrics."""
        self.metrics['intent_detection']['total_requests'] += 1
        self.metrics['intent_detection']['by_intent'][detected_intent] += 1
        self.metrics['intent_detection']['processing_times'].append(processing_time_ms)
        
        if confidence is not None:
            self.metrics['intent_detection']['confidence_scores'].append(confidence)
    
    def track_recommendations(self, intent: str, recommendations: List[Dict], 
                             processing_time_ms: float) -> None:
        """Track recommendation generation metrics."""
        self.metrics['recommendations']['total_generated'] += len(recommendations)
        self.metrics['recommendations']['average_response_time'].append(processing_time_ms)
        
        for rec in recommendations:
            chart_type = rec.get('name', 'unknown')
            self.metrics['recommendations']['by_chart_type'][chart_type] += 1
    
    def track_data_analysis(self, file_size_bytes: int, num_rows: int, 
                           num_insights: int, num_charts: int, 
                           processing_time_ms: float) -> None:
        """Track data analysis metrics."""
        self.metrics['data_analysis']['files_analyzed'] += 1
        self.metrics['data_analysis']['total_rows_processed'] += num_rows
        self.metrics['data_analysis']['insights_generated'] += num_insights
        self.metrics['data_analysis']['charts_created'] += num_charts
        self.metrics['data_analysis']['processing_times'].append(processing_time_ms)
        self.metrics['data_analysis']['file_sizes'].append(file_size_bytes / (1024 * 1024))  # MB
    
    def track_error(self, error_type: str) -> None:
        """Track errors."""
        self.metrics['errors']['total_errors'] += 1
        self.metrics['errors']['by_type'][error_type] += 1
    
    def calculate_intent_accuracy(self, assistant) -> Dict[str, Any]:
        """Calculate intent detection accuracy using ground truth."""
        if not self.ground_truth:
            return {"error": "No ground truth data available"}
        
        correct = 0
        total = len(self.ground_truth)
        results = []
        confusion_matrix = defaultdict(lambda: defaultdict(int))
        
        for test_case in self.ground_truth:
            goal = test_case['goal']
            expected = test_case['expected_intent']
            
            # Detect intent
            start_time = time.time()
            detected = assistant.detect_intent(goal)
            processing_time = (time.time() - start_time) * 1000  # ms
            
            # Track result
            is_correct = (detected == expected)
            if is_correct:
                correct += 1
            
            # Update confusion matrix
            confusion_matrix[expected][detected] += 1
            
            results.append({
                'goal': goal,
                'expected': expected,
                'detected': detected,
                'correct': is_correct,
                'processing_time_ms': processing_time
            })
        
        accuracy = (correct / total) * 100 if total > 0 else 0
        
        # Calculate per-intent accuracy
        per_intent_accuracy = {}
        for intent in ['comparison', 'trend', 'distribution', 'proportion', 'relationship']:
            intent_cases = [r for r in results if r['expected'] == intent]
            if intent_cases:
                intent_correct = sum(1 for r in intent_cases if r['correct'])
                per_intent_accuracy[intent] = (intent_correct / len(intent_cases)) * 100
        
        return {
            'overall_accuracy': accuracy,
            'correct': correct,
            'total': total,
            'per_intent_accuracy': per_intent_accuracy,
            'confusion_matrix': dict(confusion_matrix),
            'detailed_results': results,
            'average_processing_time_ms': sum(r['processing_time_ms'] for r in results) / len(results)
        }
    
    def calculate_performance_metrics(self) -> Dict[str, Any]:
        """Calculate performance metrics."""
        intent_times = self.metrics['intent_detection']['processing_times']
        recommendation_times = self.metrics['recommendations']['average_response_time']
        analysis_times = self.metrics['data_analysis']['processing_times']
        
        return {
            'intent_detection': {
                'avg_time_ms': sum(intent_times) / len(intent_times) if intent_times else 0,
                'min_time_ms': min(intent_times) if intent_times else 0,
                'max_time_ms': max(intent_times) if intent_times else 0,
                'meets_benchmark': (sum(intent_times) / len(intent_times) if intent_times else 0) < self.benchmarks['intent_detection_time_ms']
            },
            'recommendations': {
                'avg_time_ms': sum(recommendation_times) / len(recommendation_times) if recommendation_times else 0,
                'meets_benchmark': (sum(recommendation_times) / len(recommendation_times) if recommendation_times else 0) < self.benchmarks['recommendation_time_ms']
            },
            'data_analysis': {
                'avg_time_ms': sum(analysis_times) / len(analysis_times) if analysis_times else 0,
                'avg_time_per_mb_ms': self._calculate_time_per_mb(),
                'meets_benchmark': self._calculate_time_per_mb() < self.benchmarks['file_analysis_time_per_mb_ms']
            }
        }
    
    def _calculate_time_per_mb(self) -> float:
        """Calculate average processing time per MB."""
        times = self.metrics['data_analysis']['processing_times']
        sizes = self.metrics['data_analysis']['file_sizes']
        
        if not times or not sizes:
            return 0
        
        time_per_mb = [t / s if s > 0 else 0 for t, s in zip(times, sizes)]
        return sum(time_per_mb) / len(time_per_mb) if time_per_mb else 0
    
    def get_summary_report(self) -> Dict[str, Any]:
        """Generate comprehensive summary report."""
        return {
            'timestamp': datetime.now().isoformat(),
            'intent_detection': {
                'total_requests': self.metrics['intent_detection']['total_requests'],
                'distribution': dict(self.metrics['intent_detection']['by_intent']),
                'avg_confidence': sum(self.metrics['intent_detection']['confidence_scores']) / len(self.metrics['intent_detection']['confidence_scores']) if self.metrics['intent_detection']['confidence_scores'] else None
            },
            'recommendations': {
                'total_generated': self.metrics['recommendations']['total_generated'],
                'chart_distribution': dict(self.metrics['recommendations']['by_chart_type'])
            },
            'data_analysis': {
                'files_analyzed': self.metrics['data_analysis']['files_analyzed'],
                'total_rows_processed': self.metrics['data_analysis']['total_rows_processed'],
                'insights_generated': self.metrics['data_analysis']['insights_generated'],
                'charts_created': self.metrics['data_analysis']['charts_created']
            },
            'errors': {
                'total': self.metrics['errors']['total_errors'],
                'by_type': dict(self.metrics['errors']['by_type'])
            }
        }
    
    def export_metrics(self, filename: str = 'metrics_report.json') -> str:
        """Export metrics to JSON file."""
        report = {
            'summary': self.get_summary_report(),
            'performance': self.calculate_performance_metrics(),
            'raw_metrics': {
                'intent_detection': {
                    k: v if not isinstance(v, defaultdict) else dict(v)
                    for k, v in self.metrics['intent_detection'].items()
                },
                'recommendations': self.metrics['recommendations'],
                'data_analysis': self.metrics['data_analysis'],
                'errors': {
                    'total_errors': self.metrics['errors']['total_errors'],
                    'by_type': dict(self.metrics['errors']['by_type'])
                }
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filename
    
    def generate_accuracy_report(self, assistant) -> str:
        """Generate detailed accuracy report."""
        accuracy_data = self.calculate_intent_accuracy(assistant)
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    BIZVIZ MODEL ACCURACY REPORT                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 OVERALL ACCURACY
{'─' * 80}
Intent Detection Accuracy: {accuracy_data['overall_accuracy']:.2f}%
Correct Predictions: {accuracy_data['correct']}/{accuracy_data['total']}
Average Processing Time: {accuracy_data['average_processing_time_ms']:.2f}ms

📈 PER-INTENT ACCURACY
{'─' * 80}
"""
        for intent, acc in accuracy_data['per_intent_accuracy'].items():
            report += f"{intent.capitalize():15} : {acc:6.2f}%\n"
        
        report += f"""
🔄 CONFUSION MATRIX
{'─' * 80}
"""
        # Format confusion matrix
        intents = ['comparison', 'trend', 'distribution', 'proportion', 'relationship']
        report += f"{'Expected':15} | "
        for intent in intents:
            report += f"{intent[:3]:>5} "
        report += "\n" + "─" * 80 + "\n"
        
        for expected in intents:
            report += f"{expected:15} | "
            for detected in intents:
                count = accuracy_data['confusion_matrix'].get(expected, {}).get(detected, 0)
                report += f"{count:>5} "
            report += "\n"
        
        report += f"""
✅ MODEL QUALITY RATING
{'─' * 80}
"""
        overall = accuracy_data['overall_accuracy']
        if overall >= 95:
            rating = "EXCELLENT ⭐⭐⭐⭐⭐"
            note = "Model is production-ready with exceptional accuracy"
        elif overall >= 90:
            rating = "VERY GOOD ⭐⭐⭐⭐"
            note = "Model performs well and is suitable for production"
        elif overall >= 80:
            rating = "GOOD ⭐⭐⭐"
            note = "Model is reliable but may benefit from refinement"
        elif overall >= 70:
            rating = "FAIR ⭐⭐"
            note = "Model needs improvement for production use"
        else:
            rating = "NEEDS IMPROVEMENT ⭐"
            note = "Model requires significant refinement"
        
        report += f"Rating: {rating}\n"
        report += f"Note: {note}\n"
        report += f"\n{'═' * 80}\n"
        
        return report
    
    def generate_performance_report(self) -> str:
        """Generate detailed performance report."""
        perf = self.calculate_performance_metrics()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   BIZVIZ PERFORMANCE METRICS REPORT                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

⚡ INTENT DETECTION PERFORMANCE
{'─' * 80}
Average Time: {perf['intent_detection']['avg_time_ms']:.2f}ms
Min Time: {perf['intent_detection']['min_time_ms']:.2f}ms
Max Time: {perf['intent_detection']['max_time_ms']:.2f}ms
Benchmark: {self.benchmarks['intent_detection_time_ms']}ms
Status: {'✅ MEETS BENCHMARK' if perf['intent_detection']['meets_benchmark'] else '⚠️  EXCEEDS BENCHMARK'}

📋 RECOMMENDATION GENERATION
{'─' * 80}
Average Time: {perf['recommendations']['avg_time_ms']:.2f}ms
Benchmark: {self.benchmarks['recommendation_time_ms']}ms
Status: {'✅ MEETS BENCHMARK' if perf['recommendations']['meets_benchmark'] else '⚠️  EXCEEDS BENCHMARK'}

📊 DATA ANALYSIS PERFORMANCE
{'─' * 80}
Average Time: {perf['data_analysis']['avg_time_ms']:.2f}ms
Time per MB: {perf['data_analysis']['avg_time_per_mb_ms']:.2f}ms/MB
Benchmark: {self.benchmarks['file_analysis_time_per_mb_ms']}ms/MB
Status: {'✅ MEETS BENCHMARK' if perf['data_analysis']['meets_benchmark'] else '⚠️  EXCEEDS BENCHMARK'}

{'═' * 80}
"""
        return report


def run_accuracy_benchmark(assistant) -> Dict[str, Any]:
    """Run complete accuracy benchmark test."""
    tracker = MetricsTracker()
    
    print("Running accuracy benchmark...")
    print("This may take a moment...\n")
    
    # Calculate accuracy
    accuracy_data = tracker.calculate_intent_accuracy(assistant)
    
    # Print report
    report = tracker.generate_accuracy_report(assistant)
    print(report)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"accuracy_report_{timestamp}.txt"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📄 Report saved to: {report_filename}")
    
    return accuracy_data


if __name__ == "__main__":
    # Test the metrics tracker
    from services.visualization_assistant import VisualizationAssistant
    
    assistant = VisualizationAssistant()
    
    # Run accuracy benchmark
    accuracy_data = run_accuracy_benchmark(assistant)
    
    # Create tracker and test performance
    tracker = MetricsTracker()
    
    # Simulate some tracking
    print("\nTesting performance tracking...")
    test_goals = [
        "Compare sales by region",
        "Show trend over time",
        "Display distribution of ages"
    ]
    
    for goal in test_goals:
        start = time.time()
        result = assistant.analyze_data_goal(goal)
        elapsed_ms = (time.time() - start) * 1000
        
        tracker.track_intent_detection(goal, result['intent'], elapsed_ms)
        tracker.track_recommendations(result['intent'], result['recommendations'], elapsed_ms)
    
    # Print performance report
    print(tracker.generate_performance_report())
    
    # Export metrics
    metrics_file = tracker.export_metrics()
    print(f"\n📊 Metrics exported to: {metrics_file}")
