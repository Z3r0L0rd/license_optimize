"""
Configuration settings for License Optimization System
"""

# AWS Settings
AWS_REGION = 'us-east-1'
DYNAMODB_TABLE_NAME = 'license_optimization_table'
S3_BUCKET_NAME = 'license-optimization-storage'

# Application Settings
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/license_system.log'

# ML Settings
ML_CONFIDENCE_THRESHOLD = 0.7
USAGE_THRESHOLD_LOW = 0.3
USAGE_THRESHOLD_HIGH = 0.9

# Compliance Settings
EXPIRY_WARNING_DAYS = 30
COMPLIANCE_CHECK_INTERVAL = 24  # hours

# Cost optimization settings
COST_SETTINGS = {
    'min_usage_for_recommendation': 0.3,
    'max_usage_threshold': 0.9,
    'cost_per_unused_license': 10.0,
    'savings_threshold': 100.0
}

# Compliance thresholds
COMPLIANCE_THRESHOLDS = {
    'usage_warning': 0.8,
    'usage_critical': 0.95,
    'expiry_warning_days': 30,
    'expiry_critical_days': 7
}