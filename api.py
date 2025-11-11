"""
API Module for Data Visualization Assistant
Provides a simple interface for programmatic access to recommendations.
"""

from services.visualization_assistant import VisualizationAssistant
import json


class VisualizationAPI:
    """Simple API wrapper for the visualization assistant."""
    
    def __init__(self):
        """Initialize the API."""
        self.assistant = VisualizationAssistant()
    
    def get_recommendations(self, data_goal: str, format: str = 'dict') -> any:
        """
        Get visualization recommendations for a data goal.
        
        Args:
            data_goal: Plain-language description of visualization goal
            format: Output format ('dict' or 'json')
            
        Returns:
            Recommendations in the specified format
        """
        result = self.assistant.analyze_data_goal(data_goal)
        
        if format == 'json':
            return json.dumps(result, indent=2)
        
        return result
    
    def detect_intent(self, data_goal: str) -> str:
        """
        Detect only the visualization intent.
        
        Args:
            data_goal: Plain-language description
            
        Returns:
            Intent string
        """
        return self.assistant.detect_intent(data_goal)


# Example usage
if __name__ == "__main__":
    api = VisualizationAPI()
    
    # Example 1: Compare monthly sales
    print("=" * 80)
    print("Example 1: Compare monthly sales across regions")
    print("=" * 80)
    result1 = api.get_recommendations("Compare monthly sales across regions", format='json')
    print(result1)
    print("\n")
    
    # Example 2: Show growth trend
    print("=" * 80)
    print("Example 2: Show growth trend of revenue over 5 years")
    print("=" * 80)
    result2 = api.get_recommendations("Show growth trend of revenue over 5 years", format='json')
    print(result2)
    print("\n")
    
    # Example 3: Display distribution
    print("=" * 80)
    print("Example 3: Display distribution of customer ages")
    print("=" * 80)
    result3 = api.get_recommendations("Display distribution of customer ages", format='json')
    print(result3)
    print("\n")
    
    # Example 4: Intent detection only
    print("=" * 80)
    print("Example 4: Intent Detection Only")
    print("=" * 80)
    test_goals = [
        "Compare sales across regions",
        "Show revenue trend over time",
        "Display customer age distribution",
        "Show market share percentages",
        "Analyze relationship between price and demand"
    ]
    
    for goal in test_goals:
        intent = api.detect_intent(goal)
        print(f"Goal: {goal}")
        print(f"Intent: {intent}\n")
