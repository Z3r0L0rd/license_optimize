#!/bin/bash
# Auto setup script for License Optimization System

echo "🚀 Setting up License Optimization System..."

# Update system
sudo yum update -y
sudo yum install -y python3 python3-pip git

# Install Python dependencies
pip3 install -r requirements.txt

# Create config directory and files
mkdir -p config logs
touch config/__init__.py
touch src/__init__.py

# Create config.py automatically
cat > config/config.py << 'EOF'
AWS_REGION = 'us-east-1'
DYNAMODB_TABLE_NAME = 'license_optimization_table'
S3_BUCKET_NAME = 'license-optimization-storage'

COST_SETTINGS = {
    'min_usage_for_recommendation': 0.3,
    'max_usage_threshold': 0.9,
    'cost_per_unused_license': 10.0,
    'savings_threshold': 100.0
}

COMPLIANCE_THRESHOLDS = {
    'usage_warning': 0.8,
    'usage_critical': 0.95,
    'expiry_warning_days': 30,
    'expiry_critical_days': 7
}
EOF

# Setup AWS credentials (if not exists)
if [ ! -f ~/.aws/credentials ]; then
    echo "⚠️  AWS credentials not found. Please run: aws configure"
fi

# Create DynamoDB table
echo "📊 Creating DynamoDB table..."
aws dynamodb create-table \
    --table-name license_optimization_table \
    --attribute-definitions AttributeName=license_id,AttributeType=S \
    --key-schema AttributeName=license_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1 2>/dev/null || echo "Table already exists"

echo "✅ Setup completed!"
echo "🌐 Run app: streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true"