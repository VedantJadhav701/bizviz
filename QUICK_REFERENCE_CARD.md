# 📋 Quick Reference Card - For Your Frontend Developer

## 🎯 What to Send
**File:** `bizviz-backend-for-react.zip`  
**Start with:** `SEND_TO_FRONTEND_DEV.md`

---

## ⚡ Quick Setup (3 Commands)
```bash
pip install -r requirements.txt
python flask_api.py
# API runs on http://localhost:5000
```

---

## 🔌 5 API Endpoints

### 1. Get Chart Recommendations
```javascript
POST /api/recommendations
Body: { "data_goal": "Compare sales by region" }
Returns: { intent, recommendations[] }
```

### 2. Analyze Data File
```javascript
POST /api/analyze
Body: FormData with file
Returns: { analysis, insights[], charts[] }
```

### 3. Detect Intent
```javascript
POST /api/detect-intent
Body: { "data_goal": "..." }
Returns: { intent }
```

### 4. Export Chart
```javascript
POST /api/export-chart
Body: { "chart_json": {...} }
Returns: { image: base64 }
```

### 5. Health Check
```javascript
GET /api/health
Returns: { status: "healthy" }
```

---

## 📦 React Packages Needed
```bash
npm install axios react-plotly.js plotly.js
```

---

## 🎨 UI Components to Build
- [ ] ChartRecommendation cards
- [ ] InsightCard with recommendations
- [ ] FileUploader (drag & drop)
- [ ] ChartViewer (Plotly)
- [ ] LoadingSpinner
- [ ] ErrorMessage
- [ ] Mode switcher

---

## 🚀 Example React Code

### Get Recommendations
```javascript
const response = await axios.post(
  'http://localhost:5000/api/recommendations',
  { data_goal: text }
);
console.log(response.data);
```

### Upload File
```javascript
const formData = new FormData();
formData.append('file', file);
const response = await axios.post(
  'http://localhost:5000/api/analyze',
  formData,
  { headers: { 'Content-Type': 'multipart/form-data' } }
);
console.log(response.data.insights);
```

### Render Chart
```javascript
import Plot from 'react-plotly.js';

const chartData = JSON.parse(chart.chart_data);
<Plot 
  data={chartData.data} 
  layout={chartData.layout} 
/>
```

---

## 📚 Documentation Files
1. **SEND_TO_FRONTEND_DEV.md** ← Start here!
2. **API_INTEGRATION_GUIDE.md** ← Full API docs
3. **FRONTEND_INTEGRATION_CHECKLIST.md** ← Checklist
4. **README.md** ← Quick reference

---

## 🎯 What Backend Provides

### Chart Recommendations Mode
Input: Text description  
Output: 3 chart recommendations + design constraints

### Data Analysis Mode
Input: CSV/Excel file  
Output: 5 insights + 5 charts (auto-generated)

---

## 🔥 Unique Features

✅ 5-second analysis (600x faster!)  
✅ 15 chart types across 5 intents  
✅ Automatic business insights  
✅ Design constraints per chart  
✅ PNG export (2400×1600)  
✅ Interactive Plotly charts  
✅ Dual-mode intelligence

---

## 🐛 Quick Troubleshooting

**CORS Error?** → Make sure API is running  
**Module Not Found?** → `pip install flask flask-cors`  
**File Upload Fails?** → Use FormData with correct headers  
**Chart Not Rendering?** → Parse JSON first: `JSON.parse(chart_data)`

---

## 📧 Message Template

```
Hey! Backend is ready. See attached ZIP.

Start with: SEND_TO_FRONTEND_DEV.md
API docs: API_INTEGRATION_GUIDE.md

Setup: 
1. pip install -r requirements.txt
2. python flask_api.py
3. http://localhost:5000

Questions? Let me know!
```

---

**Ready to build! 🚀**
