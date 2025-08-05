# Hướng dẫn cài đặt License Optimization System

## Bước 1: Cài đặt Python và Dependencies

```bash
# Kiểm tra Python (cần Python 3.7+)
python --version

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

## Bước 2: Cấu hình AWS

### 2.1 Tạo AWS Account (Free Tier)
1. Đăng ký tại: https://aws.amazon.com/free/
2. Chọn Free Tier để sử dụng miễn phí 12 tháng

### 2.2 Cài đặt AWS CLI

**Cách 1: MSI Installer (Khuyến nghị)**
1. Tải từ: https://aws.amazon.com/cli/
2. Chạy file .msi và cài đặt
3. AWS CLI sẽ được cài tại: `C:\Program Files\Amazon\AWSCLIV2\`

**Cách 2: Qua pip**
```bash
pip install awscli
```

**Kiểm tra cài đặt:**
```bash
aws --version
```

### 2.3 Cấu hình AWS Credentials
```bash
aws configure
```
Nhập:
- AWS Access Key ID: [Lấy từ AWS Console > IAM]
- AWS Secret Access Key: [Lấy từ AWS Console > IAM]
- Default region: us-east-1
- Default output format: json

## Bước 3: Chạy hệ thống

```bash
# Di chuyển vào thư mục src
cd src

# Chạy hệ thống
python main.py
```

## Bước 4: Sử dụng cơ bản

1. **Thiết lập lần đầu**: Chọn 'y' khi được hỏi
2. **Thêm license**: Sử dụng menu option 2
3. **Xem báo cáo**: Sử dụng menu option 4 và 5
4. **Kiểm tra hàng ngày**: Sử dụng menu option 6

## Chi phí dự kiến (Free Tier)

- **DynamoDB**: 25GB storage miễn phí
- **Lambda**: 1 triệu request miễn phí/tháng
- **S3**: 5GB storage miễn phí
- **CloudWatch**: Monitoring cơ bản miễn phí

**Tổng chi phí**: $0-5/tháng (sau khi hết Free Tier)

## Troubleshooting

### Lỗi AWS Credentials
```bash
# Kiểm tra credentials
aws sts get-caller-identity

# Nếu lỗi, cấu hình lại
aws configure
```

### Lỗi DynamoDB
- Đảm bảo region đúng (us-east-1)
- Kiểm tra IAM permissions
- Thử tạo table thủ công trên AWS Console

### Lỗi Python Dependencies
```bash
# Cài đặt lại
pip install --upgrade -r requirements.txt
```

## Liên hệ hỗ trợ

Nếu gặp vấn đề, hãy:
1. Kiểm tra file log
2. Đọc error message cẩn thận
3. Google error message
4. Hỏi trên AWS forums hoặc Stack Overflow