"""
License Optimization System - Main Application
Hệ thống tối ưu hóa license chính
"""

import sys
import os
from datetime import datetime

# Thêm path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from license_tracker import LicenseTracker
from usage_analyzer import UsageAnalyzer
from compliance_checker import ComplianceChecker

class LicenseOptimizationSystem:
    def __init__(self):
        """Khởi tạo hệ thống"""
        self.tracker = LicenseTracker()
        self.analyzer = UsageAnalyzer()
        self.compliance = ComplianceChecker()
        
    def setup_system(self):
        """Thiết lập hệ thống lần đầu"""
        print("🚀 THIẾT LẬP HỆ THỐNG LICENSE OPTIMIZATION!!")
        print("=" * 50)
        
        # Tạo bảng DynamoDB
        print("1. Tạo cơ sở dữ liệu...")
        self.tracker.create_table_if_not_exists()
        
        # Thêm dữ liệu mẫu
        print("2. Thêm dữ liệu mẫu...")
        sample_licenses = [
            {
                'license_id': 'exOFFICE365-001',
                'software_name': 'exMicrosoft Office 365',
                'license_type': 'SUBSCRIPTION',
                'total_licenses': 50,
                'used_licenses': 35,
                'expiry_date': '2024-12-31',
                'cost_per_license': 12.50
            },
            {
                'license_id': 'exADOBE-CC-001',
                'software_name': 'exAdobe Creative Cloud',
                'license_type': 'SUBSCRIPTION',
                'total_licenses': 20,
                'used_licenses': 8,
                'expiry_date': '2024-11-15',
                'cost_per_license': 52.99
            },
            {
                'license_id': 'exWINDOWS-001',
                'software_name': 'exWindows 11 Pro',
                'license_type': 'PERPETUAL',
                'total_licenses': 1,
                'used_licenses': 1,
                'expiry_date': '',
                'cost_per_license': 199.99
            }
        ]
        
        for license_data in sample_licenses:
            self.tracker.add_license(license_data)
        
        print("✅ Thiết lập hoàn tất!")
    
    def run_daily_check(self):
        """Chạy kiểm tra hàng ngày"""
        print("📅 KIỂM TRA HÀNG NGÀY")
        print("=" * 50)
        
        # Kiểm tra compliance
        print("1. Kiểm tra tuân thủ...")
        self.compliance.print_compliance_report()
        
        # Phân tích usage
        print("\n2. Phân tích sử dụng...")
        self.analyzer.print_analysis_report()
        
        # Lưu báo cáo
        print("\n3. Lưu báo cáo...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        report_path = os.path.join(reports_dir, f"compliance_{timestamp}.txt")
        self.compliance.save_compliance_report(report_path)
        
    def interactive_menu(self):
        """Menu tương tác"""
        while True:
            print("\n" + "=" * 50)
            print("🎯 LICENSE OPTIMIZATION SYSTEM")
            print("=" * 50)
            print("1. Xem tất cả license")
            print("2. Thêm license mới")
            print("3. Cập nhật usage")
            print("4. Kiểm tra tuân thủ")
            print("5. Phân tích và đề xuất")
            print("6. Chạy kiểm tra hàng ngày")
            print("7. Thiết lập hệ thống")
            print("0. Thoát")
            print("-" * 50)
            
            choice = input("Chọn chức năng (0-7): ").strip()
            
            if choice == '0':
                print("👋 Tạm biệt!")
                break
            elif choice == '1':
                self._show_all_licenses()
            elif choice == '2':
                self._add_new_license()
            elif choice == '3':
                self._update_usage()
            elif choice == '4':
                self.compliance.print_compliance_report()
            elif choice == '5':
                self.analyzer.print_analysis_report()
            elif choice == '6':
                self.run_daily_check()
            elif choice == '7':
                self.setup_system()
            else:
                print("❌ Lựa chọn không hợp lệ!")
    
    def _show_all_licenses(self):
        """Hiển thị tất cả license"""
        licenses = self.tracker.get_all_licenses()
        if not licenses:
            print("📭 Chưa có license nào!")
            return
        
        print(f"\n📊 DANH SÁCH LICENSE ({len(licenses)}):")
        print("-" * 80)
        for license in licenses:
            usage_rate = (license['used_licenses'] / license['total_licenses']) * 100
            status = "🟢" if usage_rate < 80 else "🟡" if usage_rate < 95 else "🔴"
            print(f"{status} {license['software_name']}")
            print(f"   ID: {license['license_id']}")
            print(f"   Sử dụng: {license['used_licenses']}/{license['total_licenses']} ({usage_rate:.1f}%)")
            print(f"   Chi phí: ${float(license['cost_per_license'])}/license")
            if license.get('expiry_date'):
                print(f"   Hết hạn: {license['expiry_date']}")
            print()
    
    def _add_new_license(self):
        """Thêm license mới"""
        print("\n➕ THÊM LICENSE MỚI:")
        try:
            license_data = {
                'license_id': input("License ID: ").strip(),
                'software_name': input("Tên phần mềm: ").strip(),
                'license_type': input("Loại license (SUBSCRIPTION/PERPETUAL/CONCURRENT/NAMED_USER): ").strip().upper(),
                'total_licenses': int(input("Tổng số license: ")),
                'used_licenses': int(input("Số license đang dùng: ")),
                'expiry_date': input("Ngày hết hạn (YYYY-MM-DD, để trống nếu vĩnh viễn): ").strip(),
                'cost_per_license': float(input("Chi phí mỗi license ($): "))
            }
            
            if self.tracker.add_license(license_data):
                print("✅ Thêm license thành công!")
            else:
                print("❌ Thêm license thất bại!")
                
        except ValueError:
            print("❌ Dữ liệu nhập không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    
    def _update_usage(self):
        """Cập nhật usage"""
        print("\n🔄 CẬP NHẬT USAGE:")
        try:
            license_id = input("License ID: ").strip()
            used_licenses = int(input("Số license đang sử dụng: "))
            
            if self.tracker.update_usage(license_id, used_licenses):
                print("✅ Cập nhật thành công!")
            else:
                print("❌ Cập nhật thất bại!")
                
        except ValueError:
            print("❌ Số lượng không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")

def main():
    """Hàm chính"""
    system = LicenseOptimizationSystem()
    
    print("🎯 Chào mừng đến với License Optimization System!")
    print("Hệ thống tối ưu hóa license với chi phí thấp sử dụng AWS")
    
    # Kiểm tra xem có muốn thiết lập hệ thống không
    setup = input("\nBạn có muốn thiết lập hệ thống lần đầu? (y/n): ").lower()
    if setup == 'y':
        system.setup_system()
    
    # Chạy menu tương tác
    system.interactive_menu()

if __name__ == "__main__":
    main()