# 🚀 AWS AMPLIFY DEPLOYMENT GUIDE

## 📋 Hướng dẫn deploy License Optimization System lên AWS Amplify

### 🎯 **BƯỚC 1: Chuẩn bị**

#### 1.1 Kiểm tra files cần thiết
```
license-optimization/
├── amplify.yml          ✅ Build configuration
├── app.py              ✅ Amplify entry point  
├── streamlit_app.py    ✅ Main application
├── requirements.txt    ✅ Dependencies
└── src/               ✅ Core modules
```

#### 1.2 Push code lên GitHub
```bash
git add .
git commit -m "Add Amplify deployment config"
git push origin main
```

---

### 🌐 **BƯỚC 2: Tạo Amplify App**

#### 2.1 Truy cập AWS Console
1. Đăng nhập [AWS Console](https://console.aws.amazon.com)
2. Tìm kiếm "AWS Amplify"
3. Click "Create new app"

#### 2.2 Connect Repository
1. Chọn "GitHub" 
2. Authorize AWS Amplify
3. Chọn repository: `license-optimization`
4. Chọn branch: `main`

---

### ⚙️ **BƯỚC 3: Cấu hình Build**

#### 3.1 Build Settings
- **App name**: `license-optimization`
- **Environment**: `production`
- **Build command**: Tự động detect từ `amplify.yml`

#### 3.2 Environment Variables
Thêm các biến môi trường:
```
AWS_DEFAULT_REGION=us-east-1
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

#### 3.3 Advanced Settings
- **Build timeout**: 30 minutes
- **Compute type**: Small (1 vCPU, 3GB RAM)
- **Operating system**: Amazon Linux 2

---

### 🔧 **BƯỚC 4: Deploy**

#### 4.1 Start Deployment
1. Click "Save and deploy"
2. Theo dõi build process:
   - Provision → Build → Deploy → Verify

#### 4.2 Build Process
```
Phase 1: Provision (2-3 phút)
├── Create build environment
├── Install Python 3.9
└── Setup networking

Phase 2: Build (5-7 phút)  
├── Install dependencies
├── Run pip install -r requirements.txt
└── Prepare application files

Phase 3: Deploy (2-3 phút)
├── Upload to CDN
├── Configure routing
└── Health checks

Phase 4: Verify (1 phút)
└── Final validation
```

---

### 🌍 **BƯỚC 5: Truy cập App**

#### 5.1 Get URL
- URL format: `https://main.d1234567890.amplifyapp.com`
- Custom domain có thể setup sau

#### 5.2 Test Features
1. **Dashboard** - Metrics và charts
2. **License Management** - CRUD operations  
3. **Usage Analysis** - Analytics
4. **ML Recommendations** - AI insights
5. **Operations** - Health monitoring

---

### 🔄 **BƯỚC 6: Auto Deployment**

#### 6.1 Continuous Deployment
- Mỗi khi push code → Auto deploy
- Build time: ~10-15 phút
- Zero downtime deployment

#### 6.2 Branch Management
```bash
# Development
git checkout -b develop
git push origin develop
# Tạo separate Amplify app cho develop branch

# Production  
git checkout main
git push origin main
# Auto deploy to production
```

---

### 📊 **MONITORING & LOGS**

#### 7.1 Build Logs
- Real-time build progress
- Error debugging
- Performance metrics

#### 7.2 Access Logs
- Traffic analytics
- User behavior
- Performance monitoring

---

### 💰 **CHI PHÍ AMPLIFY**

#### Free Tier (12 tháng đầu)
- **Build minutes**: 1,000 phút/tháng
- **Storage**: 5GB
- **Data transfer**: 15GB/tháng
- **Requests**: 1 triệu/tháng

#### Sau Free Tier
- **Build**: $0.01/phút
- **Hosting**: $0.15/GB/tháng
- **Requests**: $0.20/1M requests

**Ước tính**: $5-15/tháng cho production app

---

### 🛠️ **TROUBLESHOOTING**

#### Build Failures
```bash
# Common issues:
1. Python version mismatch
   → Specify python_version in amplify.yml

2. Dependencies error  
   → Check requirements.txt format

3. Memory limit
   → Increase compute type to Medium

4. Timeout
   → Increase build timeout to 45 minutes
```

#### Runtime Issues
```bash
# App not loading:
1. Check CloudWatch logs
2. Verify environment variables
3. Test locally first: streamlit run streamlit_app.py
```

---

### 🎯 **PRODUCTION CHECKLIST**

#### Pre-deployment
- [ ] Code tested locally
- [ ] Requirements.txt updated
- [ ] Environment variables set
- [ ] AWS credentials configured

#### Post-deployment  
- [ ] App loads successfully
- [ ] All features working
- [ ] Database connectivity
- [ ] Performance acceptable

#### Monitoring
- [ ] CloudWatch alarms setup
- [ ] Error tracking enabled
- [ ] Performance monitoring
- [ ] Backup strategy

---

### 🚀 **NEXT STEPS**

#### Custom Domain
1. Purchase domain (Route 53 hoặc external)
2. Add to Amplify app
3. SSL certificate auto-generated

#### Advanced Features
- **Authentication**: Cognito integration
- **API Gateway**: REST API endpoints  
- **Lambda Functions**: Serverless backend
- **RDS**: Relational database option

---

**🎉 APP SẴN SÀNG DEPLOY LÊN AWS AMPLIFY!**

**URL sau khi deploy**: `https://main.d[app-id].amplifyapp.com`