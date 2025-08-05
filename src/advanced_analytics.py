"""
Advanced Analytics Engine for License Optimization
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
from license_tracker import LicenseTracker

class AdvancedAnalytics:
    def __init__(self):
        self.tracker = LicenseTracker()
    
    def generate_executive_summary(self) -> Dict:
        """Tạo báo cáo tổng quan cho leadership"""
        licenses = self.tracker.get_all_licenses()
        if not licenses:
            return {'error': 'No license data available'}
        
        df = pd.DataFrame(licenses)
        df['used_licenses'] = pd.to_numeric(df['used_licenses'])
        df['total_licenses'] = pd.to_numeric(df['total_licenses'])
        df['cost_per_license'] = pd.to_numeric(df['cost_per_license'])
        df['usage_rate'] = df['used_licenses'] / df['total_licenses']
        df['total_cost'] = df['total_licenses'] * df['cost_per_license']
        df['waste_cost'] = (df['total_licenses'] - df['used_licenses']) * df['cost_per_license']
        
        # Calculate key metrics
        total_spend = df['total_cost'].sum()
        total_waste = df['waste_cost'].sum()
        avg_utilization = df['usage_rate'].mean()
        
        # Risk assessment
        high_risk_licenses = len(df[df['usage_rate'] > 0.95])
        underutilized_licenses = len(df[df['usage_rate'] < 0.3])
        
        # Expiry analysis
        expired_count = 0
        expiring_soon_count = 0
        
        for _, license in df.iterrows():
            if license.get('expiry_date'):
                try:
                    expiry = datetime.strptime(license['expiry_date'], '%Y-%m-%d')
                    days_until_expiry = (expiry - datetime.now()).days
                    if days_until_expiry < 0:
                        expired_count += 1
                    elif days_until_expiry <= 30:
                        expiring_soon_count += 1
                except:
                    pass
        
        return {
            'total_licenses': len(licenses),
            'total_annual_spend': total_spend * 12,  # Assuming monthly costs
            'potential_annual_savings': total_waste * 12,
            'average_utilization': f"{avg_utilization:.1%}",
            'efficiency_score': f"{((total_spend - total_waste) / total_spend * 100):.1f}%",
            'high_risk_licenses': high_risk_licenses,
            'underutilized_licenses': underutilized_licenses,
            'expired_licenses': expired_count,
            'expiring_soon': expiring_soon_count,
            'top_cost_drivers': df.nlargest(3, 'total_cost')[['software_name', 'total_cost']].to_dict('records'),
            'biggest_waste_sources': df.nlargest(3, 'waste_cost')[['software_name', 'waste_cost']].to_dict('records')
        }
    
    def calculate_roi_projections(self, optimization_scenarios: List[Dict]) -> Dict:
        """Tính toán ROI cho các kịch bản tối ưu hóa"""
        current_summary = self.generate_executive_summary()
        current_annual_spend = current_summary.get('total_annual_spend', 0)
        
        projections = []
        
        for scenario in optimization_scenarios:
            scenario_name = scenario.get('name', 'Unnamed Scenario')
            expected_savings = scenario.get('expected_savings', 0)
            implementation_cost = scenario.get('implementation_cost', 0)
            
            # Calculate ROI metrics
            annual_savings = expected_savings * 12
            roi_percentage = ((annual_savings - implementation_cost) / implementation_cost * 100) if implementation_cost > 0 else 0
            payback_months = (implementation_cost / expected_savings) if expected_savings > 0 else float('inf')
            
            projections.append({
                'scenario': scenario_name,
                'implementation_cost': implementation_cost,
                'monthly_savings': expected_savings,
                'annual_savings': annual_savings,
                'roi_percentage': f"{roi_percentage:.1f}%",
                'payback_period_months': f"{payback_months:.1f}" if payback_months != float('inf') else "N/A",
                'net_benefit_year_1': annual_savings - implementation_cost
            })
        
        return {
            'current_annual_spend': current_annual_spend,
            'projections': projections,
            'recommended_scenario': max(projections, key=lambda x: x['net_benefit_year_1']) if projections else None
        }
    
    def generate_compliance_risk_score(self) -> Dict:
        """Tính điểm rủi ro tuân thủ"""
        licenses = self.tracker.get_all_licenses()
        if not licenses:
            return {'error': 'No license data available'}
        
        total_score = 0
        risk_factors = []
        
        for license in licenses:
            license_risk = 0
            
            # Usage risk
            usage_rate = float(license['used_licenses']) / float(license['total_licenses'])
            if usage_rate > 1.0:
                license_risk += 40  # Critical over-allocation
                risk_factors.append(f"{license['software_name']}: Over-allocation detected")
            elif usage_rate > 0.95:
                license_risk += 20  # High usage risk
                risk_factors.append(f"{license['software_name']}: High usage risk")
            
            # Expiry risk
            if license.get('expiry_date'):
                try:
                    expiry = datetime.strptime(license['expiry_date'], '%Y-%m-%d')
                    days_until_expiry = (expiry - datetime.now()).days
                    if days_until_expiry < 0:
                        license_risk += 30  # Expired
                        risk_factors.append(f"{license['software_name']}: License expired")
                    elif days_until_expiry <= 7:
                        license_risk += 20  # Expiring very soon
                        risk_factors.append(f"{license['software_name']}: Expiring within 7 days")
                    elif days_until_expiry <= 30:
                        license_risk += 10  # Expiring soon
                        risk_factors.append(f"{license['software_name']}: Expiring within 30 days")
                except:
                    license_risk += 5  # Invalid date format
                    risk_factors.append(f"{license['software_name']}: Invalid expiry date")
            
            total_score += license_risk
        
        # Normalize score (0-100)
        max_possible_score = len(licenses) * 70  # Max risk per license
        normalized_score = min(100, (total_score / max_possible_score * 100)) if max_possible_score > 0 else 0
        
        # Risk level
        if normalized_score >= 70:
            risk_level = 'CRITICAL'
        elif normalized_score >= 40:
            risk_level = 'HIGH'
        elif normalized_score >= 20:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        return {
            'risk_score': f"{normalized_score:.1f}",
            'risk_level': risk_level,
            'total_licenses_evaluated': len(licenses),
            'risk_factors': risk_factors[:10],  # Top 10 risk factors
            'recommendations': self._get_risk_mitigation_recommendations(risk_level, risk_factors)
        }
    
    def _get_risk_mitigation_recommendations(self, risk_level: str, risk_factors: List[str]) -> List[str]:
        """Đề xuất giảm thiểu rủi ro"""
        recommendations = []
        
        if risk_level in ['CRITICAL', 'HIGH']:
            recommendations.append("Immediate action required - Review all high-risk licenses")
            recommendations.append("Implement automated compliance monitoring")
            recommendations.append("Establish emergency license procurement process")
        
        if any('expired' in factor.lower() for factor in risk_factors):
            recommendations.append("Renew expired licenses immediately")
            recommendations.append("Set up expiry alerts 60 days in advance")
        
        if any('over-allocation' in factor.lower() for factor in risk_factors):
            recommendations.append("Audit license usage to prevent over-allocation")
            recommendations.append("Implement usage monitoring tools")
        
        if any('expiring' in factor.lower() for factor in risk_factors):
            recommendations.append("Create renewal calendar for upcoming expirations")
            recommendations.append("Negotiate multi-year contracts for better rates")
        
        return recommendations