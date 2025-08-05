"""
Compliance Checker - Kiểm tra tuân thủ license
"""

import boto3
from datetime import datetime, timedelta
from typing import Dict, List
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.config import *
from license_tracker import LicenseTracker

class ComplianceChecker:
    def __init__(self):
        """Khởi tạo Compliance Checker"""
        self.tracker = LicenseTracker()
    
    def check_compliance_status(self) -> Dict:
        """Kiểm tra trạng thái tuân thủ"""
        licenses = self.tracker.get_all_licenses()
        compliance_report = {
            'total_licenses': len(licenses),
            'compliant': [],
            'warnings': [],
            'violations': [],
            'overall_status': 'COMPLIANT'
        }
        
        for license in licenses:
            license_status = self._check_single_license(license)
            
            if license_status['status'] == 'COMPLIANT':
                compliance_report['compliant'].append(license_status)
            elif license_status['status'] == 'WARNING':
                compliance_report['warnings'].append(license_status)
                if compliance_report['overall_status'] == 'COMPLIANT':
                    compliance_report['overall_status'] = 'WARNING'
            else:  # VIOLATION
                compliance_report['violations'].append(license_status)
                compliance_report['overall_status'] = 'VIOLATION'
        
        return compliance_report
    
    def _check_single_license(self, license: Dict) -> Dict:
        """Kiểm tra một license cụ thể"""
        status = {
            'license_id': license['license_id'],
            'software_name': license['software_name'],
            'status': 'COMPLIANT',
            'issues': []
        }
        
        # Kiểm tra over-usage
        usage_rate = license['used_licenses'] / license['total_licenses']
        
        if usage_rate > 1.0:  # Vượt quá 100%
            status['status'] = 'VIOLATION'
            status['issues'].append(f"Vượt quá license: {license['used_licenses']}/{license['total_licenses']}")
        elif usage_rate > COMPLIANCE_THRESHOLDS['usage_critical']:
            status['status'] = 'WARNING'
            status['issues'].append(f"Sử dụng cao: {usage_rate:.1%}")
        elif usage_rate > COMPLIANCE_THRESHOLDS['usage_warning']:
            if status['status'] == 'COMPLIANT':
                status['status'] = 'WARNING'
            status['issues'].append(f"Cảnh báo sử dụng: {usage_rate:.1%}")
        
        # Kiểm tra expiry date
        if license.get('expiry_date'):
            try:
                expiry = datetime.strptime(license['expiry_date'], '%Y-%m-%d')
                days_until_expiry = (expiry - datetime.now()).days
                
                if days_until_expiry < 0:
                    status['status'] = 'VIOLATION'
                    status['issues'].append(f"License đã hết hạn {abs(days_until_expiry)} ngày - Cần mua license mới")
                elif days_until_expiry <= COMPLIANCE_THRESHOLDS['expiry_warning_days']:
                    if status['status'] == 'COMPLIANT':
                        status['status'] = 'WARNING'
                    status['issues'].append(f"Sắp hết hạn trong {days_until_expiry} ngày")
            except:
                status['issues'].append("Ngày hết hạn không hợp lệ")
        
        return status
    
    def generate_compliance_report(self) -> str:
        """Tạo báo cáo tuân thủ"""
        compliance_data = self.check_compliance_status()
        
        report = []
        report.append("=" * 60)
        report.append("🛡️  BÁO CÁO TUÂN THỦ LICENSE")
        report.append("=" * 60)
        
        # Overall status
        status_emoji = {
            'COMPLIANT': '✅',
            'WARNING': '⚠️',
            'VIOLATION': '🚨'
        }
        
        report.append(f"\n📊 TỔNG QUAN:")
        report.append(f"- Trạng thái tổng thể: {status_emoji[compliance_data['overall_status']]} {compliance_data['overall_status']}")
        report.append(f"- Tổng số license: {compliance_data['total_licenses']}")
        report.append(f"- Tuân thủ: {len(compliance_data['compliant'])}")
        report.append(f"- Cảnh báo: {len(compliance_data['warnings'])}")
        report.append(f"- Vi phạm: {len(compliance_data['violations'])}")
        
        # Violations
        if compliance_data['violations']:
            report.append(f"\n🚨 VI PHẠM NGHIÊM TRỌNG ({len(compliance_data['violations'])}):")
            for violation in compliance_data['violations']:
                report.append(f"- {violation['software_name']}:")
                for issue in violation['issues']:
                    report.append(f"  • {issue}")
                    if "đã hết hạn" in issue:
                        report.append(f"    ➤ Đề xuất: Nên mua license {violation['software_name']} nếu vẫn còn sử dụng")
        
        # Warnings
        if compliance_data['warnings']:
            report.append(f"\n⚠️  CẢNH BÁO ({len(compliance_data['warnings'])}):")
            for warning in compliance_data['warnings']:
                report.append(f"- {warning['software_name']}:")
                for issue in warning['issues']:
                    report.append(f"  • {issue}")
        
        # Compliant
        if compliance_data['compliant']:
            report.append(f"\n✅ TUÂN THỦ TỐT ({len(compliance_data['compliant'])}):")
            for compliant in compliance_data['compliant']:
                report.append(f"- {compliant['software_name']}")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)
    
    def save_compliance_report(self, filename: str = None):
        """Lưu báo cáo tuân thủ"""
        if not filename:
            filename = f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        report = self.generate_compliance_report()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Đã lưu báo cáo: {filename}")
        except Exception as e:
            print(f"❌ Lỗi lưu báo cáo: {e}")
    
    def print_compliance_report(self):
        """In báo cáo tuân thủ"""
        print(self.generate_compliance_report())

def main():
    """Test function"""
    checker = ComplianceChecker()
    checker.print_compliance_report()
    
    # Lưu báo cáo
    checker.save_compliance_report()

if __name__ == "__main__":
    main()