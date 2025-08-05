"""
Cấu hình cơ bản cho License Optimization System
"""

# AWS Configuration
AWS_REGION = 'us-east-1'  # Region
DYNAMODB_TABLE_NAME = 'license-tracking'
S3_BUCKET_NAME = 'license-optimization-data'

# License Types
LICENSE_TYPES = {
    'PERPETUAL': 'Vĩnh viễn',
    'SUBSCRIPTION': 'Đăng ký',
    'CONCURRENT': 'Đồng thời',
    'NAMED_USER': 'Người dùng cụ thể'
}

# Compliance Thresholds
COMPLIANCE_THRESHOLDS = {
    'usage_warning': 0.8,  # Cảnh báo khi sử dụng 80%
    'usage_critical': 0.95,  # Nguy hiểm khi sử dụng 95%
    'expiry_warning_days': 30  # Cảnh báo trước 30 ngày hết hạn
}

# Cost Optimization Settings
COST_SETTINGS = {
    'min_usage_for_recommendation': 0.3,  # Tối thiểu 30% sử dụng
    'optimization_check_interval': 7  # Kiểm tra mỗi 7 ngày
}