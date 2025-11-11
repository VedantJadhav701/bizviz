# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Run Tests (Optional but Recommended)
```powershell
python test_assistant.py
```

### Step 3: Start the Application

**Option A: Web Interface (Recommended)**
```powershell
streamlit run app.py
```

**Option B: API/Command Line**
```powershell
python api.py
```

## 📝 Quick Examples

### Example 1: Using the Web Interface
1. Open the app in your browser (usually http://localhost:8501)
2. Type: "Compare monthly sales across regions"
3. Click "Analyze Goal"
4. View recommendations and design constraints

### Example 2: Using Python Code
```python
from services.visualization_assistant import VisualizationAssistant

assistant = VisualizationAssistant()
result = assistant.analyze_data_goal("Show revenue growth over 5 years")

print(f"Intent: {result['intent']}")
for rec in result['recommendations']:
    print(f"\nChart: {rec['name']}")
    print(f"Why: {rec['rationale']}")
```

### Example 3: Using the API
```python
from api import VisualizationAPI

api = VisualizationAPI()

# Get recommendations as dictionary
result = api.get_recommendations("Display customer age distribution")

# Get recommendations as JSON string
json_result = api.get_recommendations(
    "Show market share percentages", 
    format='json'
)

# Detect intent only
intent = api.detect_intent("Compare Q1 vs Q2 performance")
```

## 🎯 Sample Data Goals to Try

Copy and paste these into the app:

1. **Comparison**
   - "Compare monthly sales across regions"
   - "Which product category performs best"
   - "Contrast Q1 revenue versus Q2 revenue"

2. **Trend**
   - "Show growth trend of revenue over 5 years"
   - "Track website traffic changes over the past year"
   - "Display sales evolution month by month"

3. **Distribution**
   - "Display distribution of customer ages"
   - "Show how many orders fall into each price range"
   - "Frequency of purchase amounts"

4. **Proportion**
   - "Show market share percentages by product category"
   - "What percentage of revenue comes from each region"
   - "Display composition of total costs by department"

5. **Relationship**
   - "Analyze relationship between advertising spend and sales"
   - "Examine correlation between temperature and ice cream sales"
   - "Show how price affects demand"

## 🛠️ Troubleshooting

### Issue: Streamlit not found
```powershell
pip install streamlit
```

### Issue: Module import errors
Make sure you're in the project directory:
```powershell
cd c:\Users\HP\projects\bizviz-streamlit
```

### Issue: Python version
This project requires Python 3.8 or higher:
```powershell
python --version
```

## 📚 Next Steps

- **Customize**: Edit `services/visualization_assistant.py` to add your own chart types
- **Extend**: Add new intents or keywords to improve detection
- **Integrate**: Use the API to integrate with your own applications
- **Share**: Export recommendations as JSON to share with your team

## 💡 Tips

- Be specific in your data goals for better recommendations
- Include context like time periods, categories, or metrics
- Try the example buttons in the sidebar for inspiration
- Use the JSON export feature to save recommendations

## 🎓 Learning Resources

- Check the `test_assistant.py` file for usage examples
- Review `api.py` for programmatic usage patterns
- Read the docstrings in `visualization_assistant.py` for technical details

---

**Need Help?** Review the README.md for detailed documentation.
