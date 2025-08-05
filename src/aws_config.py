"""
AWS Configuration for Amplify Deployment
Handles AWS credentials and region setup
"""

import os
import boto3

def get_aws_region():
    """Get AWS region from environment or default"""
    return os.environ.get('REGION', 'us-east-1')

def get_boto3_client(service_name):
    """Get boto3 client with proper region"""
    region = get_aws_region()
    
    # Amplify automatically provides AWS credentials via IAM role
    # No need to set AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY
    try:
        client = boto3.client(service_name, region_name=region)
        return client
    except Exception as e:
        print(f"Error creating {service_name} client: {e}")
        return None

def get_boto3_resource(service_name):
    """Get boto3 resource with proper region"""
    region = get_aws_region()
    
    try:
        resource = boto3.resource(service_name, region_name=region)
        return resource
    except Exception as e:
        print(f"Error creating {service_name} resource: {e}")
        return None

def setup_aws_environment():
    """Setup AWS environment for Amplify"""
    # Set AWS region if not already set
    if 'AWS_DEFAULT_REGION' not in os.environ:
        os.environ['AWS_DEFAULT_REGION'] = get_aws_region()
    
    return {
        'region': get_aws_region(),
        'credentials_available': check_aws_credentials()
    }

def check_aws_credentials():
    """Check if AWS credentials are available"""
    try:
        sts = boto3.client('sts')
        sts.get_caller_identity()
        return True
    except Exception:
        return False