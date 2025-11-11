# 🚀 Deployment Notes

## Chart Export Feature

### PNG Export (Optional)
The application includes optional PNG export functionality for charts. This feature requires:
- **Kaleido** Python package (included in requirements.txt)
- **Chrome/Chromium** browser installed on the system

### Behavior in Different Environments

#### ✅ Local Development (with Chrome)
- PNG download buttons appear for all charts
- Users can download charts as high-quality PNG images
- Works when Chrome is installed on the development machine

#### ⚠️ Cloud Deployment (without Chrome)
- **Streamlit Cloud**: Chrome is not pre-installed
- **AWS/Azure/GCP**: May not have Chrome by default
- **Result**: PNG export gracefully disabled
- **User Experience**: 
  - No error messages
  - Info message explains PNG export unavailable
  - All charts still fully interactive
  - Users can screenshot or use browser's built-in tools

### Why This Design?

1. **Graceful Degradation**: App works perfectly without PNG export
2. **Cloud-Friendly**: Most cloud platforms don't have Chrome
3. **User Experience**: Charts are still fully functional
4. **Alternative Solutions**: Users can:
   - Use browser screenshot tools
   - Right-click charts → "Save image as"
   - Use OS screenshot shortcuts
   - Install Chrome locally if needed

## Streamlit Cloud Deployment

### Prerequisites
✅ GitHub repository: https://github.com/VedantJadhav701/bizviz
✅ Main file: `app_enhanced.py`
✅ Requirements: Listed in `requirements.txt`
✅ Secrets: GROQ_API_KEY needs to be configured

### Deployment Steps

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub

2. **Deploy App**
   - Click "New app"
   - Select repository: `VedantJadhav701/bizviz`
   - Branch: `main`
   - Main file path: `app_enhanced.py`

3. **Configure Secrets**
   - Click "Advanced settings"
   - Under "Secrets", add:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for deployment
   - Your app will be live!

### Expected Behavior on Streamlit Cloud

✅ **What Works:**
- 200MB file uploads
- Universal chart generation (5-8 charts)
- User intent detection
- Interactive Plotly charts
- All data analysis features
- Groq AI insights

⚠️ **What's Limited:**
- PNG export buttons won't appear (Chrome not available)
- Users see helpful message about PNG export
- All other features work normally

### Alternative PNG Export Solutions

If PNG export is critical:

1. **Local Installation** (Recommended for Development)
   ```bash
   pip install kaleido
   # Install Chrome browser
   ```

2. **Docker Deployment** (For Full Control)
   ```dockerfile
   FROM python:3.10
   RUN apt-get update && apt-get install -y chromium
   ENV CHROME_PATH=/usr/bin/chromium
   ```

3. **Heroku/Railway** (Buildpacks Available)
   - Use Chrome buildpack
   - Add to `app.json` or `Procfile`

4. **AWS EC2/Azure VM** (Full Control)
   - Install Chrome manually
   - Full PNG export support

## Testing Checklist

Before deploying:
- ✅ Test with 200MB file locally
- ✅ Verify 5-8 charts generate
- ✅ Test user intent detection
- ✅ Confirm app runs without PNG export
- ✅ Check Groq API key in secrets.toml
- ✅ Verify .gitignore excludes secrets

After deploying:
- ⬜ Confirm app loads on Streamlit Cloud
- ⬜ Test file upload (up to 200MB)
- ⬜ Verify charts generate
- ⬜ Check AI insights work
- ⬜ Confirm user intent detection
- ⬜ Verify no error messages

## Troubleshooting

### Issue: "Kaleido requires Chrome" error
**Solution**: This is now handled gracefully. If you see this error:
1. The app will continue working
2. PNG export will be disabled
3. Users see helpful info message

### Issue: Charts not generating
**Solution**: 
1. Check file format (CSV, XLSX, XLS)
2. Verify file size < 200MB
3. Check Streamlit Cloud logs for errors

### Issue: AI insights not working
**Solution**:
1. Verify GROQ_API_KEY in Streamlit secrets
2. Check API key is valid
3. Review API quota limits

## Performance Notes

### Data Sampling
- **Full dataset**: Used for calculations and statistics
- **Sampled data (10K rows)**: Used for visualizations
- **Reason**: Maintains performance with large files

### File Size Limits
- **Maximum**: 200MB
- **Recommended**: < 100MB for best performance
- **Cloud constraints**: Streamlit Cloud may have lower limits

### Chart Generation
- **Minimum**: 5 charts guaranteed
- **Maximum**: 8 charts typically
- **Time**: 2-10 seconds depending on file size

## Support

Need help?
1. Check logs in Streamlit Cloud dashboard
2. Review this documentation
3. Test locally first
4. Check GitHub Issues

---

**Last Updated**: After Kaleido/Chrome fix
**Status**: ✅ Ready for Streamlit Cloud deployment
