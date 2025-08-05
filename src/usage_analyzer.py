"""
Usage Analyzer - Phân tích sử dụng license
"""

import boto3
from datetime import datetime, timedelta
from typing import Dict, List
from decimal import Decimal
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.config import *
from license_tracker import LicenseTracker

class UsageAnalyzer:
    def __init__(self):
        """Khởi tạo Usage Analyzer"""
        self.tracker = LicenseTracker()
    
    def analyze_usage_patterns(self) -> Dict:
        """Phân tích pattern sử dụng license"""
        licenses = self.tracker.get_all_licenses()
        analysis = {
            'total_licenses': len(licenses),
            'underutilized': [],
            'overutilized': [],
            'expiring_soon': [],
            'expired': [],
            'cost_analysis': {}
        }
        
        total_cost = 0
        total_waste = 0
        
        for license in licenses:
            usage_rate = float(license['used_licenses']) / float(license['total_licenses'])
            cost_per_license = float(license['cost_per_license'])
            total_licenses = float(license['total_licenses'])
            used_licenses = float(license['used_licenses'])
            monthly_cost = cost_per_license * total_licenses
            total_cost += monthly_cost
            
            # Kiểm tra underutilized (dưới 30%)
            if usage_rate < COST_SETTINGS['min_usage_for_recommendation']:
                waste = (total_licenses - used_licenses) * cost_per_license
                total_waste += waste
                analysis['underutilized'].append({
                    'software': license['software_name'],
                    'usage_rate': f"{usage_rate:.1%}",
                    'unused_licenses': int(total_licenses - used_licenses),
                    'potential_savings': waste
                })
            
            # Kiểm tra overutilized (trên 95%)
            if usage_rate > COMPLIANCE_THRESHOLDS['usage_critical']:
                analysis['overutilized'].append({
                    'software': license['software_name'],
                    'usage_rate': f"{usage_rate:.1%}",
                    'risk_level': 'HIGH'
                })
            
            # Kiểm tra expiring soon và expired
            if license.get('expiry_date'):
                try:
                    expiry = datetime.strptime(license['expiry_date'], '%Y-%m-%d')
                    days_until_expiry = (expiry - datetime.now()).days
                    if days_until_expiry < 0:
                        analysis['expired'].append({
                            'software': license['software_name'],
                            'expiry_date': license['expiry_date'],
                            'days_expired': abs(days_until_expiry)
                        })
                    elif days_until_expiry <= COMPLIANCE_THRESHOLDS['expiry_warning_days']:
                        analysis['expiring_soon'].append({
                            'software': license['software_name'],
                            'expiry_date': license['expiry_date'],
                            'days_remaining': days_until_expiry
                        })
                except:
                    pass
        
        analysis['cost_analysis'] = {
            'total_monthly_cost': total_cost,
            'potential_monthly_savings': total_waste,
            'efficiency_rate': f"{((total_cost - total_waste) / total_cost * 100):.1f}%" if total_cost > 0 else "0%"
        }
        
        return analysis
    
    def generate_recommendations(self, analysis: Dict) -> List[str]:
        """Tạo đề xuất tối ưu hóa"""
        recommendations = []
        
        # Đề xuất cho underutilized licenses
        for item in analysis['underutilized']:
            recommendations.append(
                f"🔄 Giảm {item['unused_licenses']} license cho {item['software']} "
                f"để tiết kiệm ${item['potential_savings']:.2f}/tháng"
            )
        
        # Đề xuất cho overutilized licenses
        for item in analysis['overutilized']:
            recommendations.append(
                f"⚠️ Cần mua thêm license cho {item['software']} "
                f"(đang sử dụng {item['usage_rate']})"
            )
        
        # Đề xuất cho expiring licenses (chỉ những license còn hạn)
        for item in analysis['expiring_soon']:
            if item['days_remaining'] > 0:
                recommendations.append(
                    f"📅 Gia hạn {item['software']} trong {item['days_remaining']} ngày"
                )
        
        # Đề xuất cho expired licenses
        for item in analysis['expired']:
            recommendations.append(
                f"🛒 Nên mua license {item['software']} nếu vẫn còn sử dụng"
            )
        
        return recommendations
    
    def print_analysis_report(self):
        """In báo cáo phân tích"""
        print("=" * 60)
        print("📊 BÁO CÁO PHÂN TÍCH LICENSE")
        print("=" * 60)
        
        analysis = self.analyze_usage_patterns()
        
        # Tổng quan
        print(f"\n🔍 TỔNG QUAN:")
        print(f"- Tổng số license: {analysis['total_licenses']}")
        print(f"- Chi phí hàng tháng: ${analysis['cost_analysis']['total_monthly_cost']:.2f}")
        print(f"- Tiềm năng tiết kiệm: ${analysis['cost_analysis']['potential_monthly_savings']:.2f}")
        print(f"- Hiệu suất sử dụng: {analysis['cost_analysis']['efficiency_rate']}")
        
        # Underutilized
        if analysis['underutilized']:
            print(f"\n⚡ LICENSE SỬ DỤNG THẤP ({len(analysis['underutilized'])}):")
            for item in analysis['underutilized']:
                print(f"- {item['software']}: {item['usage_rate']} (tiết kiệm ${item['potential_savings']:.2f})")
        
        # Overutilized
        if analysis['overutilized']:
            print(f"\n🚨 LICENSE SỬ DỤNG CAO ({len(analysis['overutilized'])}):")
            for item in analysis['overutilized']:
                print(f"- {item['software']}: {item['usage_rate']}")
        
        # Expiring
        if analysis['expiring_soon']:
            print(f"\n📅 LICENSE SẮP HẾT HẠN ({len(analysis['expiring_soon'])}):")
            for item in analysis['expiring_soon']:
                print(f"- {item['software']}: {item['days_remaining']} ngày")
        
        # Expired
        if analysis['expired']:
            print(f"\n❌ LICENSE ĐÃ HẾT HẠN ({len(analysis['expired'])}):")
            for item in analysis['expired']:
                print(f"- {item['software']}: hết hạn {item['days_expired']} ngày")
        
        # Recommendations
        recommendations = self.generate_recommendations(analysis)
        if recommendations:
            print(f"\n💡 ĐỀ XUẤT TỐI ƯU HÓA:")
            for rec in recommendations:
                print(f"  {rec}")
        
        print("\n" + "=" * 60)

def main():
    """Test function"""
    analyzer = UsageAnalyzer()
    analyzer.print_analysis_report()

if __name__ == "__main__":
    main()