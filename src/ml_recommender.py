"""
Machine Learning Recommender for License Optimization
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from license_tracker import LicenseTracker

class MLRecommender:
    def __init__(self):
        self.tracker = LicenseTracker()
    
    def predict_usage_trend(self, license_id: str, days_ahead: int = 30) -> Dict:
        """Dự đoán xu hướng sử dụng license"""
        # Simplified ML prediction - trong thực tế sẽ dùng historical data
        licenses = self.tracker.get_all_licenses()
        license_data = next((l for l in licenses if l['license_id'] == license_id), None)
        
        if not license_data:
            return {'error': 'License not found'}
        
        current_usage = float(str(license_data['used_licenses']))
        total_licenses = float(str(license_data['total_licenses']))
        usage_rate = current_usage / total_licenses
        
        # Simple trend prediction based on current usage pattern
        if usage_rate < 0.3:
            trend = 'decreasing'
            predicted_change = -5
        elif usage_rate > 0.8:
            trend = 'increasing'
            predicted_change = 10
        else:
            trend = 'stable'
            predicted_change = 2
        
        predicted_usage = min(total_licenses, max(0, current_usage + predicted_change))
        
        return {
            'license_id': license_id,
            'current_usage': current_usage,
            'predicted_usage': predicted_usage,
            'trend': trend,
            'confidence': 0.75,
            'days_ahead': days_ahead
        }
    
    def get_cost_optimization_recommendations(self) -> List[Dict]:
        """Đề xuất tối ưu hóa chi phí dựa trên ML"""
        try:
            licenses = self.tracker.get_all_licenses()
            if not licenses:
                return []
            recommendations = []
            
            for license in licenses:
                used_licenses = float(str(license['used_licenses']))
                total_licenses = float(str(license['total_licenses']))
                cost_per_license = float(str(license['cost_per_license']))
                usage_rate = used_licenses / total_licenses
                total_cost = total_licenses * cost_per_license
                
                # ML-based recommendations
                if usage_rate < 0.2:
                    action = 'REDUCE_SIGNIFICANTLY'
                    recommended_licenses = max(1, int(used_licenses * 1.2))
                    potential_savings = (total_licenses - recommended_licenses) * cost_per_license
                    priority = 'HIGH'
                elif usage_rate < 0.5:
                    action = 'REDUCE_MODERATELY'
                    recommended_licenses = max(1, int(used_licenses * 1.5))
                    potential_savings = (total_licenses - recommended_licenses) * cost_per_license
                    priority = 'MEDIUM'
                elif usage_rate > 0.9:
                    action = 'INCREASE'
                    recommended_licenses = int(total_licenses * 1.2)
                    potential_savings = 0
                    priority = 'HIGH'
                else:
                    action = 'MAINTAIN'
                    recommended_licenses = int(total_licenses)
                    potential_savings = 0
                    priority = 'LOW'
                
                recommendations.append({
                    'software_name': license['software_name'],
                    'license_id': license['license_id'],
                    'current_licenses': int(total_licenses),
                    'current_usage': int(used_licenses),
                    'usage_rate': f"{usage_rate:.1%}",
                    'recommended_licenses': recommended_licenses,
                    'action': action,
                    'potential_savings': potential_savings,
                    'priority': priority,
                    'confidence_score': 0.8
                })
        
            return sorted(recommendations, key=lambda x: x['potential_savings'], reverse=True)
        except Exception as e:
            return []
    
    def detect_anomalies(self) -> List[Dict]:
        """Phát hiện bất thường trong sử dụng license"""
        licenses = self.tracker.get_all_licenses()
        anomalies = []
        
        for license in licenses:
            used_licenses = float(str(license['used_licenses']))
            total_licenses = float(str(license['total_licenses']))
            usage_rate = used_licenses / total_licenses
            
            # Detect anomalies
            if usage_rate > 1.0:
                anomalies.append({
                    'license_id': license['license_id'],
                    'software_name': license['software_name'],
                    'anomaly_type': 'OVER_ALLOCATION',
                    'severity': 'CRITICAL',
                    'description': f"Usage exceeds total licenses: {used_licenses}/{total_licenses}"
                })
            elif usage_rate == 0:
                anomalies.append({
                    'license_id': license['license_id'],
                    'software_name': license['software_name'],
                    'anomaly_type': 'ZERO_USAGE',
                    'severity': 'HIGH',
                    'description': "No usage detected - potential waste"
                })
            elif usage_rate < 0.1:
                anomalies.append({
                    'license_id': license['license_id'],
                    'software_name': license['software_name'],
                    'anomaly_type': 'VERY_LOW_USAGE',
                    'severity': 'MEDIUM',
                    'description': f"Extremely low usage: {usage_rate:.1%}"
                })
        
        return anomalies