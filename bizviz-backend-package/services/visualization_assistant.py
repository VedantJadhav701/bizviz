"""
Data Visualization Assistant Service
Analyzes user goals and recommends appropriate chart types with design constraints.
"""

import json
from typing import Dict, List, Any


class VisualizationAssistant:
    """Service for analyzing data goals and recommending visualizations."""
    
    # Intent keywords mapping
    INTENT_KEYWORDS = {
        'comparison': ['compare', 'versus', 'vs', 'difference', 'contrast', 'which is better', 'ranking', 'which'],
        'trend': ['trend', 'over time', 'growth', 'decline', 'change', 'progress', 'evolution', 'historical', 'time series', 'year', 'month', 'week', 'day', 'track'],
        'distribution': ['distribution', 'spread', 'frequency', 'histogram', 'range', 'how many', 'count', 'breakdown'],
        'proportion': ['proportion', 'percentage', 'share', 'composition', 'part of', 'make up', 'portion', 'split'],
        'relationship': ['relationship', 'correlation', 'association', 'depends on', 'impact', 'affect', 'against', 'analyze', 'examine', 'between']
    }
    
    # Chart recommendations by intent
    CHART_RECOMMENDATIONS = {
        'comparison': [
            {
                'name': 'Bar Chart',
                'rationale': 'Best for comparing values across different categories. Easy to read and understand at a glance.',
                'constraints': {
                    'color': 'Use distinct colors for each category or a single color with varying shades for simplicity.',
                    'axis': 'Start Y-axis at zero to avoid misleading comparisons. Use consistent intervals.',
                    'label': 'Label each bar clearly with category names. Consider showing values on bars for precision.'
                }
            },
            {
                'name': 'Grouped Bar Chart',
                'rationale': 'Ideal when comparing multiple metrics across categories (e.g., sales by region and quarter).',
                'constraints': {
                    'color': 'Use a consistent color scheme for each metric across all groups (e.g., blue for Q1, red for Q2).',
                    'axis': 'Ensure adequate spacing between groups to avoid clutter. Start at zero.',
                    'label': 'Include a clear legend and label groups. Keep category names short.'
                }
            },
            {
                'name': 'Column Chart',
                'rationale': 'Similar to bar charts but vertical orientation works well for time-based comparisons.',
                'constraints': {
                    'color': 'Use gradient or categorical colors to distinguish periods or categories.',
                    'axis': 'Label time periods clearly on X-axis. Keep Y-axis scale consistent.',
                    'label': 'Rotate labels if needed to prevent overlap. Highlight key data points.'
                }
            }
        ],
        'trend': [
            {
                'name': 'Line Chart',
                'rationale': 'Perfect for showing changes over time. Makes trends and patterns immediately visible.',
                'constraints': {
                    'color': 'Use contrasting colors for multiple lines. Consider using a bold primary color for main trend.',
                    'axis': 'Use appropriate time intervals on X-axis. Y-axis should accommodate all values comfortably.',
                    'label': 'Label axes clearly with units. Add markers for significant events or milestones.'
                }
            },
            {
                'name': 'Area Chart',
                'rationale': 'Shows cumulative totals over time and emphasizes the magnitude of change.',
                'constraints': {
                    'color': 'Use semi-transparent fills to see overlapping areas. Darker borders for clarity.',
                    'axis': 'Ensure X-axis covers the full time range. Y-axis should start at zero for accurate area representation.',
                    'label': 'Label time periods clearly. Add data labels at key points (peaks, valleys).'
                }
            },
            {
                'name': 'Combo Chart (Line + Bar)',
                'rationale': 'Useful for showing trends alongside specific period values or comparing trend with targets.',
                'constraints': {
                    'color': 'Use distinct colors for line vs bars (e.g., blue bars, red line). Ensure good contrast.',
                    'axis': 'May need dual Y-axes if scales differ significantly. Keep time axis consistent.',
                    'label': 'Include legend to distinguish chart types. Label both axes with appropriate units.'
                }
            }
        ],
        'distribution': [
            {
                'name': 'Histogram',
                'rationale': 'Shows frequency distribution of a continuous variable. Great for understanding data spread.',
                'constraints': {
                    'color': 'Use a single color or gradient. Highlight outliers or specific ranges with accent colors.',
                    'axis': 'Choose appropriate bin sizes (5-20 bins typically). Y-axis shows frequency or count.',
                    'label': 'Label bins clearly with range values. Include total count and mean/median markers.'
                }
            },
            {
                'name': 'Box Plot',
                'rationale': 'Displays distribution summary (median, quartiles, outliers) in a compact format.',
                'constraints': {
                    'color': 'Use light fill with darker borders. Highlight outliers with a contrasting color.',
                    'axis': 'Y-axis should show the full range of data. Label quartile lines for clarity.',
                    'label': 'Label median, Q1, Q3 values. Explain what the box represents in a subtitle.'
                }
            },
            {
                'name': 'Bar Chart (Frequency)',
                'rationale': 'Simple way to show counts or frequencies across discrete categories or ranges.',
                'constraints': {
                    'color': 'Use a single color or color-code by frequency levels (low, medium, high).',
                    'axis': 'Sort bars by frequency (descending) for easier reading. Start Y-axis at zero.',
                    'label': 'Show count values on or above bars. Label all categories on X-axis.'
                }
            }
        ],
        'proportion': [
            {
                'name': 'Pie Chart',
                'rationale': 'Best for showing parts of a whole when you have 3-6 categories. Easy to grasp at a glance.',
                'constraints': {
                    'color': 'Use distinct, easily distinguishable colors. Avoid too many similar shades.',
                    'axis': 'No axes needed. Ensure slices are properly sized by percentage.',
                    'label': 'Show percentage labels on slices. Include category names and consider a legend for clarity.'
                }
            },
            {
                'name': 'Donut Chart',
                'rationale': 'Similar to pie chart but with center space for displaying totals or key metrics.',
                'constraints': {
                    'color': 'Use a cohesive color palette. Order slices from largest to smallest clockwise.',
                    'axis': 'No axes. Use center space wisely for summary information.',
                    'label': 'Label percentages and values. Add a descriptive title in the center if space allows.'
                }
            },
            {
                'name': 'Stacked Bar Chart',
                'rationale': 'Shows composition while allowing comparison across categories. Works well with multiple groups.',
                'constraints': {
                    'color': 'Use consistent colors for each component across all bars. Include a clear legend.',
                    'axis': 'Y-axis typically shows 0-100% or absolute totals. Keep bars of equal width.',
                    'label': 'Label each segment if space allows. Show total at the end of each bar.'
                }
            }
        ],
        'relationship': [
            {
                'name': 'Scatter Plot',
                'rationale': 'Best for showing correlation between two variables. Reveals patterns and outliers.',
                'constraints': {
                    'color': 'Use a single color or color-code by category. Consider size for a third dimension.',
                    'axis': 'Both axes should cover full data range with appropriate scales. Label with variable names and units.',
                    'label': 'Add trendline if correlation is strong. Label outliers or interesting data points.'
                }
            },
            {
                'name': 'Bubble Chart',
                'rationale': 'Shows relationships between three variables using position and bubble size.',
                'constraints': {
                    'color': 'Use color for a fourth dimension (category). Keep bubbles semi-transparent to see overlaps.',
                    'axis': 'Scale both axes appropriately. Use logarithmic scale if data spans orders of magnitude.',
                    'label': 'Include legend for bubble sizes. Label key bubbles directly to highlight important points.'
                }
            },
            {
                'name': 'Heatmap',
                'rationale': 'Shows relationships across multiple variables or correlation matrix. Great for pattern detection.',
                'constraints': {
                    'color': 'Use sequential or diverging color scale (e.g., blue-white-red). Ensure sufficient contrast.',
                    'axis': 'Label all rows and columns clearly. Keep text readable.',
                    'label': 'Include color scale legend showing value ranges. Consider showing values in cells if not too cluttered.'
                }
            }
        ]
    }
    
    def __init__(self):
        """Initialize the Visualization Assistant."""
        pass
    
    def detect_intent(self, data_goal: str) -> str:
        """
        Detect the visualization intent from the user's data goal.
        
        Args:
            data_goal: Plain-language description of what user wants to visualize
            
        Returns:
            Intent string: comparison, trend, distribution, proportion, or relationship
        """
        data_goal_lower = data_goal.lower()
        
        # Count keyword matches for each intent
        intent_scores = {}
        for intent, keywords in self.INTENT_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in data_goal_lower)
            intent_scores[intent] = score
        
        # Get intent with highest score
        max_score = max(intent_scores.values())
        
        # If no clear intent detected, analyze common patterns
        if max_score == 0:
            # Default fallback logic
            if any(word in data_goal_lower for word in ['show', 'display', 'view']):
                return 'comparison'  # Most common fallback
            return 'comparison'
        
        # Return highest scoring intent
        detected_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
        return detected_intent
    
    def get_recommendations(self, intent: str) -> List[Dict[str, Any]]:
        """
        Get chart recommendations for the given intent.
        
        Args:
            intent: Visualization intent
            
        Returns:
            List of chart recommendations with constraints
        """
        return self.CHART_RECOMMENDATIONS.get(intent, self.CHART_RECOMMENDATIONS['comparison'])
    
    def analyze_data_goal(self, data_goal: str) -> Dict[str, Any]:
        """
        Analyze user's data goal and provide visualization recommendations.
        
        Args:
            data_goal: Plain-language description of visualization goal
            
        Returns:
            Dictionary with intent and recommendations
        """
        if not data_goal or not data_goal.strip():
            # Return fallback recommendations
            return {
                'intent': 'comparison',
                'recommendations': [
                    {
                        'name': 'Bar Chart',
                        'rationale': 'Versatile and easy to understand for most comparisons.',
                        'constraints': {
                            'color': 'Use a simple color scheme with good contrast.',
                            'axis': 'Start Y-axis at zero. Use clear intervals.',
                            'label': 'Label all categories clearly on the X-axis.'
                        }
                    },
                    {
                        'name': 'Line Chart',
                        'rationale': 'Excellent for showing trends and changes over time.',
                        'constraints': {
                            'color': 'Use distinct line colors if showing multiple series.',
                            'axis': 'Label time periods on X-axis, values on Y-axis.',
                            'label': 'Add markers at key data points for emphasis.'
                        }
                    },
                    {
                        'name': 'Scatter Plot',
                        'rationale': 'Useful for exploring relationships between variables.',
                        'constraints': {
                            'color': 'Use color to represent categories or a third variable.',
                            'axis': 'Ensure both axes cover the full data range.',
                            'label': 'Label axes with variable names and units.'
                        }
                    }
                ]
            }
        
        # Detect intent
        intent = self.detect_intent(data_goal)
        
        # Get recommendations
        recommendations = self.get_recommendations(intent)
        
        return {
            'intent': intent,
            'recommendations': recommendations
        }
    
    def get_json_response(self, data_goal: str) -> str:
        """
        Get recommendations as formatted JSON string.
        
        Args:
            data_goal: User's data visualization goal
            
        Returns:
            JSON formatted string
        """
        result = self.analyze_data_goal(data_goal)
        return json.dumps(result, indent=2)
