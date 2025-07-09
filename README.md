# 🌏 Malaysia Tourism AI - Frontend

Modern Streamlit interface for Malaysia Tourism AI chatbot using fine-tuned Gemini model.

## 🚀 Render Free Tier Deployment

### ✅ 免费版优势:
- 每月 750 小时免费使用
- 自动 HTTPS 证书
- 支持环境变量配置
- GitHub 自动部署

### ⚠️ 免费版限制:
- **服务休眠**: 15分钟不活动后自动休眠
- **冷启动**: 唤醒需要 10-30 秒
- **内存限制**: 512MB RAM
- **CPU限制**: 共享 CPU 资源

### 🔧 部署配置:

```yaml
# render.yaml (frontend部分)
- type: web
  name: malaysia-ai-frontend  
  env: python
  buildCommand: pip install -r requirements.txt
  startCommand: streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --server.enableCORS false
  envVars:
    - key: API_BASE_URL
      value: https://malaysia-ai-backend.onrender.com
  autoDeploy: true
```

### 📋 Dependencies:
```
streamlit>=1.28.0
requests>=2.28.0  
google-generativeai>=0.3.0
google-auth>=2.17.0
```

## 💡 优化建议:

### 1. **减少冷启动影响:**
- 使用 uptime monitoring 服务 (如 UptimeRobot)
- 定期 ping 服务保持活跃

### 2. **用户体验优化:**
- 添加"服务启动中"提示
- 实现重试机制
- 缓存常用响应

### 3. **资源优化:**
- 最小化依赖包
- 优化图片和静态资源
- 使用 Streamlit 缓存功能

## 🌐 Access URLs:
- **Frontend**: https://malaysia-ai-frontend.onrender.com
- **Backend**: https://malaysia-ai-backend.onrender.com

## 🔍 监控:
- 健康检查: `/health`  
- 状态页面: [Render Dashboard](https://dashboard.render.com)

---
**Note**: 免费版服务会在不活动后休眠，首次访问可能需要等待启动。
