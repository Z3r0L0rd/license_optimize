# 🎯 License Optimization System

## 📋 Mô tả dự án
Hệ thống theo dõi và tối ưu hóa license phần mềm với chi phí thấp sử dụng AWS.

## ✨ Tính năng chính
- ✅ **License Tracking** - Theo dõi license với CRUD operations
- ✅ **Usage Analysis** - Phân tích sử dụng và tối ưu hóa
- ✅ **Compliance Monitoring** - Giám sát tuân thủ và risk assessment
- ✅ **ML Recommendations** - AI-powered cost optimization
- ✅ **Executive Dashboard** - Báo cáo tổng quan cho leadership
- ✅ **Operations Center** - Automated workflows và monitoring
- ✅ **Audit System** - Change tracking và compliance auditing
- ✅ **Data Management** - Import/export CSV với auto-setup

## 🚀 Công nghệ sử dụng
- **Backend**: Python 3.9+, AWS DynamoDB, S3, CloudWatch
- **Frontend**: Streamlit với interactive sidebar
- **ML/Analytics**: Pandas, Plotly, Custom ML algorithms
- **Infrastructure**: AWS Free Tier services

## 📦 Cài đặt nhanh

### 1. Clone và setup
```bash
git clone <repository>
cd license-optimization
pip install -r requirements.txt
```

### 2. Cấu hình AWS
```bash
aws configure
# Nhập AWS credentials và chọn region us-east-1
```

### 3. Chạy ứng dụng
```bash
python run_app.py
```
Truy cập: http://localhost:8501

## 🎯 Sử dụng

### Web Interface (Khuyến nghị)
- **Dashboard**: Tổng quan metrics và charts
- **License Management**: CRUD operations với validation
- **Usage Analysis**: Phân tích underutilized/overutilized
- **ML Recommendations**: AI-powered cost optimization
- **Operations**: Daily operations, health check, backup
- **Data Management**: Import/export CSV với auto-setup

### Command Line
```bash
cd src
python main.py
```

## 💰 Chi phí (AWS Free Tier)
- **DynamoDB**: 25GB storage miễn phí
- **S3**: 5GB storage miễn phí  
- **CloudWatch**: Monitoring cơ bản miễn phí
- **Tổng**: $0-5/tháng (sau khi hết Free Tier)

## 📊 Kiến trúc hệ thống

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Core Engine    │    │   AWS Services  │
│   Web App       │◄──►│   - Tracker      │◄──►│   - DynamoDB    │
│   - Dashboard   │    │   - Analyzer     │    │   - S3          │
│   - Management  │    │   - ML Engine    │    │   - CloudWatch  │
│   - Analytics   │    │   - Operations   │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔧 Tính năng nâng cao

### Phase 1: Core System ✅
- License CRUD operations
- Usage analysis và compliance
- Web interface với Streamlit
- Bulk import/export CSV

### Phase 2: Advanced Analytics ✅  
- ML-powered recommendations
- Executive summary reporting
- Risk assessment và scoring
- Predictive analytics

### Phase 3: Enterprise Ready ✅
- Real-time monitoring
- Automated operations
- Comprehensive auditing
- Interactive sidebar với search

## 📁 Cấu trúc project

```
license-optimization/
├── src/                    # Core modules
│   ├── license_tracker.py  # CRUD operations
│   ├── usage_analyzer.py   # Usage analysis
│   ├── ml_recommender.py   # ML recommendations
│   ├── operations.py       # Automated operations
│   └── audit_system.py     # Audit và compliance
├── docs/                   # Documentation
├── config/                 # Configuration files
├── streamlit_app.py        # Web interface
├── run_app.py             # App launcher
└── requirements.txt        # Dependencies
```

## 🎯 Business Value

### Cost Savings
- Identify underutilized licenses (tiết kiệm 20-40%)
- Optimize license allocation
- Predict future needs
- Reduce compliance risks

### Operational Excellence  
- Automated daily operations
- Real-time health monitoring
- Comprehensive audit trails
- Executive-ready reporting

## 🚀 Roadmap

### Completed ✅
- [x] Core license management
- [x] Advanced analytics với ML
- [x] Enterprise operations
- [x] Interactive web interface

### Future Enhancements
- [ ] Multi-tenant support
- [ ] Advanced integrations (LDAP, SSO)
- [ ] Mobile app
- [ ] Advanced ML models

## 📞 Hỗ trợ

**Troubleshooting:**
1. Kiểm tra AWS credentials: `aws sts get-caller-identity`
2. Xem logs trong folder `logs/`
3. Sử dụng "System Setup" để tạo database
4. Import sample data để test

**Documentation:** Xem folder `docs/` để biết thêm chi tiết

---

**🎉 Project hoàn thành 100% với tất cả enterprise features!**