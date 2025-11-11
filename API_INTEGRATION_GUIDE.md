# 🔌 Backend API Integration Guide for React Frontend

## 📦 Files to Send to Frontend Developer

### ✅ **MUST SEND - Core Backend Files:**

```
bizviz-streamlit/
├── services/
│   ├── __init__.py
│   ├── visualization_assistant.py    # Chart recommendation engine
│   └── data_analyzer.py             # Data analysis & insights engine
├── utils/
│   ├── __init__.py
│   └── formatting.py                # Helper utilities
├── api.py                           # API wrapper (USE THIS!)
├── requirements.txt                 # Python dependencies
└── .env.example                     # Environment variables template
```

### 📚 **SHOULD SEND - Documentation:**

```
├── API_INTEGRATION_GUIDE.md         # This file - API docs
├── SEND_TO_FRIEND.md                # Project overview
├── QUICK_REFERENCE.md               # Feature reference
└── test_data_*.csv                  # Sample datasets for testing
```

### ❌ **DON'T SEND - Streamlit UI Files:**

```
❌ app.py                    # Streamlit UI (not needed)
❌ app_enhanced.py           # Streamlit UI (not needed)
❌ test_assistant.py         # Backend tests (optional)
❌ test_data_analysis.py     # Backend tests (optional)
```

---

## 🚀 API Endpoints for React Integration

Your frontend developer needs to create API endpoints. Here are the recommended approaches:

### **Option 1: Flask REST API (Recommended)**

Create a new file: `flask_api.py`

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.visualization_assistant import VisualizationAssistant
from services.data_analyzer import DataAnalyzer
import pandas as pd
import io
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize services
viz_assistant = VisualizationAssistant()

# Endpoint 1: Get Chart Recommendations
@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """
    Get chart recommendations from text description.
    
    Request Body:
    {
        "data_goal": "Compare monthly sales across regions"
    }
    
    Response:
    {
        "intent": "comparison",
        "recommendations": [
            {
                "name": "Bar Chart",
                "rationale": "...",
                "constraints": {
                    "color": "...",
                    "axis": "...",
                    "label": "..."
                }
            }
        ]
    }
    """
    try:
        data = request.get_json()
        data_goal = data.get('data_goal', '')
        
        result = viz_assistant.analyze_data_goal(data_goal)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint 2: Analyze Uploaded Data
@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """
    Analyze uploaded CSV/Excel file.
    
    Request: multipart/form-data with file upload
    
    Response:
    {
        "analysis": {
            "shape": [rows, cols],
            "columns": [...],
            "numeric_columns": [...],
            "categorical_columns": [...]
        },
        "insights": [
            {
                "title": "Revenue Performance",
                "insight": "...",
                "recommendation": "..."
            }
        ],
        "charts": [
            {
                "title": "Revenue by Category",
                "description": "...",
                "chart_data": {...},  # Plotly JSON
                "chart_type": "bar"
            }
        ]
    }
    """
    try:
        # Get uploaded file
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        
        # Read file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(file.stream.read().decode("UTF8")))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        else:
            return jsonify({"error": "Unsupported file format"}), 400
        
        # Analyze data
        analyzer = DataAnalyzer(df)
        analysis = analyzer.analyze_data()
        insights = analyzer.generate_sales_insights(analysis)
        
        # Get data goal from request (optional)
        data_goal = request.form.get('data_goal', '')
        charts = analyzer.create_visualizations(data_goal, analysis)
        
        # Convert Plotly figures to JSON
        charts_json = []
        for chart in charts:
            charts_json.append({
                'title': chart['title'],
                'description': chart['description'],
                'chart_data': chart['figure'].to_json(),
                'chart_type': 'plotly'
            })
        
        return jsonify({
            'analysis': {
                'shape': list(analysis['shape']),
                'columns': analysis['columns'],
                'numeric_columns': analysis['numeric_columns'],
                'categorical_columns': analysis['categorical_columns']
            },
            'insights': insights,
            'charts': charts_json
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint 3: Detect Intent Only
@app.route('/api/detect-intent', methods=['POST'])
def detect_intent():
    """
    Detect visualization intent from text.
    
    Request Body:
    {
        "data_goal": "Show sales trend over time"
    }
    
    Response:
    {
        "intent": "trend"
    }
    """
    try:
        data = request.get_json()
        data_goal = data.get('data_goal', '')
        
        intent = viz_assistant.detect_intent(data_goal)
        return jsonify({"intent": intent}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint 4: Export Chart as PNG
@app.route('/api/export-chart', methods=['POST'])
def export_chart():
    """
    Export chart as PNG image.
    
    Request Body:
    {
        "chart_json": {...}  # Plotly JSON
    }
    
    Response: PNG image bytes (base64 encoded)
    """
    try:
        import plotly.graph_objects as go
        
        data = request.get_json()
        chart_json = data.get('chart_json', {})
        
        # Recreate figure from JSON
        fig = go.Figure(chart_json)
        
        # Convert to PNG
        img_bytes = fig.to_image(format="png", width=1200, height=800, scale=2)
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        return jsonify({
            'image': img_base64,
            'format': 'png'
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if API is running."""
    return jsonify({
        "status": "healthy",
        "version": "1.0.0"
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Dependencies to add:**
```bash
pip install flask flask-cors
```

---

### **Option 2: FastAPI (Modern, Async)**

Create a new file: `fastapi_api.py`

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.visualization_assistant import VisualizationAssistant
from services.data_analyzer import DataAnalyzer
import pandas as pd
import io
import base64

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
viz_assistant = VisualizationAssistant()


# Request/Response models
class DataGoalRequest(BaseModel):
    data_goal: str


class RecommendationResponse(BaseModel):
    intent: str
    recommendations: list


# Endpoint 1: Get Chart Recommendations
@app.post("/api/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: DataGoalRequest):
    """Get chart recommendations from text description."""
    try:
        result = viz_assistant.analyze_data_goal(request.data_goal)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint 2: Analyze Uploaded Data
@app.post("/api/analyze")
async def analyze_data(file: UploadFile = File(...), data_goal: str = ""):
    """Analyze uploaded CSV/Excel file."""
    try:
        # Read file
        contents = await file.read()
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Analyze data
        analyzer = DataAnalyzer(df)
        analysis = analyzer.analyze_data()
        insights = analyzer.generate_sales_insights(analysis)
        charts = analyzer.create_visualizations(data_goal, analysis)
        
        # Convert charts to JSON
        charts_json = []
        for chart in charts:
            charts_json.append({
                'title': chart['title'],
                'description': chart['description'],
                'chart_data': chart['figure'].to_json(),
                'chart_type': 'plotly'
            })
        
        return {
            'analysis': {
                'shape': list(analysis['shape']),
                'columns': analysis['columns'],
                'numeric_columns': analysis['numeric_columns'],
                'categorical_columns': analysis['categorical_columns']
            },
            'insights': insights,
            'charts': charts_json
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint 3: Health Check
@app.get("/api/health")
async def health_check():
    """Check if API is running."""
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Dependencies to add:**
```bash
pip install fastapi uvicorn python-multipart
```

---

## 📱 React Integration Examples

### **Example 1: Get Chart Recommendations**

```javascript
// React Component
import React, { useState } from 'react';
import axios from 'axios';

function ChartRecommendations() {
  const [dataGoal, setDataGoal] = useState('');
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);

  const getRecommendations = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/recommendations', {
        data_goal: dataGoal
      });
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Get Chart Recommendations</h2>
      <textarea
        value={dataGoal}
        onChange={(e) => setDataGoal(e.target.value)}
        placeholder="Describe what you want to visualize..."
      />
      <button onClick={getRecommendations} disabled={loading}>
        {loading ? 'Analyzing...' : 'Get Recommendations'}
      </button>

      {recommendations && (
        <div>
          <h3>Intent: {recommendations.intent}</h3>
          {recommendations.recommendations.map((rec, idx) => (
            <div key={idx}>
              <h4>{rec.name}</h4>
              <p>{rec.rationale}</p>
              <ul>
                <li>Color: {rec.constraints.color}</li>
                <li>Axis: {rec.constraints.axis}</li>
                <li>Label: {rec.constraints.label}</li>
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ChartRecommendations;
```

---

### **Example 2: File Upload & Analysis**

```javascript
import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';

function DataAnalysis() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const analyzeData = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('data_goal', ''); // Optional

    try {
      const response = await axios.post(
        'http://localhost:5000/api/analyze',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      setResults(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Upload & Analyze Data</h2>
      <input type="file" accept=".csv,.xlsx,.xls" onChange={handleFileChange} />
      <button onClick={analyzeData} disabled={loading || !file}>
        {loading ? 'Analyzing...' : 'Analyze'}
      </button>

      {results && (
        <div>
          {/* Display Insights */}
          <h3>Business Insights</h3>
          {results.insights.map((insight, idx) => (
            <div key={idx} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px 0' }}>
              <h4>{insight.title}</h4>
              <p><strong>Insight:</strong> {insight.insight}</p>
              <p style={{ backgroundColor: '#e8f5e9', padding: '10px' }}>
                <strong>💡 Recommendation:</strong> {insight.recommendation}
              </p>
            </div>
          ))}

          {/* Display Charts */}
          <h3>Visualizations</h3>
          {results.charts.map((chart, idx) => (
            <div key={idx}>
              <h4>{chart.title}</h4>
              <p>{chart.description}</p>
              <Plot
                data={JSON.parse(chart.chart_data).data}
                layout={JSON.parse(chart.chart_data).layout}
                config={{ responsive: true }}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default DataAnalysis;
```

---

## 📦 Package.json Dependencies for React

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0",
    "react-plotly.js": "^2.6.0",
    "plotly.js": "^2.27.0"
  }
}
```

Install with:
```bash
npm install axios react-plotly.js plotly.js
```

---

## 🔧 Environment Setup

### **Backend (.env file)**

```env
# Flask/FastAPI Configuration
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000

# CORS Settings (Update with your React app URL)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Optional: Database (if needed later)
DATABASE_URL=sqlite:///app.db

# Optional: API Rate Limiting
RATE_LIMIT=100/hour
```

---

## 🚀 Running Both Backend & Frontend

### **Terminal 1 - Backend (Flask)**
```bash
cd bizviz-streamlit
python flask_api.py
# API runs on http://localhost:5000
```

### **Terminal 2 - Frontend (React)**
```bash
cd your-react-app
npm start
# React runs on http://localhost:3000
```

---

## 📋 API Endpoints Summary

| Method | Endpoint | Purpose | Request | Response |
|--------|----------|---------|---------|----------|
| POST | `/api/recommendations` | Get chart recommendations | `{data_goal: string}` | `{intent, recommendations[]}` |
| POST | `/api/analyze` | Analyze uploaded file | `FormData(file)` | `{analysis, insights[], charts[]}` |
| POST | `/api/detect-intent` | Detect intent only | `{data_goal: string}` | `{intent: string}` |
| POST | `/api/export-chart` | Export chart as PNG | `{chart_json}` | `{image: base64}` |
| GET | `/api/health` | Health check | - | `{status, version}` |

---

## 🎨 Frontend Components to Build

### **1. ChartRecommendations Component**
- Text input for data goal
- Display recommendations with constraints
- Show intent badge

### **2. FileUpload Component**
- Drag & drop file upload
- File type validation (.csv, .xlsx)
- Upload progress indicator

### **3. InsightCard Component**
- Display insight title
- Show insight text
- Highlight recommendation (different bg color)
- Icon for insight type

### **4. ChartViewer Component**
- Render Plotly charts
- PNG download button
- Interactive zoom/pan
- Full-screen mode

### **5. Dashboard Layout**
- Mode switcher (Recommendations / Analysis)
- Sidebar navigation
- Responsive grid layout

---

## 🐛 Testing the API

### **Using Postman/Thunder Client:**

**Test 1: Recommendations**
```
POST http://localhost:5000/api/recommendations
Content-Type: application/json

{
  "data_goal": "Compare monthly sales across regions"
}
```

**Test 2: File Analysis**
```
POST http://localhost:5000/api/analyze
Content-Type: multipart/form-data

file: [Upload test_data_office_supplies.csv]
```

### **Using cURL:**

```bash
# Test recommendations
curl -X POST http://localhost:5000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"data_goal": "Show sales trend over time"}'

# Test health check
curl http://localhost:5000/api/health
```

---

## 📄 Files Checklist for Frontend Developer

### ✅ **Must Send:**

```
□ services/visualization_assistant.py
□ services/data_analyzer.py
□ services/__init__.py
□ utils/formatting.py
□ utils/__init__.py
□ flask_api.py (NEW - create this)
□ requirements.txt
□ API_INTEGRATION_GUIDE.md (this file)
□ .env.example
□ test_data_office_supplies.csv
□ test_data_retail_stores.csv
□ test_data_marketing_campaigns.csv
```

### 📚 **Nice to Have:**

```
□ SEND_TO_FRIEND.md (project overview)
□ QUICK_REFERENCE.md (features)
□ UNIQUE_FEATURES.md (what makes it special)
□ test_assistant.py (for reference)
```

### ❌ **Don't Send:**

```
□ app.py (Streamlit UI)
□ app_enhanced.py (Streamlit UI)
□ All markdown docs (except API guide)
```

---

## 🎯 Next Steps for Frontend Dev

1. **Setup Backend API:**
   ```bash
   pip install -r requirements.txt
   pip install flask flask-cors
   python flask_api.py
   ```

2. **Create React App:**
   ```bash
   npx create-react-app bizviz-frontend
   cd bizviz-frontend
   npm install axios react-plotly.js plotly.js
   ```

3. **Build Components:**
   - Mode Switcher
   - Chart Recommendations View
   - File Upload & Analysis View
   - Insight Cards
   - Chart Viewer

4. **Test Integration:**
   - Test file upload
   - Test chart rendering
   - Test recommendations
   - Test PNG export

5. **Deploy:**
   - Backend: Heroku, AWS, or DigitalOcean
   - Frontend: Vercel, Netlify, or AWS S3

---

## 🔐 Security Considerations

```python
# Add to Flask/FastAPI

# 1. File size limit
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 2. Allowed file types
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 3. Rate limiting (install: flask-limiter)
from flask_limiter import Limiter

limiter = Limiter(
    app,
    default_limits=["100 per hour"]
)

# 4. CORS - specify exact origins in production
CORS(app, origins=["https://yourdomain.com"])
```

---

## 📞 Support

**For Frontend Developer:**
- Full API documentation above
- Example React code provided
- Test datasets included
- Sample requests/responses documented

**Questions?**
- Check API endpoint responses
- Test with Postman first
- Review React examples
- Start with recommendations endpoint (simplest)

---

## 🎉 Ready to Integrate!

Send these files:
1. ✅ Core services folder
2. ✅ Flask API file (create using code above)
3. ✅ This integration guide
4. ✅ Test datasets

Your frontend dev has everything needed to build a beautiful React UI! 🚀

---

**Built with ❤️ for seamless integration**
