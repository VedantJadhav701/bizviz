# 📊 Quick Reference Guide

## 🚀 Start the App

```powershell
streamlit run app_enhanced.py
```

**Access at:** http://localhost:8502

---

## 🎯 Two Modes

### Mode 1: Get Recommendations
**Use when:** You need chart suggestions
1. Select "💡 Get Recommendations"
2. Type your goal (e.g., "Compare monthly sales")
3. Get top 3 chart recommendations + design tips

### Mode 2: Analyze My Data
**Use when:** You have a data file
1. Select "📈 Analyze My Data"
2. Upload CSV/Excel file
3. Get automatic insights + visualizations

---

## 📁 What You Get from File Upload

### Instant Analysis:
- ✅ 5 Business Insights with recommendations
- ✅ 5 Interactive Visualizations (Plotly)
- ✅ Data Summary Statistics
- ✅ Export Options (CSV, TXT, JSON)

### Sample Output (Flipkart Dataset):
```
💰 Revenue: $13.3M total | $99.92 avg per transaction
📊 Top Categories: Shipped Abroad, Standard, Express
🔄 Returns: 27% (needs attention!)
🗺️ Top Market: Greater Accra ($3.4M)
👥 Customers: 112K unique | 1.2 orders/customer
```

---

## 📊 Charts Generated Automatically

1. **Revenue by Category** - Top 10 horizontal bars
2. **Revenue Trend** - Line chart over time
3. **Status Distribution** - Donut chart
4. **Geographic Performance** - Location bars
5. **Price Analysis** - Scatter plot

---

## 💡 5 Types of Business Insights

| Icon | Insight Type | What It Shows | Recommendation For |
|------|-------------|---------------|-------------------|
| 💰 | Revenue Performance | Total & average revenue | Upselling strategies |
| 📊 | Product Performance | Top/bottom categories | Inventory optimization |
| 🔄 | Return Analysis | Return rate & impact | Quality improvements |
| 🗺️ | Geographic Insights | Regional performance | Expansion planning |
| 👥 | Customer Behavior | Engagement metrics | Loyalty programs |

---

## 🎨 Chart Recommendations (Mode 1)

### 5 Intent Types Detected:
- ⚖️ **Comparison** → Bar, Grouped Bar, Column
- 📈 **Trend** → Line, Area, Combo
- 📊 **Distribution** → Histogram, Box Plot, Bar
- 🥧 **Proportion** → Pie, Donut, Stacked Bar
- 🔗 **Relationship** → Scatter, Bubble, Heatmap

---

## 📁 Supported File Formats

| Format | Extensions | Notes |
|--------|-----------|-------|
| CSV | `.csv` | UTF-8, comma-separated |
| Excel | `.xlsx`, `.xls` | First sheet used |

---

## 🎯 Column Auto-Detection

The app automatically finds:
- 💰 Revenue: `price`, `revenue`, `sale`, `amount`
- 📦 Quantity: `quantity`, `qty`, `units`
- ✅ Status: `status`, `state`
- 🏷️ Category: `category`, `product`, `type`
- 📍 Location: `location`, `zone`, `region`, `city`
- 👤 Customer: `customer`, `client`, `id`
- 📅 Dates: Auto-parsed from column names

---

## ⚡ Quick Commands

```powershell
# Install packages
uv pip install streamlit pandas plotly matplotlib openpyxl

# Run enhanced app
streamlit run app_enhanced.py

# Run original app
streamlit run app.py

# Run tests
python test_assistant.py
python test_data_analysis.py

# Test with Flipkart data
python test_data_analysis.py
```

---

## 📥 Export Options

### Recommendation Mode:
- 📄 JSON recommendations
- 💾 Download button

### Data Analysis Mode:
- 📊 Insights report (TXT)
- 📈 Data summary (CSV)
- 🖼️ Charts (Plotly interactive)

---

## 💡 Pro Tips

### ✅ DO:
- Use clean, structured data
- Include column headers
- Name columns clearly
- Format dates consistently
- Remove special characters

### ❌ DON'T:
- Upload corrupted files
- Use symbols in headers
- Mix date formats
- Leave many empty cells
- Use merged cells (Excel)

---

## 🔧 File Structure

```
bizviz-streamlit/
├── app_enhanced.py          ⭐ NEW! Upload & analyze
├── app.py                   📊 Original recommendations
├── api.py                   🔌 Python API
├── services/
│   ├── visualization_assistant.py   💡 Chart recommendations
│   └── data_analyzer.py            ⭐ NEW! Analysis engine
├── utils/
│   └── formatting.py               🎨 Display helpers
├── test_assistant.py              ✅ Tests (ALL PASSING)
├── test_data_analysis.py          ⭐ NEW! Data tests
└── Flipkart Sales Dataset.csv     📁 Sample data
```

---

## 🎯 Common Use Cases

### 1. E-commerce Analysis
Upload: Sales data
Get: Revenue trends, top products, return analysis
Action: Optimize inventory, reduce returns

### 2. Regional Performance
Upload: Sales by location
Get: Geographic insights, top markets
Action: Focus on high-performing regions

### 3. Customer Insights
Upload: Customer transaction data
Get: Engagement metrics, purchase frequency
Action: Implement loyalty programs

### 4. Product Strategy
Upload: Product performance data
Get: Category analysis, pricing insights
Action: Adjust product mix

---

## 📊 Example Data Goals (Mode 1)

Copy-paste these to try:

```
Compare monthly sales across regions
Show growth trend of revenue over 5 years
Display distribution of customer ages
Show market share percentages by product
Analyze relationship between price and demand
Compare Q1 vs Q2 performance
Track website traffic over time
Display order frequency by customer segment
Show revenue composition by category
Examine correlation between marketing spend and sales
```

---

## 🚨 Troubleshooting

### App won't start?
```powershell
# Check if port is in use
netstat -ano | findstr :8502

# Use different port
streamlit run app_enhanced.py --server.port 8503
```

### Upload fails?
- Check file size (< 200MB recommended)
- Verify CSV encoding (UTF-8)
- Remove special characters
- Check for corrupted data

### No insights generated?
- Ensure revenue/sales columns exist
- Check column names contain keywords
- Verify numeric data types
- Remove empty rows

---

## 🎊 Success Checklist

After uploading data, you should see:

- ✅ "Loaded X rows and Y columns" message
- ✅ Data preview table
- ✅ 5 business insights with recommendations
- ✅ 5 interactive visualizations
- ✅ Data summary statistics
- ✅ Export buttons

If any missing, check data format and column names.

---

## 📞 Quick Help

| Issue | Solution |
|-------|----------|
| Can't upload file | Check file format (CSV/Excel) |
| No charts shown | Verify data has numeric columns |
| No insights | Check column names match patterns |
| App is slow | Reduce data size or use sampling |
| Charts not interactive | Use latest Plotly version |

---

## 🎓 Learning Path

### Beginner:
1. Try Mode 1 with example goals
2. Upload sample data in Mode 2
3. Explore generated insights

### Intermediate:
4. Upload your own business data
5. Customize insights in code
6. Add new visualization types

### Advanced:
7. Integrate via API
8. Customize color schemes
9. Add new insight categories
10. Deploy to production

---

## 🌟 Key Features Summary

| Feature | Description | Benefit |
|---------|-------------|---------|
| 🤖 Auto-Detection | Finds revenue, categories, dates | No setup needed |
| 💡 Smart Insights | 5 business recommendations | Actionable advice |
| 📊 Auto Charts | 5 visualizations created | Instant visual analysis |
| 🎨 Interactive | Plotly charts with zoom/hover | Professional output |
| 📥 Export | Multiple format options | Share with team |
| 🚀 Fast | Process 100K+ rows quickly | Production ready |

---

## 🎯 One-Minute Workflow

```
1. Open http://localhost:8502
2. Click "Analyze My Data"
3. Upload your CSV
4. Review 5 insights
5. Explore 5 charts
6. Export reports
7. Take action!
```

**Total time: < 60 seconds** ⚡

---

## 📚 More Documentation

- **ENHANCED_FEATURES.md** - Complete feature list
- **README.md** - Full documentation  
- **QUICKSTART.md** - Getting started
- **SETUP_COMPLETE.md** - Setup summary

---

## 🎉 You're Ready!

Open **http://localhost:8502** and start analyzing! 📊✨

**Remember:** Upload data → Get insights → Take action → Improve business! 🚀
