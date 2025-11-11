# 📊 Data Visualization Assistant

A smart assistant that analyzes your data goals and recommends the best chart types with practical design constraints for small business users.

## 🎯 Features

- **Intent Detection**: Automatically identifies what you want to communicate (comparison, trend, distribution, proportion, relationship)
- **Top 3 Recommendations**: Provides three best-suited chart types with clear rationale
- **Design Constraints**: Offers specific guidance on color palettes, axis scales, and labeling
- **User-Friendly Interface**: Built with Streamlit for easy interaction
- **JSON Output**: Export recommendations in JSON format for integration with other tools
- **API Access**: Programmatic access for developers

## 🚀 Quick Start

### Installation

1. Clone or navigate to the project directory:
```powershell
cd c:\Users\HP\projects\bizviz-streamlit
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

### Running the Application

#### Streamlit Web Interface

```powershell
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

#### API / Command Line

```powershell
python api.py
```

This will run examples and show JSON output for various data goals.

## 📖 Usage

### Web Interface

1. **Enter Your Data Goal**: Describe what you want to show with your data
   - Example: "Compare monthly sales across regions"
   - Example: "Show growth trend of revenue over 5 years"

2. **Click Analyze Goal**: The assistant will detect your intent and provide recommendations

3. **Review Recommendations**: You'll get:
   - Detected visualization intent
   - Top 3 chart types with rationale
   - Design constraints for each chart (color, axis, labeling)

4. **Export (Optional)**: Download recommendations as JSON

### Programmatic Usage

```python
from api import VisualizationAPI

# Initialize API
api = VisualizationAPI()

# Get recommendations
result = api.get_recommendations("Compare monthly sales across regions")

# Get JSON format
json_result = api.get_recommendations("Show revenue trend", format='json')

# Detect intent only
intent = api.detect_intent("Display customer age distribution")
print(f"Detected intent: {intent}")
```

### Direct Service Usage

```python
from services.visualization_assistant import VisualizationAssistant

assistant = VisualizationAssistant()

# Analyze data goal
result = assistant.analyze_data_goal("Compare quarterly performance")

# Access results
print(f"Intent: {result['intent']}")
for rec in result['recommendations']:
    print(f"Chart: {rec['name']}")
    print(f"Rationale: {rec['rationale']}")
    print(f"Constraints: {rec['constraints']}")
```

## 🎨 Visualization Intents

The assistant detects five main visualization intents:

1. **Comparison** (⚖️): Comparing values across categories
   - Recommended: Bar Chart, Grouped Bar Chart, Column Chart

2. **Trend** (📈): Showing changes over time
   - Recommended: Line Chart, Area Chart, Combo Chart

3. **Distribution** (📊): Displaying data spread or frequency
   - Recommended: Histogram, Box Plot, Frequency Bar Chart

4. **Proportion** (🥧): Showing parts of a whole
   - Recommended: Pie Chart, Donut Chart, Stacked Bar Chart

5. **Relationship** (🔗): Examining correlations between variables
   - Recommended: Scatter Plot, Bubble Chart, Heatmap

## 📁 Project Structure

```
bizviz-streamlit/
├── app.py                          # Main Streamlit application
├── api.py                          # API wrapper and examples
├── requirements.txt                # Python dependencies
├── services/
│   ├── __init__.py
│   └── visualization_assistant.py  # Core recommendation engine
├── utils/
│   ├── __init__.py
│   └── formatting.py              # Formatting utilities
└── README.md                      # This file
```

## 🔧 Configuration

No additional configuration needed! The assistant works out of the box with sensible defaults.

## 📊 Example Data Goals

Try these examples to see the assistant in action:

- "Compare monthly sales across regions"
- "Show growth trend of revenue over 5 years"
- "Display distribution of customer ages"
- "Show market share percentages by product category"
- "Analyze relationship between advertising spend and sales"
- "Compare quarterly performance of different departments"
- "Track website traffic changes over the past year"

## 🛠️ Development

### Adding New Chart Types

Edit `services/visualization_assistant.py` and add to the `CHART_RECOMMENDATIONS` dictionary:

```python
'your_intent': [
    {
        'name': 'Chart Name',
        'rationale': 'Why this chart works...',
        'constraints': {
            'color': 'Color guidance...',
            'axis': 'Axis guidance...',
            'label': 'Label guidance...'
        }
    }
]
```

### Adding New Intent Keywords

Edit the `INTENT_KEYWORDS` dictionary in `visualization_assistant.py`:

```python
'your_intent': ['keyword1', 'keyword2', 'keyword3']
```

## 📝 JSON Response Format

```json
{
  "intent": "comparison",
  "recommendations": [
    {
      "name": "Bar Chart",
      "rationale": "Best for comparing values...",
      "constraints": {
        "color": "Use distinct colors...",
        "axis": "Start Y-axis at zero...",
        "label": "Label each bar clearly..."
      }
    }
  ]
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Add new chart types
- Improve intent detection
- Enhance design constraints
- Fix bugs or typos

## 📄 License

This project is open source and available for educational and commercial use.

## 🙏 Acknowledgments

Built for small business users who need practical, easy-to-understand visualization guidance without technical jargon.

## 📞 Support

For issues or questions:
1. Check the examples in the sidebar of the web interface
2. Review this README
3. Run `python api.py` to see example outputs

---

**Built with ❤️ for better data communication** 📊
