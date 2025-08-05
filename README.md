# 🎯 License Optimization System

Enterprise-grade license management với AWS - Chi phí thấp, hiệu quả cao.

## 🚀 Quick Start (5 phút)

### **Bước 1: Clone repository**
```bash
git clone https://github.com/your-username/license-optimization.git
cd license-optimization
```

### **Bước 2: Setup AWS credentials**
```bash
aws configure
# Nhập AWS Access Key ID và Secret Access Key
```

### **Bước 3: Auto setup**
```bash
chmod +x setup.sh
./setup.sh
```

### **Bước 4: Chạy app**
```bash
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
```

### **Bước 5: Truy cập**
```
http://[EC2-PUBLIC-IP]:8501
```

**Xong! App sẵn sàng sử dụng** 🎉

---

## ✨ Tính năng chính

- ✅ **License Tracking** - CRUD operations với DynamoDB
- ✅ **Usage Analysis** - Phân tích tối ưu hóa chi phí  
- ✅ **ML Recommendations** - AI-powered insights
- ✅ **S3 Storage** - Backup và export tự động
- ✅ **Compliance Monitoring** - Risk assessment
- ✅ **Executive Dashboard** - Báo cáo tổng quan

## 💰 Chi phí

- **Free Tier**: $0/tháng (12 tháng đầu)
- **Sau đó**: ~$5-15/tháng
- **ROI**: Tiết kiệm 20-40% chi phí license

## 🏗️ Kiến trúc

```
Streamlit App → DynamoDB + S3 → CloudWatch
```

## 📊 Tech Stack

- **Backend**: Python 3.9+, AWS SDK (boto3)
- **Frontend**: Streamlit với interactive UI
- **Database**: AWS DynamoDB (NoSQL)
- **Storage**: AWS S3 (backup/export)
- **Monitoring**: AWS CloudWatch

## 🛠️ Requirements

- Python 3.9+
- AWS Account (Free Tier)
- AWS CLI configured
- EC2 instance (t2.micro)

## 📝 Usage

1. **System Setup** - Tạo database tables
2. **License Management** - Thêm/sửa/xóa licenses
3. **Usage Analysis** - Xem báo cáo tối ưu hóa
4. **ML Recommendations** - AI insights
5. **S3 Storage** - Backup và restore
6. **Operations** - Health monitoring

## 🔧 Troubleshooting

### AWS Credentials Error
```bash
aws sts get-caller-identity  # Test connection
aws configure                # Reconfigure if needed
```

### Module Import Error
```bash
./setup.sh                   # Re-run setup script
```

### Port 8501 Access Error
- Check EC2 Security Group allows port 8501
- Use Public IP, not private IP

## 📚 Documentation

- **Technical Documentation**: `TECHNICAL_DOCUMENTATION.md`
- **Project Report**: `PROJECT_REPORT.md`
- **Sample Data**: `sample_licenses.csv`
- **Setup Guide**: This README

---

**🎉 Enterprise-ready license optimization in 5 minutes!**