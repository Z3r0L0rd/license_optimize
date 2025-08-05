"""
Operational Procedures and Automation
"""

import os
import json
import shutil
from datetime import datetime, timedelta
from typing import Dict, List
from logger import LicenseLogger

class OperationsManager:
    def __init__(self):
        self.logger = LicenseLogger()
        self.backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def daily_operations(self) -> Dict:
        """Run daily operational tasks"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'tasks': {}
        }
        
        # 1. Health check
        results['tasks']['health_check'] = self.health_check()
        
        # 2. Backup data
        results['tasks']['backup'] = self.backup_data()
        
        # 3. Clean old logs
        results['tasks']['log_cleanup'] = self.cleanup_old_logs()
        
        # 4. Generate daily report
        results['tasks']['daily_report'] = self.generate_daily_report()
        
        # 5. Send metrics
        results['tasks']['metrics'] = self.send_daily_metrics()
        
        self.logger.info(f"Daily operations completed: {results}")
        return results
    
    def health_check(self) -> Dict:
        """System health check"""
        try:
            from license_tracker import LicenseTracker
            
            tracker = LicenseTracker()
            
            # Test database connection
            licenses = tracker.get_all_licenses()
            
            return {
                'status': 'success',
                'license_count': len(licenses),
                'system_health': 'healthy'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def backup_data(self) -> Dict:
        """Backup system data"""
        try:
            from bulk_importer import BulkImporter
            
            importer = BulkImporter()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(self.backup_dir, f'licenses_backup_{timestamp}.csv')
            
            if importer.export_to_csv(backup_file):
                return {'status': 'success', 'backup_file': backup_file}
            else:
                return {'status': 'error', 'message': 'Export failed'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def cleanup_old_logs(self, days_to_keep: int = 30) -> Dict:
        """Clean up old log files"""
        try:
            logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
            if not os.path.exists(logs_dir):
                return {'status': 'success', 'message': 'No logs directory'}
            
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            cleaned_files = []
            
            for filename in os.listdir(logs_dir):
                file_path = os.path.join(logs_dir, filename)
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_time < cutoff_date:
                        os.remove(file_path)
                        cleaned_files.append(filename)
            
            return {
                'status': 'success',
                'cleaned_files': len(cleaned_files),
                'files': cleaned_files
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def generate_daily_report(self) -> Dict:
        """Generate daily operational report"""
        try:
            from usage_analyzer import UsageAnalyzer
            from compliance_checker import ComplianceChecker
            
            analyzer = UsageAnalyzer()
            compliance = ComplianceChecker()
            
            # Get analysis
            analysis = analyzer.analyze_usage_patterns()
            compliance_data = compliance.check_compliance_status()
            
            # Create report
            report = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'summary': {
                    'total_licenses': analysis['total_licenses'],
                    'underutilized': len(analysis['underutilized']),
                    'overutilized': len(analysis['overutilized']),
                    'expired': len(analysis.get('expired', [])),
                    'compliance_status': compliance_data['overall_status']
                }
            }
            
            # Save report
            reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
            os.makedirs(reports_dir, exist_ok=True)
            
            report_file = os.path.join(reports_dir, f"daily_report_{datetime.now().strftime('%Y%m%d')}.json")
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            return {'status': 'success', 'report_file': report_file}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def send_daily_metrics(self) -> Dict:
        """Send daily metrics to monitoring"""
        try:
            from usage_analyzer import UsageAnalyzer
            
            analyzer = UsageAnalyzer()
            analysis = analyzer.analyze_usage_patterns()
            
            # Log metrics instead of sending to CloudWatch
            self.logger.info(f"Daily metrics - Total: {analysis['total_licenses']}, Underutilized: {len(analysis['underutilized'])}")
            
            return {'status': 'success', 'metrics_logged': 4}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def disaster_recovery(self, backup_file: str) -> Dict:
        """Restore from backup"""
        try:
            from bulk_importer import BulkImporter
            
            if not os.path.exists(backup_file):
                return {'status': 'error', 'message': 'Backup file not found'}
            
            importer = BulkImporter()
            results = importer.import_from_csv(backup_file)
            
            return {
                'status': 'success',
                'restored_licenses': results['success'],
                'errors': len(results['errors'])
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}