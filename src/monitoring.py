"""
Real-time Monitoring System
"""

import boto3
import json
from datetime import datetime
from typing import Dict, List
from logger import LicenseLogger

class MonitoringSystem:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
        self.logger = LicenseLogger()
        self.namespace = 'LicenseOptimization'
    
    def send_metric(self, metric_name: str, value: float, unit: str = 'Count'):
        """Send custom metric to CloudWatch"""
        try:
            self.cloudwatch.put_metric_data(
                Namespace=self.namespace,
                MetricData=[
                    {
                        'MetricName': metric_name,
                        'Value': value,
                        'Unit': unit,
                        'Timestamp': datetime.utcnow()
                    }
                ]
            )
        except Exception as e:
            self.logger.error(f"Failed to send metric {metric_name}: {e}")
    
    def create_dashboard(self):
        """Create CloudWatch dashboard"""
        dashboard_body = {
            "widgets": [
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            [self.namespace, "TotalLicenses"],
                            [self.namespace, "ExpiredLicenses"],
                            [self.namespace, "HighRiskLicenses"]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": "us-east-1",
                        "title": "License Overview"
                    }
                }
            ]
        }
        
        try:
            self.cloudwatch.put_dashboard(
                DashboardName='LicenseOptimization',
                DashboardBody=json.dumps(dashboard_body)
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to create dashboard: {e}")
            return False
    
    def create_alarms(self):
        """Create CloudWatch alarms"""
        alarms = [
            {
                'AlarmName': 'HighRiskLicenses',
                'MetricName': 'HighRiskLicenses',
                'Threshold': 5,
                'ComparisonOperator': 'GreaterThanThreshold'
            },
            {
                'AlarmName': 'ExpiredLicenses',
                'MetricName': 'ExpiredLicenses', 
                'Threshold': 0,
                'ComparisonOperator': 'GreaterThanThreshold'
            }
        ]
        
        for alarm in alarms:
            try:
                self.cloudwatch.put_metric_alarm(
                    AlarmName=alarm['AlarmName'],
                    ComparisonOperator=alarm['ComparisonOperator'],
                    EvaluationPeriods=1,
                    MetricName=alarm['MetricName'],
                    Namespace=self.namespace,
                    Period=300,
                    Statistic='Average',
                    Threshold=alarm['Threshold'],
                    ActionsEnabled=True,
                    AlarmDescription=f'Alert for {alarm["AlarmName"]}',
                    Unit='Count'
                )
            except Exception as e:
                self.logger.error(f"Failed to create alarm {alarm['AlarmName']}: {e}")
    
    def health_check(self) -> Dict:
        """System health check"""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'checks': {}
        }
        
        # Database connectivity
        try:
            from license_tracker import LicenseTracker
            tracker = LicenseTracker()
            licenses = tracker.get_all_licenses()
            health_status['checks']['database'] = 'healthy'
            health_status['checks']['license_count'] = len(licenses)
        except Exception as e:
            health_status['status'] = 'unhealthy'
            health_status['checks']['database'] = f'error: {e}'
        
        # Log health status instead of sending metric to avoid circular import
        self.logger.info(f"Health check: {health_status['status']}")
        
        return health_status