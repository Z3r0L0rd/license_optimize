#!/bin/bash
# EC2 Deployment Script for License Optimization System

echo "🚀 Starting deployment..."

# Update system
sudo yum update -y

# Install Python 3.9
sudo yum install python3 python3-pip -y

# Install git
sudo yum install git -y

# Clone repository (replace with your repo URL)
cd /home/ec2-user
git clone https://github.com/your-username/license-optimization.git
cd license-optimization

# Install Python dependencies
pip3 install -r requirements.txt

# Configure AWS credentials (EC2 will use IAM role)
export AWS_DEFAULT_REGION=us-east-1

# Install PM2 for process management
sudo npm install -g pm2

# Create PM2 ecosystem file
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'license-optimization',
    script: 'streamlit',
    args: 'run streamlit_app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true',
    interpreter: 'python3',
    env: {
      REGION: 'us-east-1'
    }
  }]
}
EOF

# Start application with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup

echo "✅ Deployment completed!"
echo "🌐 Access app at: http://[EC2-PUBLIC-IP]:8501"