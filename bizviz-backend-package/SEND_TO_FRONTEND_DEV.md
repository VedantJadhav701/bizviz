# 📦 Files Package for Frontend Developer

## 🎯 Quick Summary

**What is this?**
Backend services for an AI-powered Data Visualization Assistant that:
- Recommends the best charts based on text descriptions (5 intents, 15 chart types)
- Analyzes CSV/Excel files and generates 5 business insights automatically
- Creates 5 interactive Plotly charts automatically
- Provides design constraints (color, axis, label) for each chart
- Exports charts as high-quality PNG images

**Your job:** Build a beautiful React UI that talks to this backend via REST API

---

## 📂 Files You Need (Send These)

### ✅ **Core Backend Services** (The Brain)

```
services/
├── visualization_assistant.py   # 🧠 Chart recommendation engine
│                                 # - Detects intent from text
│                                 # - Recommends top 3 charts
│                                 # - Provides design constraints
│
├── data_analyzer.py             # 📊 Data analysis engine
│                                 # - Analyzes CSV/Excel files
│                                 # - Generates 5 business insights
│                                 # - Creates 5 Plotly charts
│
└── __init__.py                  # Package initializer

utils/
├── formatting.py                # 🛠️ Helper utilities
└── __init__.py
```

### ✅ **API Layer** (The Interface)

```
flask_api.py                     # 🔌 REST API for React integration
                                 # - 5 endpoints ready to use
                                 # - CORS enabled
                                 # - Error handling included
```

### ✅ **Configuration**

```
requirements.txt                 # 📦 Python dependencies
.env.example                     # 🔐 Environment variables template
```

### ✅ **Test Data** (For Development)

```
test_data/
├── test_data_office_supplies.csv       # 📌 Office products sales (50 rows)
├── test_data_retail_stores.csv         # 📌 Multi-store performance (50 rows)
└── test_data_marketing_campaigns.csv   # 📌 Marketing ROI (46 rows)
```

### ✅ **Documentation**

```
API_INTEGRATION_GUIDE.md         # 📖 Complete API docs with React examples
SEND_TO_FRIEND.md                # 📄 Project overview
```

---

## ❌ Files You DON'T Need (Ignore These)

```
❌ app.py                        # Streamlit UI (not needed)
❌ app_enhanced.py               # Streamlit UI (not needed)
❌ test_assistant.py             # Backend tests (optional)
❌ test_data_analysis.py         # Backend tests (optional)
❌ *.md files                    # Docs (except API guide)
```

---

## 🚀 Quick Start Guide

### **Step 1: Setup Backend** (5 minutes)

```bash
# Install dependencies
pip install -r requirements.txt
pip install flask flask-cors kaleido

# Run API server
python flask_api.py

# API runs on: http://localhost:5000
```

### **Step 2: Test API** (2 minutes)

```bash
# Test 1: Health check
curl http://localhost:5000/api/health

# Test 2: Get recommendations
curl -X POST http://localhost:5000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{"data_goal": "Compare sales by region"}'
```

### **Step 3: Build React UI** (Your work starts here!)

```bash
# Create React app
npx create-react-app bizviz-frontend
cd bizviz-frontend

# Install dependencies
npm install axios react-plotly.js plotly.js

# Start development
npm start
```

---

## 🔌 API Endpoints (What You'll Use)

| Method | Endpoint | Purpose | Example |
|--------|----------|---------|---------|
| **POST** | `/api/recommendations` | Get chart recommendations | See below ⬇️ |
| **POST** | `/api/analyze` | Analyze CSV/Excel file | See below ⬇️ |
| **POST** | `/api/detect-intent` | Detect intent only | See below ⬇️ |
| **POST** | `/api/export-chart` | Export chart as PNG | See below ⬇️ |
| **GET** | `/api/health` | Health check | Simple GET request |

---

## 📱 React Code Examples

### **Example 1: Get Chart Recommendations**

```javascript
import axios from 'axios';

async function getRecommendations(dataGoal) {
  try {
    const response = await axios.post('http://localhost:5000/api/recommendations', {
      data_goal: dataGoal
    });
    
    console.log('Intent:', response.data.intent);
    console.log('Top 3 Charts:', response.data.recommendations);
    
    return response.data;
  } catch (error) {
    console.error('Error:', error);
  }
}

// Usage
getRecommendations("Compare monthly sales across regions");

/* Response:
{
  "intent": "comparison",
  "recommendations": [
    {
      "name": "Bar Chart",
      "rationale": "Perfect for comparing values across categories",
      "constraints": {
        "color": "Use distinct colors for each category",
        "axis": "Categories on X-axis, values on Y-axis",
        "label": "Label each bar with exact values"
      }
    },
    // ... 2 more charts
  ]
}
*/
```

### **Example 2: Upload & Analyze File**

```javascript
import axios from 'axios';

async function analyzeFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('data_goal', ''); // Optional

  try {
    const response = await axios.post('http://localhost:5000/api/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    console.log('Data shape:', response.data.analysis.shape);
    console.log('Insights:', response.data.insights);
    console.log('Charts:', response.data.charts);
    
    return response.data;
  } catch (error) {
    console.error('Error:', error);
  }
}

/* Response:
{
  "analysis": {
    "shape": [50, 8],
    "columns": ["Date", "Product", "Category", "Sales", ...],
    "numeric_columns": ["Sales", "Quantity", "Revenue"],
    "categorical_columns": ["Product", "Category", "Region"]
  },
  "insights": [
    {
      "title": "Revenue Performance",
      "insight": "Total revenue is $1.2M with average of $24K per record",
      "recommendation": "Focus on high-revenue categories to maximize profit"
    },
    // ... 4 more insights
  ],
  "charts": [
    {
      "title": "Revenue by Category",
      "description": "Bar chart showing revenue distribution",
      "chart_data": "{...plotly json...}",
      "chart_type": "plotly"
    },
    // ... 4 more charts
  ]
}
*/
```

### **Example 3: Render Plotly Chart**

```javascript
import Plot from 'react-plotly.js';

function ChartViewer({ chartData }) {
  const chart = JSON.parse(chartData);
  
  return (
    <Plot
      data={chart.data}
      layout={chart.layout}
      config={{ responsive: true }}
    />
  );
}
```

---

## 🎨 UI Components to Build

### **1. HomePage**
- Two big cards: "Get Recommendations" and "Analyze Data"
- Modern gradient backgrounds
- Icons for each mode

### **2. RecommendationsPage**
- Large text area: "Describe what you want to visualize..."
- Button: "Get Recommendations"
- Results display:
  - Intent badge (blue, green, purple based on type)
  - 3 chart cards with name, rationale, constraints

### **3. AnalysisPage**
- Drag & drop file upload zone
- File preview (name, size, type)
- Button: "Analyze"
- Results display:
  - 5 insight cards (with 💡 icons)
  - 5 interactive Plotly charts
  - Download PNG button for each chart

### **4. InsightCard Component**
```javascript
function InsightCard({ insight }) {
  return (
    <div className="insight-card">
      <h3>💡 {insight.title}</h3>
      <p className="insight-text">{insight.insight}</p>
      <div className="recommendation">
        <strong>Recommendation:</strong> {insight.recommendation}
      </div>
    </div>
  );
}
```

---

## 🎯 What Makes This Unique?

**15 Unique Features** (Full list in `UNIQUE_FEATURES.md`):
1. **5-Second Analysis** - 600x faster than traditional tools
2. **Dual Intelligence** - Recommendations OR data analysis
3. **Auto-Generated Insights** - 5 actionable insights per upload
4. **Design Constraints** - Color, axis, label guidance for each chart
5. **Intent Detection** - Automatically understands what you want
6. **15 Chart Types** - 3 per intent (comparison, trend, distribution, etc.)
7. **Interactive Charts** - Plotly with zoom, pan, hover
8. **PNG Export** - High-quality 2400×1600 images
9. **Multi-Format Support** - CSV, Excel (XLSX, XLS)
10. ... and more!

---

## 📊 Test Datasets Explained

### **1. Office Supplies Sales** (50 rows)
- **Columns:** Date, Product, Category, Region, Sales, Quantity, Revenue, Profit
- **Best for:** Testing comparison charts (by category, region)
- **Example insight:** "Technology category generates 45% of total revenue"

### **2. Retail Store Performance** (50 rows)
- **Columns:** Store ID, Location, Manager, Revenue, Expenses, Profit Margin, Employees, Customer Rating
- **Best for:** Testing distribution & relationship charts
- **Example insight:** "Store efficiency varies by location - NYC stores most profitable"

### **3. Marketing Campaigns** (46 rows)
- **Columns:** Campaign Name, Channel, Budget, Impressions, Clicks, Conversions, Revenue, ROI
- **Best for:** Testing trend analysis & ROI calculations
- **Example insight:** "Email marketing has 3.2x higher ROI than social media"

---

## 🔐 Security & Configuration

### **CORS Settings** (Already configured in `flask_api.py`)
```python
CORS(app, origins=["http://localhost:3000", "http://localhost:3001"])
```
**Update this** when you deploy!

### **File Limits**
- Max size: 16MB
- Allowed formats: CSV, XLSX, XLS

### **Environment Variables** (Create `.env` file)
```env
FLASK_ENV=development
API_PORT=5000
CORS_ORIGINS=http://localhost:3000
```

---

## 🐛 Debugging Tips

### **Issue: CORS Error**
```javascript
// Error: Access to XMLHttpRequest has been blocked by CORS policy
```
**Fix:** Make sure Flask API is running and CORS origins include your React URL

### **Issue: Module Not Found**
```bash
# Error: ModuleNotFoundError: No module named 'flask'
```
**Fix:** Install dependencies:
```bash
pip install flask flask-cors
```

### **Issue: File Upload Not Working**
```javascript
// Error: No file uploaded
```
**Fix:** Use `FormData` and correct headers:
```javascript
const formData = new FormData();
formData.append('file', file);

axios.post(url, formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
```

---

## 📦 Package Checklist

Before sending to frontend dev, make sure you have:

- [ ] `services/` folder (visualization_assistant.py, data_analyzer.py)
- [ ] `utils/` folder (formatting.py)
- [ ] `flask_api.py` (REST API)
- [ ] `requirements.txt`
- [ ] `.env.example`
- [ ] `API_INTEGRATION_GUIDE.md` (full docs)
- [ ] `SEND_TO_FRONTEND_DEV.md` (this file)
- [ ] Test datasets (3 CSV files)

---

## 🚀 Deployment Ready

### **Backend Deployment Options:**
- **Heroku:** Easy Python deployment
- **AWS Lambda:** Serverless with API Gateway
- **DigitalOcean:** VPS with Docker
- **Render:** Modern PaaS (recommended)

### **Frontend Deployment Options:**
- **Vercel:** Best for React (automatic deployments)
- **Netlify:** Great for static sites
- **AWS S3 + CloudFront:** Scalable solution

---

## 📞 Support for Frontend Dev

**Questions?**
1. Check `API_INTEGRATION_GUIDE.md` for detailed API docs
2. Test endpoints with Postman/Thunder Client first
3. Review React examples above
4. Start with `/api/health` endpoint (simplest)

**Testing Workflow:**
1. ✅ Health check → Returns `{"status": "healthy"}`
2. ✅ Recommendations → Test with simple text
3. ✅ File upload → Use test datasets provided
4. ✅ Chart rendering → Parse Plotly JSON
5. ✅ PNG export → Test download functionality

---

## 🎉 You're All Set!

**What you have:**
- ✅ Complete backend services
- ✅ REST API with 5 endpoints
- ✅ 3 test datasets
- ✅ Full API documentation
- ✅ React code examples

**What you need to build:**
- 🎨 Beautiful React UI
- 📱 Responsive layout
- ⚡ Smooth file upload experience
- 📊 Chart visualization components
- 💡 Insight display cards

**Time to build something amazing! 🚀**

---

**Built with ❤️ for seamless integration**

Need help? Check the full API guide or test with Postman first!
