"""
Utility functions for the Data Visualization Assistant
"""

from typing import Dict, List, Any
import json


def format_recommendation(recommendation: Dict[str, Any], index: int) -> str:
    """
    Format a single recommendation for display.
    
    Args:
        recommendation: Dictionary containing chart recommendation
        index: Index number for the recommendation
        
    Returns:
        Formatted string for display
    """
    output = f"\n### {index}. {recommendation['name']}\n"
    output += f"**Rationale:** {recommendation['rationale']}\n\n"
    output += "**Design Constraints:**\n"
    output += f"- 🎨 **Color:** {recommendation['constraints']['color']}\n"
    output += f"- 📊 **Axis:** {recommendation['constraints']['axis']}\n"
    output += f"- 🏷️ **Label:** {recommendation['constraints']['label']}\n"
    return output


def format_full_response(result: Dict[str, Any]) -> str:
    """
    Format the complete analysis result for display.
    
    Args:
        result: Analysis result dictionary
        
    Returns:
        Formatted string for display
    """
    output = f"## 🎯 Visualization Intent: **{result['intent'].upper()}**\n\n"
    output += "---\n"
    output += "## 📈 Top 3 Chart Recommendations:\n"
    
    for i, rec in enumerate(result['recommendations'], 1):
        output += format_recommendation(rec, i)
        if i < len(result['recommendations']):
            output += "\n---\n"
    
    return output


def export_to_json(result: Dict[str, Any], filename: str = "visualization_recommendations.json") -> str:
    """
    Export recommendations to a JSON file.
    
    Args:
        result: Analysis result dictionary
        filename: Output filename
        
    Returns:
        Status message
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        return f"✅ Recommendations exported to {filename}"
    except Exception as e:
        return f"❌ Error exporting: {str(e)}"


def get_example_goals() -> List[str]:
    """
    Get list of example data goals for demonstration.
    
    Returns:
        List of example goals
    """
    return [
        "Compare monthly sales across regions",
        "Show growth trend of revenue over 5 years",
        "Display distribution of customer ages",
        "Show market share percentages by product category",
        "Analyze relationship between advertising spend and sales",
        "Compare quarterly performance of different departments",
        "Track website traffic changes over the past year",
        "Show how many customers fall into each age group",
        "Display what percentage of revenue comes from each product line",
        "Examine correlation between temperature and ice cream sales"
    ]


def validate_data_goal(data_goal: str) -> tuple[bool, str]:
    """
    Validate user input for data goal.
    
    Args:
        data_goal: User's input
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not data_goal or not data_goal.strip():
        return False, "⚠️ Please enter a data visualization goal."
    
    if len(data_goal.strip()) < 5:
        return False, "⚠️ Please provide a more detailed description of your data goal."
    
    if len(data_goal) > 500:
        return False, "⚠️ Please keep your goal description under 500 characters."
    
    return True, ""


def get_intent_icon(intent: str) -> str:
    """
    Get an emoji icon for the given intent.
    
    Args:
        intent: Visualization intent
        
    Returns:
        Emoji string
    """
    icons = {
        'comparison': '⚖️',
        'trend': '📈',
        'distribution': '📊',
        'proportion': '🥧',
        'relationship': '🔗'
    }
    return icons.get(intent, '📊')


def get_intent_description(intent: str) -> str:
    """
    Get a description of the visualization intent.
    
    Args:
        intent: Visualization intent
        
    Returns:
        Description string
    """
    descriptions = {
        'comparison': 'Comparing values or categories to identify differences and rankings.',
        'trend': 'Showing changes over time to identify patterns, growth, or decline.',
        'distribution': 'Displaying how data is spread across a range or frequency.',
        'proportion': 'Showing parts of a whole or percentage breakdown.',
        'relationship': 'Examining correlations or associations between variables.'
    }
    return descriptions.get(intent, 'General data visualization.')
