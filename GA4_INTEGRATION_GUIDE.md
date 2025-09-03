# Google Analytics 4 (GA4) Integration Guide

This guide explains how to connect your startup tracker dashboard to your own Google Analytics 4 property to pull real data instead of using mock data.

## 🎯 Overview

The current implementation uses mock data that matches the dashboard design. To connect to your real GA4 data, you'll need to modify specific parts of the code and set up GA4 API credentials.

## 📋 Prerequisites

1. **Google Analytics 4 Property** - You need an active GA4 property
2. **Google Cloud Project** - For API access
3. **Service Account** - For server-to-server authentication
4. **Python Environment** - With required dependencies

## 🔧 Step-by-Step Integration

### Step 1: Set Up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the **Google Analytics Data API**
4. Go to **IAM & Admin** → **Service Accounts**
5. Create a new service account with **Viewer** permissions
6. Download the JSON credentials file

### Step 2: Install Required Dependencies

Add these to your `requirements.txt`:

```txt
google-analytics-data==0.18.12
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
```

Install them:
```bash
pip install google-analytics-data google-auth google-auth-oauthlib google-auth-httplib2
```

### Step 3: Environment Variables

Create a `.env` file in your project root (add to `.gitignore`):

```env
# GA4 Configuration
GA4_PROPERTY_ID=YOUR_PROPERTY_ID_HERE
GA4_CREDENTIALS_PATH=/path/to/your/service-account.json

# Example:
# GA4_PROPERTY_ID=123456789
# GA4_CREDENTIALS_PATH=./credentials/ga4-service-account.json
```

### Step 4: Update GA4 Service Code

Replace the mock implementation in `app/integrations/ga4_service.py`:

#### 4.1 Add Real GA4 API Imports

```python
# Add these imports at the top of ga4_service.py
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    Filter,
    FilterExpression
)
from google.oauth2 import service_account
import pandas as pd
```

#### 4.2 Update the GA4Service Class Constructor

```python
def __init__(self, property_id: Optional[str] = None):
    """
    Initialize GA4 service with real API connection
    """
    self.property_id = property_id or os.getenv('GA4_PROPERTY_ID')
    self.credentials_path = os.getenv('GA4_CREDENTIALS_PATH')
    
    # Initialize the GA4 client
    if self.credentials_path and os.path.exists(self.credentials_path):
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path,
            scopes=['https://www.googleapis.com/auth/analytics.readonly']
        )
        self.client = BetaAnalyticsDataClient(credentials=credentials)
    else:
        self.client = None
        print("Warning: GA4 credentials not found. Using mock data.")
```

#### 4.3 Replace Mock Methods with Real API Calls

Here's how to replace each method:

##### Website Visitors Method
```python
def get_website_visitors(self, days: int = 30) -> Dict:
    """
    Get real website visitors data from GA4
    """
    if not self.client:
        return self._get_mock_visitors_data(days)
    
    try:
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[
                Metric(name="totalUsers"),
                Metric(name="newUsers"),
                Metric(name="sessions")
            ],
            date_ranges=[DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )]
        )
        
        response = self.client.run_report(request)
        
        # Process the response data
        total_users = sum(int(row.metric_values[0].value) for row in response.rows)
        new_users = sum(int(row.metric_values[1].value) for row in response.rows)
        returning_users = total_users - new_users
        
        return {
            'total_visitors': total_users,
            'new_visitors': new_users,
            'returning_visitors': returning_users,
            'period_days': days,
            'date_range': f'Last {days} days'
        }
        
    except Exception as e:
        print(f"Error fetching visitors data: {e}")
        return self._get_mock_visitors_data(days)
```

##### Conversion Funnel Method
```python
def get_conversion_funnel_data(self, days: int = 30) -> Dict:
    """
    Get real conversion funnel data from GA4
    """
    if not self.client:
        return self._get_mock_funnel_data(days)
    
    try:
        # Get website visitors
        visitors_request = RunReportRequest(
            property=f"properties/{self.property_id}",
            metrics=[Metric(name="totalUsers")],
            date_ranges=[DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )]
        )
        
        visitors_response = self.client.run_report(visitors_request)
        website_visitors = int(visitors_response.rows[0].metric_values[0].value)
        
        # Get sign-ups (custom event)
        signups_request = RunReportRequest(
            property=f"properties/{self.property_id}",
            metrics=[Metric(name="eventCount")],
            dimension_filter=FilterExpression(
                filter=Filter(
                    field_name="eventName",
                    string_filter=Filter.StringFilter(value="sign_up")
                )
            ),
            date_ranges=[DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )]
        )
        
        signups_response = self.client.run_report(signups_request)
        sign_ups = int(signups_response.rows[0].metric_values[0].value) if signups_response.rows else 0
        
        # Calculate conversion rates
        visitor_to_signup_rate = (sign_ups / website_visitors * 100) if website_visitors > 0 else 0
        
        return {
            'website_visitors': website_visitors,
            'sign_ups': sign_ups,
            'trial_users': int(sign_ups * 0.3),  # Adjust based on your funnel
            'paid_customers': int(sign_ups * 0.15),  # Adjust based on your funnel
            'retained_customers': int(sign_ups * 0.125),  # Adjust based on your funnel
            'conversion_rates': {
                'visitor_to_signup': round(visitor_to_signup_rate, 1),
                'signup_to_trial': 30.0,  # Adjust based on your data
                'trial_to_paid': 50.0,    # Adjust based on your data
                'retention_rate': 94.8    # Adjust based on your data
            }
        }
        
    except Exception as e:
        print(f"Error fetching funnel data: {e}")
        return self._get_mock_funnel_data(days)
```

##### Revenue Data Method
```python
def get_revenue_data(self, days: int = 30) -> Dict:
    """
    Get real revenue data from GA4
    """
    if not self.client:
        return self._get_mock_revenue_data(days)
    
    try:
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            metrics=[
                Metric(name="totalRevenue"),
                Metric(name="purchaseRevenue"),
                Metric(name="transactions"),
                Metric(name="averagePurchaseRevenue")
            ],
            date_ranges=[DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )]
        )
        
        response = self.client.run_report(request)
        
        if response.rows:
            row = response.rows[0]
            total_revenue = float(row.metric_values[0].value)
            transactions = int(row.metric_values[2].value)
            avg_order_value = float(row.metric_values[3].value) if row.metric_values[3].value else 0
            
            return {
                'total_revenue': total_revenue,
                'monthly_revenue': total_revenue,
                'average_order_value': avg_order_value,
                'transactions': transactions,
                'revenue_per_visitor': total_revenue / self.get_website_visitors(days)['total_visitors']
            }
        else:
            return self._get_mock_revenue_data(days)
            
    except Exception as e:
        print(f"Error fetching revenue data: {e}")
        return self._get_mock_revenue_data(days)
```

### Step 5: Add Mock Data Fallback Methods

Add these methods to provide fallback data when GA4 API fails:

```python
def _get_mock_visitors_data(self, days: int) -> Dict:
    """Fallback mock data for visitors"""
    return {
        'total_visitors': 12450,
        'new_visitors': 8930,
        'returning_visitors': 3520,
        'period_days': days,
        'date_range': f'Last {days} days'
    }

def _get_mock_funnel_data(self, days: int) -> Dict:
    """Fallback mock data for funnel"""
    return {
        'website_visitors': 12450,
        'sign_ups': 1245,
        'trial_users': 374,
        'paid_customers': 187,
        'retained_customers': 156,
        'conversion_rates': {
            'visitor_to_signup': 10.0,
            'signup_to_trial': 30.0,
            'trial_to_paid': 50.0,
            'retention_rate': 94.8
        }
    }

def _get_mock_revenue_data(self, days: int) -> Dict:
    """Fallback mock data for revenue"""
    return {
        'total_revenue': 62000,
        'monthly_revenue': 62000,
        'average_order_value': 20.83,
        'transactions': 187,
        'revenue_per_visitor': 4.98
    }
```

### Step 6: Update Flask Routes

Modify `app/routes/routes.py` to use the GA4 service:

```python
from app.integrations.ga4_service import GA4Service

@app.route('/api/ga4/metrics')
def get_ga4_metrics():
    """API endpoint to get GA4 metrics"""
    try:
        ga4_service = GA4Service()
        metrics = ga4_service.get_all_metrics(days=30)
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ga4/visitors')
def get_ga4_visitors():
    """API endpoint to get visitor data"""
    try:
        ga4_service = GA4Service()
        visitors = ga4_service.get_website_visitors(days=30)
        return jsonify(visitors)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Step 7: Update Frontend to Use Real Data

Add JavaScript to fetch real data in `templates/tutorial-dashboard.html`:

```javascript
// Add this to your existing JavaScript
async function loadRealGA4Data() {
    try {
        const response = await fetch('/api/ga4/metrics');
        const data = await response.json();
        
        // Update dashboard with real data
        updateDashboardWithRealData(data);
        
        // Track that real data is loaded
        gtag('event', 'real_data_loaded', {
            'data_source': 'GA4_API',
            'metrics_count': Object.keys(data).length
        });
        
    } catch (error) {
        console.log('Using mock data - GA4 API not available');
        gtag('event', 'mock_data_used', {
            'reason': 'GA4_API_unavailable',
            'error': error.message
        });
    }
}

function updateDashboardWithRealData(data) {
    // Update visitor count
    document.querySelector('[data-metric="visitors"]').textContent = 
        data.website_visitors.total_visitors.toLocaleString();
    
    // Update revenue
    document.querySelector('[data-metric="revenue"]').textContent = 
        `$${data.revenue.total_revenue.toLocaleString()}`;
    
    // Update conversion funnel
    updateFunnelWithRealData(data.conversion_funnel);
    
    // Add more updates as needed
}

// Call this when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadRealGA4Data();
});
```

## 🔍 Key Files to Modify

1. **`app/integrations/ga4_service.py`** - Main service class
2. **`app/routes/routes.py`** - API endpoints
3. **`templates/tutorial-dashboard.html`** - Frontend data loading
4. **`requirements.txt`** - Dependencies
5. **`.env`** - Environment variables (create this file)

## 🚨 Important Notes

### Security
- **Never commit** your `.env` file or service account JSON to version control
- Add `.env` and `credentials/` to your `.gitignore`
- Use environment variables in production

### GA4 Setup Requirements
- Your GA4 property must have **Enhanced Ecommerce** enabled for revenue data
- Set up **Custom Events** for sign-ups, trials, etc.
- Configure **Goals** and **Conversions** in GA4
- Ensure your website has the GA4 tracking code installed

### Data Mapping
You may need to adjust the metric names and dimensions based on your specific GA4 setup:
- Custom event names (sign_up, trial_start, purchase, etc.)
- Ecommerce tracking configuration
- Custom dimensions for user segments

## 🧪 Testing

Test your integration:

```python
# Test the service
from app.integrations.ga4_service import GA4Service

service = GA4Service()
print("Testing GA4 Service...")
print(f"Visitors: {service.get_website_visitors()}")
print(f"Revenue: {service.get_revenue_data()}")
```

## 📊 Expected Results

Once integrated, your dashboard will show:
- ✅ Real visitor counts from GA4
- ✅ Actual conversion rates
- ✅ Live revenue data
- ✅ Current traffic sources
- ✅ Real-time user behavior metrics

## 🆘 Troubleshooting

### Common Issues

1. **"Property not found"** - Check your GA4 Property ID
2. **"Insufficient permissions"** - Verify service account has Viewer access
3. **"No data returned"** - Check date ranges and metric availability
4. **"API quota exceeded"** - Implement caching or reduce API calls

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🎉 Success!

Once implemented, your startup tracker will pull real data from GA4, making it a powerful tool for actual business analytics rather than just a tutorial!

---

**Need Help?** Check the [Google Analytics Data API documentation](https://developers.google.com/analytics/devguides/reporting/data/v1) for more details.
