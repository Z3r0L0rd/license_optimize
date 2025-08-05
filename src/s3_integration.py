"""
S3 Integration for License System
Integrates S3 storage with existing modules
"""

from .s3_storage import S3StorageManager
from .license_tracker import LicenseTracker
import pandas as pd
from datetime import datetime
import json

class S3Integration:
    def __init__(self):
        self.s3_storage = S3StorageManager()
        self.license_tracker = LicenseTracker()
    
    def backup_all_licenses(self):
        """Backup all license data to S3"""
        try:
            licenses = self.license_tracker.get_all_licenses()
            backup_data = {
                'backup_date': datetime.now().isoformat(),
                'license_count': len(licenses),
                'licenses': licenses
            }
            
            s3_url = self.s3_storage.upload_backup(backup_data, 'licenses')
            return s3_url
        except Exception as e:
            print(f"Backup failed: {e}")
            return None
    
    def export_licenses_to_s3(self, format='csv'):
        """Export licenses to S3 in specified format"""
        try:
            licenses = self.license_tracker.get_all_licenses()
            
            if format == 'csv':
                df = pd.DataFrame(licenses)
                s3_url = self.s3_storage.upload_csv_export(df)
            else:
                s3_url = self.s3_storage.upload_license_data(licenses)
            
            return s3_url
        except Exception as e:
            print(f"Export failed: {e}")
            return None
    
    def restore_from_backup(self, backup_key):
        """Restore licenses from S3 backup"""
        try:
            backup_data = self.s3_storage.download_file(backup_key)
            if backup_data:
                data = json.loads(backup_data)
                licenses = data.get('licenses', [])
                
                # Restore each license
                restored_count = 0
                for license_data in licenses:
                    try:
                        self.license_tracker.add_license(license_data)
                        restored_count += 1
                    except:
                        continue
                
                return restored_count
            return 0
        except Exception as e:
            print(f"Restore failed: {e}")
            return 0
    
    def sync_with_s3(self):
        """Sync local data with S3"""
        try:
            # Upload current state
            backup_url = self.backup_all_licenses()
            export_url = self.export_licenses_to_s3()
            
            return {
                'backup_url': backup_url,
                'export_url': export_url,
                'sync_time': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Sync failed: {e}")
            return None

def get_s3_dashboard_data():
    """Get S3 storage data for dashboard"""
    s3_storage = S3StorageManager()
    
    try:
        stats = s3_storage.get_storage_stats()
        recent_files = s3_storage.list_files()[-10:]  # Last 10 files
        
        return {
            'storage_stats': stats,
            'recent_files': recent_files,
            'bucket_name': s3_storage.bucket_name
        }
    except Exception as e:
        print(f"Dashboard data failed: {e}")
        return {}