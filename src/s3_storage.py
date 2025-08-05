"""
S3 Storage System for License Optimization
Handles file storage, backup, and data archiving
"""

import boto3
import json
import pandas as pd
from datetime import datetime
from io import StringIO, BytesIO
import logging

class S3StorageManager:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'license-optimization-storage'
        self.logger = logging.getLogger(__name__)
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Create S3 bucket if not exists"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except:
            try:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
                print(f"Created S3 bucket: {self.bucket_name}")
            except Exception as e:
                print(f"Error creating bucket: {e}")
    
    def upload_license_data(self, data, filename=None):
        """Upload license data to S3"""
        if filename is None:
            filename = f"licenses/license_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            json_data = json.dumps(data, indent=2, default=str)
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=json_data,
                ContentType='application/json'
            )
            return f"s3://{self.bucket_name}/{filename}"
        except Exception as e:
            self.logger.error(f"Upload failed: {e}")
            return None
    
    def upload_csv_export(self, df, filename=None):
        """Upload CSV export to S3"""
        if filename is None:
            filename = f"exports/license_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=csv_buffer.getvalue(),
                ContentType='text/csv'
            )
            return f"s3://{self.bucket_name}/{filename}"
        except Exception as e:
            self.logger.error(f"CSV upload failed: {e}")
            return None
    
    def upload_backup(self, backup_data, backup_type='full'):
        """Upload system backup to S3"""
        filename = f"backups/{backup_type}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            backup_json = json.dumps(backup_data, indent=2, default=str)
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=backup_json,
                ContentType='application/json',
                Metadata={
                    'backup_type': backup_type,
                    'created_at': datetime.now().isoformat()
                }
            )
            return f"s3://{self.bucket_name}/{filename}"
        except Exception as e:
            self.logger.error(f"Backup upload failed: {e}")
            return None
    
    def download_file(self, s3_key):
        """Download file from S3"""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
            return response['Body'].read().decode('utf-8')
        except Exception as e:
            self.logger.error(f"Download failed: {e}")
            return None
    
    def list_files(self, prefix=''):
        """List files in S3 bucket"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'modified': obj['LastModified'],
                        'url': f"s3://{self.bucket_name}/{obj['Key']}"
                    })
            return files
        except Exception as e:
            self.logger.error(f"List files failed: {e}")
            return []
    
    def delete_file(self, s3_key):
        """Delete file from S3"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except Exception as e:
            self.logger.error(f"Delete failed: {e}")
            return False
    
    def get_storage_stats(self):
        """Get storage usage statistics"""
        try:
            files = self.list_files()
            total_size = sum(f['size'] for f in files)
            
            stats = {
                'total_files': len(files),
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024*1024), 2),
                'categories': {
                    'licenses': len([f for f in files if f['key'].startswith('licenses/')]),
                    'exports': len([f for f in files if f['key'].startswith('exports/')]),
                    'backups': len([f for f in files if f['key'].startswith('backups/')])
                }
            }
            return stats
        except Exception as e:
            self.logger.error(f"Stats failed: {e}")
            return {}

# Storage utility functions
def create_presigned_url(s3_key, expiration=3600):
    """Create presigned URL for file download"""
    s3_client = boto3.client('s3')
    bucket_name = 'license-optimization-storage'
    
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': s3_key},
            ExpiresIn=expiration
        )
        return url
    except Exception as e:
        print(f"Presigned URL failed: {e}")
        return None

def archive_old_data(days_old=90):
    """Archive data older than specified days"""
    s3_storage = S3StorageManager()
    files = s3_storage.list_files()
    
    archived_count = 0
    cutoff_date = datetime.now().timestamp() - (days_old * 24 * 3600)
    
    for file in files:
        if file['modified'].timestamp() < cutoff_date:
            # Move to archive folder
            old_key = file['key']
            new_key = f"archive/{old_key}"
            
            try:
                # Copy to archive
                s3_storage.s3_client.copy_object(
                    Bucket=s3_storage.bucket_name,
                    CopySource={'Bucket': s3_storage.bucket_name, 'Key': old_key},
                    Key=new_key
                )
                # Delete original
                s3_storage.delete_file(old_key)
                archived_count += 1
            except Exception as e:
                print(f"Archive failed for {old_key}: {e}")
    
    return archived_count