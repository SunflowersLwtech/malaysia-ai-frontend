# 🌏 Malaysia Tourism AI - Frontend

A modern Streamlit interface for the Malaysia Tourism AI chatbot, powered by a fine-tuned Gemini model.

## 🚀 Render Free Tier Deployment

### ✅ Free Tier Advantages:

  - 750 free instance hours per month
  - Automatic HTTPS/SSL certificates
  - Support for environment variable configuration
  - Auto-deploy from GitHub

### ⚠️ Free Tier Limitations:

  - **Instance Spindown**: The service automatically spins down after 15 minutes of inactivity.
  - **Cold Start**: Waking up from a spun-down state can take 10-30 seconds.
  - **Memory Limit**: 512MB RAM
  - **CPU Limit**: Shared CPU resources

### 🔧 Deployment Configuration:

```yaml
# render.yaml (frontend section)
services:
  - type: web
    name: malaysia-ai-frontend  
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --server.enableCORS false
    envVars:
      - key: API_BASE_URL
        value: https://malaysia-ai-backend.onrender.com # Your backend service URL
    autoDeploy: true
```

### 📋 Dependencies:

```txt
streamlit>=1.28.0
requests>=2.28.0  
google-generativeai>=0.3.0
google-auth>=2.17.0
```

## 💡 Optimization Suggestions:

### 1\. **Mitigating Cold Starts:**

  - Use an uptime monitoring service (e.g., UptimeRobot).
  - Configure it to periodically ping the service's health check endpoint to keep it active.

### 2\. **User Experience Optimization:**

  - On the frontend, add a "Service is starting, please wait..." message when an API call times out.
  - Implement a retry mechanism in the frontend for API calls that fail due to a cold start.
  - Cache frequently requested or non-dynamic responses.

### 3\. **Resource Optimization:**

  - Minimize the packages in `requirements.txt` to only what is essential.
  - Optimize the size of images and other static assets.
  - Leverage Streamlit's built-in caching features (`@st.cache_data`, `@st.cache_resource`).

## 🌐 Access URLs:

  - **Frontend**: `https://malaysia-ai-frontend.onrender.com`
  - **Backend**: `https://malaysia-ai-backend.onrender.com`

## 🔍 Monitoring:

  - **Health Check Endpoint**: `/health`
  - **Status Page**: [Render Dashboard](https://dashboard.render.com)

-----

**Note**: The free tier service will spin down after a period of inactivity. The first visit after a period of rest may require a short wait for the service to start up.
