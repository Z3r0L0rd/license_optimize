"""
License Tracker - Theo dõi license đơn giản
"""

import boto3
from .aws_config import get_boto3_client
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from decimal import Decimal
import sys
import os
# Simple config without external dependencies
DYNAMODB_TABLE_NAME = 'license_optimization_table'
AWS_REGION = 'us-east-1'

try:
    from .logger import LicenseLogger
except:
    class LicenseLogger:
        def info(self, msg): print(f"INFO: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")

class LicenseTracker:
    def __init__(self):
        """Khởi tạo License Tracker"""
        # Use default boto3 for EC2 deployment
        self.dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        self.table_name = DYNAMODB_TABLE_NAME
        self.logger = LicenseLogger()
        
    def create_table_if_not_exists(self):
        """Tạo bảng DynamoDB nếu chưa tồn tại"""
        try:
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {'AttributeName': 'license_id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'license_id', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST' 
            )
            table.wait_until_exists()
            pass
        except Exception as e:
            if 'ResourceInUseException' in str(e):
                pass
            else:
                pass
    
    def add_license(self, license_data: Dict) -> bool:
        """Thêm license mới"""
        # Auto-create table if not exists
        try:
            self.create_table_if_not_exists()
        except Exception:
            pass
            
        try:
            table = self.dynamodb.Table(self.table_name)
            
            # Chuẩn bị dữ liệu
            item = {
                'license_id': license_data['license_id'],
                'software_name': license_data['software_name'],
                'license_type': license_data['license_type'],
                'total_licenses': int(license_data['total_licenses']),
                'used_licenses': int(license_data.get('used_licenses', 0)),
                'expiry_date': license_data.get('expiry_date', ''),
                'cost_per_license': Decimal(str(license_data.get('cost_per_license', 0))),
                'created_date': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
            
            table.put_item(Item=item)
            self.logger.info(f"Added license: {license_data['software_name']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add license: {e}")
            return False
    
    def get_all_licenses(self) -> List[Dict]:
        """Lấy tất cả license"""
        # Auto-create table if not exists
        try:
            self.create_table_if_not_exists()
        except Exception:
            pass
            
        try:
            table = self.dynamodb.Table(self.table_name)
            response = table.scan()
            return response.get('Items', [])
        except Exception as e:
            return []
    
    def update_usage(self, license_id: str, used_licenses: int) -> bool:
        """Cập nhật số lượng license đang sử dụng"""
        # Auto-create table if not exists
        try:
            self.create_table_if_not_exists()
        except Exception:
            pass
            
        try:
            table = self.dynamodb.Table(self.table_name)
            table.update_item(
                Key={'license_id': license_id},
                UpdateExpression='SET used_licenses = :used, last_updated = :updated',
                ExpressionAttributeValues={
                    ':used': used_licenses,
                    ':updated': datetime.now().isoformat()
                }
            )
            self.logger.info(f"Updated usage for license: {license_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update usage: {e}")
            return False
    
    def delete_license(self, license_id: str) -> bool:
        """Xóa license"""
        # Auto-create table if not exists
        try:
            self.create_table_if_not_exists()
        except Exception:
            pass
            
        try:
            table = self.dynamodb.Table(self.table_name)
            table.delete_item(Key={'license_id': license_id})
            self.logger.info(f"Deleted license: {license_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete license: {e}")
            return False

def main():
    """Hàm chính để test"""
    tracker = LicenseTracker()
    
    # Tạo bảng
    tracker.create_table_if_not_exists()
    
    # Thêm license mẫu
    sample_license = {
        'license_id': 'OFFICE365-001',
        'software_name': 'Microsoft Office 365(Demo)',
        'license_type': 'SUBSCRIPTION',
        'total_licenses': 50,
        'used_licenses': 35,
        'expiry_date': '2024-12-31',
        'cost_per_license': 12.50
    }
    
    tracker.add_license(sample_license)
    
    # Hiển thị tất cả license
    licenses = tracker.get_all_licenses()
    print(f"\nTổng số license: {len(licenses)}")
    for license in licenses:
        usage_percent = (license['used_licenses'] / license['total_licenses']) * 100
        print(f"- {license['software_name']}: {license['used_licenses']}/{license['total_licenses']} ({usage_percent:.1f}%)")

if __name__ == "__main__":
    main()