# 🔧 Troubleshooting Guide

This guide helps you resolve common issues when setting up and running the Startup Analytics Tutorial Dashboard.

## 🚀 Quick Start Issues

### **Problem: "ModuleNotFoundError: No module named 'flask'"**

**Symptoms:**
```
Traceback (most recent call last):
  File "run.py", line 2, in <module>
    from app import create_app
  File "app/__init__.py", line 1, in <module>
    from flask import Flask
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
1. **Activate the virtual environment:**
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run with virtual environment Python:**
   ```bash
   # Windows
   .\venv\Scripts\python.exe run.py
   
   # macOS/Linux
   ./venv/bin/python run.py
   ```

### **Problem: "Port already in use"**

**Symptoms:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**
1. **Find and kill the process using port 5000:**
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID_NUMBER> /F
   
   # macOS/Linux
   lsof -ti:5000 | xargs kill -9
   ```

2. **Or use a different port:**
   ```bash
   PORT=5001 python run.py
   ```

## 📊 Calculation Issues

### **Problem: "LTV calculation seems wrong"**

**Symptoms:**
- LTV shows unexpected values
- Calculations don't match expected results

**Solution:**
1. **Check the data file:**
   ```bash
   # Verify data/business_metrics.json exists and has correct values
   cat data/business_metrics.json
   ```

2. **Run validation tests:**
   ```bash
   .\venv\Scripts\python.exe test_simple.py
   ```

3. **Verify LTV formula:**
   - **Stripe Method**: `LTV = ARPU ÷ Churn Rate`
   - **Example**: `$20.83 ÷ 0.052 = $400.58`

### **Problem: "API endpoints not working"**

**Symptoms:**
- Dashboard shows static values instead of calculated ones
- API calls return errors

**Solution:**
1. **Test API endpoints:**
   ```bash
   .\venv\Scripts\python.exe test_flask_only.py
   ```

2. **Check Flask routes:**
   ```bash
   curl http://localhost:5000/api/metrics
   ```

3. **Verify metrics calculator:**
   ```bash
   .\venv\Scripts\python.exe app/services/metrics_calculator.py
   ```

## 🔗 GA4 Integration Issues

### **Problem: "GA4 connection failed"**

**Symptoms:**
- Dashboard shows "Demo Data" instead of real GA4 data
- Error messages about GA4 configuration

**Solution:**
1. **Check environment variables:**
   ```bash
   # Verify these are set
   echo $GA4_PROPERTY_ID
   echo $GA4_CREDENTIALS_PATH
   ```

2. **Follow the GA4 integration guide:**
   - See `GA4_INTEGRATION_GUIDE.md`
   - Set up Google Cloud credentials
   - Configure GA4 API access

3. **Use demo data for testing:**
   - The app works with mock data by default
   - Real GA4 integration is optional

### **Problem: "GA4 API quota exceeded"**

**Symptoms:**
- API calls return 429 errors
- "Quota exceeded" messages

**Solution:**
1. **Check your GA4 API quota:**
   - Visit Google Cloud Console
   - Monitor API usage in the dashboard

2. **Implement rate limiting:**
   - Add delays between API calls
   - Cache results to reduce API usage

3. **Use demo data:**
   - The app falls back to mock data automatically

## 🧪 Testing Issues

### **Problem: "Tests are failing"**

**Symptoms:**
- Test suite shows errors
- Some tests don't pass

**Solution:**
1. **Run tests with virtual environment:**
   ```bash
   .\venv\Scripts\python.exe test_calculations.py
   ```

2. **Check individual test components:**
   ```bash
   .\venv\Scripts\python.exe test_simple.py
   .\venv\Scripts\python.exe test_flask_only.py
   ```

3. **Verify data file integrity:**
   ```bash
   .\venv\Scripts\python.exe -c "import json; print(json.load(open('data/business_metrics.json')))"
   ```

### **Problem: "Expected values don't match"**

**Symptoms:**
- Test assertions fail
- Calculations differ from expected results

**Solution:**
1. **Check calculation accuracy:**
   - Verify LTV: `$20.83 ÷ 0.052 = $400.58`
   - Verify MRR: `2,400 × $20.83 = $49,992`

2. **Update expected values if needed:**
   - Edit test files if calculations are correct
   - Report inconsistencies on GitHub

## 🌐 Deployment Issues

### **Problem: "App won't start on Railway/Heroku"**

**Symptoms:**
- Deployment fails
- App crashes on startup

**Solution:**
1. **Check Procfile:**
   ```
   web: python run.py
   ```

2. **Verify requirements.txt:**
   ```
   Flask==3.0.0
   Flask-Cors==4.0.0
   ```

3. **Check environment variables:**
   - Set `PORT` environment variable
   - Configure GA4 credentials if needed

### **Problem: "Static files not loading"**

**Symptoms:**
- CSS/JS not loading
- Dashboard looks broken

**Solution:**
1. **Check static file configuration:**
   - Verify `static_folder` in Flask app
   - Ensure files are in correct directories

2. **Use CDN resources:**
   - The app uses CDN for Tailwind CSS and Chart.js
   - No local static files required

## 🤖 AI-Generated Content Issues

### **Problem: "Calculations seem incorrect"**

**Symptoms:**
- Metrics don't match your expectations
- Formulas appear wrong

**Solution:**
1. **Verify with industry standards:**
   - LTV = ARPU ÷ Churn Rate (Stripe method)
   - MRR = Active Users × ARPU
   - ARR = MRR × 12

2. **Cross-reference with other sources:**
   - Check SaaS industry benchmarks
   - Verify with your own calculations

3. **Report inconsistencies:**
   - Open an issue on [GitHub](https://github.com/safinayah/startup-analytics-tutorial)
   - Provide your expected values and reasoning

## 📞 Getting Help

### **Still having issues?**

1. **Check the logs:**
   ```bash
   # Run with debug mode
   FLASK_DEBUG=1 python run.py
   ```

2. **Run comprehensive tests:**
   ```bash
   .\venv\Scripts\python.exe test_calculations.py
   ```

3. **Report the issue:**
   - Open an issue on [GitHub](https://github.com/safinayah/startup-analytics-tutorial)
   - Include error messages and steps to reproduce
   - Provide your system information (OS, Python version)

### **Common Solutions Summary**

| Problem | Quick Fix |
|---------|-----------|
| Flask not found | Activate virtual environment |
| Port in use | Kill process or use different port |
| Tests failing | Run with venv Python |
| GA4 not working | Use demo data (default) |
| Calculations wrong | Verify with industry standards |
| Deployment fails | Check Procfile and requirements.txt |

---

**🤖 Remember: This troubleshooting guide is AI-generated. If you find any issues or have suggestions for improvement, please report them on [GitHub](https://github.com/safinayah/startup-analytics-tutorial)!**
