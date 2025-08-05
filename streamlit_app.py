"""
Streamlit Web App for License Optimization System
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.license_tracker import LicenseTracker
from src.usage_analyzer import UsageAnalyzer
from src.compliance_checker import ComplianceChecker
from src.bulk_importer import BulkImporter
from src.data_validator import LicenseValidator
from src.logger import LicenseLogger
from src.ml_recommender import MLRecommender
from src.advanced_analytics import AdvancedAnalytics
from src.monitoring import MonitoringSystem
from src.operations import OperationsManager
from src.audit_system import AuditSystem
from src.s3_integration import S3Integration, get_s3_dashboard_data

st.set_page_config(
    page_title="License Optimization System",
    page_icon="🎯",
    layout="wide"
)

@st.cache_resource
def init_system():
    tracker = LicenseTracker()
    try:
        tracker.create_table_if_not_exists()
    except Exception as e:
        st.error(f"Database setup failed: {e}")
    
    return {
        'tracker': tracker,
        'analyzer': UsageAnalyzer(),
        'compliance': ComplianceChecker(),
        'importer': BulkImporter(),
        'validator': LicenseValidator(),
        'logger': LicenseLogger(),
        'ml_recommender': MLRecommender(),
        'advanced_analytics': AdvancedAnalytics(),
        'monitoring': MonitoringSystem(),
        'operations': OperationsManager(),
        'audit': AuditSystem(),
        's3_integration': S3Integration()
    }

def main():
    system = init_system()
    
    st.title("🎯 License Optimization System")
    st.markdown("**Hệ thống tối ưu hóa license với AWS**")
    
    # Sidebar with search
    st.sidebar.title("📋 Navigation")
    search_term = st.sidebar.text_input("🔍 Search:", placeholder="Type to search...")
    
    # Menu items
    menu_items = {
        "📊 Dashboard": "Dashboard",
        "📝 License Management": "License Management", 
        "📈 Usage Analysis": "Usage Analysis",
        "🛡️ Compliance Check": "Compliance Check",
        "🤖 ML Recommendations": "ML Recommendations",
        "📋 Executive Summary": "Executive Summary",
        "⚠️ Risk Assessment": "Risk Assessment",
        "⚙️ Operations": "Operations",
        "📄 Audit Reports": "Audit Reports",
        "💾 Data Management": "Data Management",
        "☁️ S3 Storage": "S3 Storage",
        "🔧 System Setup": "System Setup",
        "📋 View Logs": "View Logs"
    }
    
    # Filter by search
    if search_term:
        filtered_items = {k: v for k, v in menu_items.items() 
                         if search_term.lower() in k.lower() or search_term.lower() in v.lower()}
    else:
        filtered_items = menu_items
    
    # Session state
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Dashboard"
    
    # Menu buttons
    st.sidebar.markdown("---")
    
    for display_name, page_name in filtered_items.items():
        button_type = "primary" if st.session_state.selected_page == page_name else "secondary"
        if st.sidebar.button(display_name, key=f"btn_{page_name}", use_container_width=True, type=button_type):
            st.session_state.selected_page = page_name
            st.rerun()
    
    # Route pages
    page = st.session_state.selected_page
    
    if page == "Dashboard":
        show_dashboard(system)
    elif page == "License Management":
        show_license_management(system)
    elif page == "Usage Analysis":
        show_usage_analysis(system)
    elif page == "Compliance Check":
        show_compliance_check(system)
    elif page == "ML Recommendations":
        show_ml_recommendations(system)
    elif page == "Executive Summary":
        show_executive_summary(system)
    elif page == "Risk Assessment":
        show_risk_assessment(system)
    elif page == "Operations":
        show_operations(system)
    elif page == "Audit Reports":
        show_audit_reports(system)
    elif page == "Data Management":
        show_data_management(system)
    elif page == "S3 Storage":
        show_s3_storage(system)
    elif page == "System Setup":
        show_system_setup(system)
    elif page == "View Logs":
        show_logs()
    else:
        st.info(f"Page '{page}' is under development")

def show_dashboard(system):
    st.header("📊 Dashboard")
    
    licenses = system['tracker'].get_all_licenses()
    if not licenses:
        st.warning("Chưa có dữ liệu license. Vui lòng thêm license hoặc import dữ liệu.")
        return
    
    df = pd.DataFrame(licenses)
    df['used_licenses'] = pd.to_numeric(df['used_licenses'])
    df['total_licenses'] = pd.to_numeric(df['total_licenses'])
    df['cost_per_license'] = pd.to_numeric(df['cost_per_license'])
    df['usage_rate'] = (df['used_licenses'] / df['total_licenses'] * 100).round(1)
    df['total_cost'] = df['total_licenses'] * df['cost_per_license']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tổng License", len(licenses))
    with col2:
        st.metric("Tổng Chi Phí", f"${df['total_cost'].sum():,.2f}")
    with col3:
        avg_usage = df['usage_rate'].mean()
        st.metric("Usage Trung Bình", f"{avg_usage:.1f}%")
    with col4:
        expired_count = sum(1 for l in licenses if l.get('expiry_date') and 
                          datetime.strptime(l['expiry_date'], '%Y-%m-%d') < datetime.now())
        st.metric("License Hết Hạn", expired_count)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Usage Rate Distribution")
        fig = px.bar(df, x='software_name', y='usage_rate', 
                    color='usage_rate', color_continuous_scale='RdYlGn')
        fig.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Cost by Software")
        fig = px.pie(df, values='total_cost', names='software_name')
        st.plotly_chart(fig, use_container_width=True)

def show_license_management(system):
    st.header("📝 License Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["View Licenses", "Add License", "Update Usage", "Delete License"])
    
    with tab1:
        licenses = system['tracker'].get_all_licenses()
        if licenses:
            df = pd.DataFrame(licenses)
            df['used_licenses'] = pd.to_numeric(df['used_licenses'])
            df['total_licenses'] = pd.to_numeric(df['total_licenses'])
            df['cost_per_license'] = pd.to_numeric(df['cost_per_license'])
            df['usage_rate'] = (df['used_licenses'] / df['total_licenses'] * 100).round(1)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Chưa có license nào.")
    
    with tab2:
        st.subheader("Thêm License Mới")
        with st.form("add_license"):
            col1, col2 = st.columns(2)
            with col1:
                license_id = st.text_input("License ID*")
                software_name = st.text_input("Tên Phần Mềm*")
                license_type = st.selectbox("Loại License*", 
                    ["SUBSCRIPTION", "PERPETUAL", "CONCURRENT"])
            with col2:
                total_licenses = st.number_input("Tổng Số License*", min_value=1, value=1)
                used_licenses = st.number_input("Số License Đang Dùng", min_value=0, value=0)
                cost_per_license = st.number_input("Chi Phí/License ($)*", min_value=0.0, value=0.0)
            
            expiry_date = st.date_input("Ngày Hết Hạn (tùy chọn)", value=None)
            
            if st.form_submit_button("Thêm License"):
                license_data = {
                    'license_id': license_id,
                    'software_name': software_name,
                    'license_type': license_type,
                    'total_licenses': total_licenses,
                    'used_licenses': used_licenses,
                    'expiry_date': expiry_date.strftime('%Y-%m-%d') if expiry_date else '',
                    'cost_per_license': cost_per_license
                }
                
                errors = system['validator'].validate_license_data(license_data)
                if errors:
                    st.error(f"Lỗi validation: {', '.join(errors)}")
                else:
                    if system['tracker'].add_license(license_data):
                        st.success("Thêm license thành công!")
                        st.rerun()
                    else:
                        st.error("Thêm license thất bại!")
    
    with tab3:
        st.subheader("Cập Nhật Usage")
        licenses = system['tracker'].get_all_licenses()
        if licenses:
            license_options = {f"{l['software_name']} ({l['license_id']})": l['license_id'] 
                             for l in licenses}
            selected = st.selectbox("Chọn License:", list(license_options.keys()))
            
            if selected:
                license_id = license_options[selected]
                current_license = next(l for l in licenses if l['license_id'] == license_id)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"Hiện tại: {current_license['used_licenses']}/{current_license['total_licenses']}")
                with col2:
                    new_usage = st.number_input("Usage Mới:", 
                        min_value=0, max_value=int(current_license['total_licenses']),
                        value=int(current_license['used_licenses']))
                
                if st.button("Cập Nhật"):
                    if system['tracker'].update_usage(license_id, new_usage):
                        st.success("Cập nhật thành công!")
                        st.rerun()
                    else:
                        st.error("Cập nhật thất bại!")
    
    with tab4:
        st.subheader("Xóa License")
        licenses = system['tracker'].get_all_licenses()
        if licenses:
            license_options = {f"{l['software_name']} ({l['license_id']})": l['license_id'] 
                             for l in licenses}
            selected = st.selectbox("Chọn License cần xóa:", list(license_options.keys()))
            
            if selected:
                license_id = license_options[selected]
                current_license = next(l for l in licenses if l['license_id'] == license_id)
                
                st.warning(f"⚠️ Bạn sắp xóa: **{current_license['software_name']}**")
                st.info(f"License ID: {license_id}")
                
                if st.button("❌ Xóa License", type="primary"):
                    if system['tracker'].delete_license(license_id):
                        st.success("Xóa thành công!")
                        st.rerun()
                    else:
                        st.error("Xóa thất bại!")
        else:
            st.info("Không có license nào để xóa.")

def show_data_management(system):
    st.header("💾 Data Management")
    
    tab1, tab2 = st.tabs(["Import CSV", "Export CSV"])
    
    with tab1:
        st.subheader("Import Licenses từ CSV")
        uploaded_file = st.file_uploader("Chọn CSV file", type=['csv'])
        if uploaded_file:
            if st.button("Import"):
                temp_path = f"temp_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                with open(temp_path, 'wb') as f:
                    f.write(uploaded_file.getvalue())
                
                results = system['importer'].import_from_csv(temp_path)
                os.remove(temp_path)
                
                st.success(f"Import thành công: {results['success']} licenses")
                if results['errors']:
                    for error in results['errors']:
                        st.error(f"• {error}")
    
    with tab2:
        st.subheader("Export Licenses ra CSV")
        if st.button("Export"):
            export_path = f"licenses_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            if system['importer'].export_to_csv(export_path):
                with open(export_path, 'rb') as f:
                    st.download_button("Download CSV", f.read(), export_path)

def show_s3_storage(system):
    st.header("☁️ S3 Storage Management")
    
    # S3 Dashboard
    s3_data = get_s3_dashboard_data()
    
    if s3_data:
        st.subheader("📊 Storage Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Files", s3_data['storage_stats'].get('total_files', 0))
        with col2:
            st.metric("Storage Used", f"{s3_data['storage_stats'].get('total_size_mb', 0)} MB")
        with col3:
            st.metric("Bucket Name", s3_data.get('bucket_name', 'N/A'))
        with col4:
            st.metric("Categories", len(s3_data['storage_stats'].get('categories', {})))
    
    # S3 Operations
    st.subheader("🚀 S3 Operations")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Backup to S3", "Export to S3", "File Browser", "Sync Operations"])
    
    with tab1:
        st.write("**Backup License Data to S3**")
        if st.button("Create S3 Backup"):
            with st.spinner("Creating backup..."):
                backup_url = system['s3_integration'].backup_all_licenses()
                if backup_url:
                    st.success(f"Backup created successfully!")
                    st.info(f"S3 URL: {backup_url}")
                else:
                    st.error("Backup failed!")
    
    with tab2:
        st.write("**Export Data to S3**")
        export_format = st.selectbox("Export Format:", ["csv", "json"])
        
        if st.button("Export to S3"):
            with st.spinner("Exporting to S3..."):
                export_url = system['s3_integration'].export_licenses_to_s3(export_format)
                if export_url:
                    st.success(f"Export completed!")
                    st.info(f"S3 URL: {export_url}")
                else:
                    st.error("Export failed!")
    
    with tab3:
        st.write("**S3 File Browser**")
        
        # List files by category
        category = st.selectbox("Browse Category:", ["All Files", "licenses", "exports", "backups", "archive"])
        prefix = "" if category == "All Files" else f"{category}/"
        
        if st.button("Refresh File List"):
            files = system['s3_integration'].s3_storage.list_files(prefix)
            
            if files:
                st.write(f"Found {len(files)} files:")
                
                for file in files[-20:]:  # Show last 20 files
                    col1, col2, col3, col4 = st.columns([3, 1, 2, 1])
                    
                    with col1:
                        st.write(file['key'])
                    with col2:
                        st.write(f"{file['size']} bytes")
                    with col3:
                        st.write(file['modified'].strftime('%Y-%m-%d %H:%M'))
                    with col4:
                        if st.button("Delete", key=f"del_{file['key']}"):
                            if system['s3_integration'].s3_storage.delete_file(file['key']):
                                st.success("Deleted!")
                                st.rerun()
                            else:
                                st.error("Delete failed!")
            else:
                st.info("No files found in this category.")
    
    with tab4:
        st.write("**Sync Operations**")
        
        if st.button("Full Sync with S3"):
            with st.spinner("Syncing with S3..."):
                sync_result = system['s3_integration'].sync_with_s3()
                
                if sync_result:
                    st.success("Sync completed!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if sync_result['backup_url']:
                            st.info(f"Backup: {sync_result['backup_url']}")
                    with col2:
                        if sync_result['export_url']:
                            st.info(f"Export: {sync_result['export_url']}")
                    
                    st.write(f"Sync time: {sync_result['sync_time']}")
                else:
                    st.error("Sync failed!")
        
        st.markdown("---")
        st.write("**Restore from S3 Backup**")
        
        backup_key = st.text_input("Backup S3 Key (e.g., backups/licenses_backup_20241201_120000.json):")
        
        if st.button("Restore from Backup") and backup_key:
            with st.spinner("Restoring from backup..."):
                restored_count = system['s3_integration'].restore_from_backup(backup_key)
                
                if restored_count > 0:
                    st.success(f"Restored {restored_count} licenses from backup!")
                else:
                    st.error("Restore failed or no data found!")

def show_system_setup(system):
    st.header("🔧 System Setup")
    
    if st.button("Tạo Database Table"):
        system['tracker'].create_table_if_not_exists()
        st.success("Database setup completed!")
    
    if st.button("Thêm Dữ Liệu Mẫu"):
        sample_licenses = [
            {
                'license_id': 'OFFICE365-DEMO',
                'software_name': 'Microsoft Office 365 (Demo)',
                'license_type': 'SUBSCRIPTION',
                'total_licenses': 50,
                'used_licenses': 35,
                'expiry_date': '2024-12-31',
                'cost_per_license': 12.50
            }
        ]
        
        for license_data in sample_licenses:
            system['tracker'].add_license(license_data)
        
        st.success("Đã thêm dữ liệu mẫu!")

def show_usage_analysis(system):
    st.header("📈 Usage Analysis")
    
    analysis = system['analyzer'].analyze_usage_patterns()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Underutilized", len(analysis['underutilized']))
    with col2:
        st.metric("Overutilized", len(analysis['overutilized']))
    with col3:
        st.metric("Expiring Soon", len(analysis['expiring_soon']))
    
    if analysis['underutilized']:
        st.subheader("⚡ License Sử Dụng Thấp")
        for item in analysis['underutilized']:
            st.warning(f"**{item['software']}**: {item['usage_rate']} - Tiết kiệm ${item['potential_savings']:.2f}")
    
    if analysis['overutilized']:
        st.subheader("🚨 License Sử Dụng Cao")
        for item in analysis['overutilized']:
            st.error(f"**{item['software']}**: {item['usage_rate']}")
    
    if analysis['expired']:
        st.subheader("❌ License Đã Hết Hạn")
        for item in analysis['expired']:
            st.error(f"**{item['software']}**: Hết hạn {item['days_expired']} ngày")

def show_compliance_check(system):
    st.header("🛡️ Compliance Check")
    
    compliance_data = system['compliance'].check_compliance_status()
    
    status_color = {"COMPLIANT": "green", "WARNING": "orange", "VIOLATION": "red"}
    st.markdown(f"**Trạng thái tổng thể:** :{status_color[compliance_data['overall_status']]}[{compliance_data['overall_status']}]")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tuân Thủ", len(compliance_data['compliant']))
    with col2:
        st.metric("Cảnh Báo", len(compliance_data['warnings']))
    with col3:
        st.metric("Vi Phạm", len(compliance_data['violations']))
    
    if compliance_data['violations']:
        st.subheader("🚨 Vi Phạm Nghiêm Trọng")
        for violation in compliance_data['violations']:
            with st.expander(f"❌ {violation['software_name']}"):
                for issue in violation['issues']:
                    st.write(f"• {issue}")

def show_ml_recommendations(system):
    st.header("🤖 ML Recommendations")
    
    tab1, tab2, tab3 = st.tabs(["Cost Optimization", "Usage Prediction", "Anomaly Detection"])
    
    with tab1:
        st.subheader("Cost Optimization Recommendations")
        recommendations = system['ml_recommender'].get_cost_optimization_recommendations()
        
        if recommendations:
            for rec in recommendations:
                with st.expander(f"{rec['software_name']} - {rec['action']} (Priority: {rec['priority']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Current Licenses", rec['current_licenses'])
                        st.metric("Current Usage", rec['current_usage'])
                        st.metric("Usage Rate", rec['usage_rate'])
                    with col2:
                        st.metric("Recommended Licenses", rec['recommended_licenses'])
                        st.metric("Potential Savings", f"${rec['potential_savings']:.2f}")
                        st.metric("Confidence", f"{rec['confidence_score']:.1%}")
        else:
            st.info("No recommendations available")
    
    with tab2:
        st.subheader("Usage Trend Prediction")
        licenses = system['tracker'].get_all_licenses()
        if licenses:
            license_options = {f"{l['software_name']} ({l['license_id']})": l['license_id'] for l in licenses}
            selected = st.selectbox("Select License for Prediction:", list(license_options.keys()))
            
            if selected:
                license_id = license_options[selected]
                days_ahead = st.slider("Prediction Days Ahead:", 7, 90, 30)
                
                if st.button("Generate Prediction"):
                    prediction = system['ml_recommender'].predict_usage_trend(license_id, days_ahead)
                    
                    if 'error' not in prediction:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Current Usage", int(prediction['current_usage']))
                        with col2:
                            st.metric("Predicted Usage", int(prediction['predicted_usage']))
                        with col3:
                            st.metric("Trend", prediction['trend'].title())
                        
                        st.info(f"Confidence: {prediction['confidence']:.1%}")
    
    with tab3:
        st.subheader("Anomaly Detection")
        anomalies = system['ml_recommender'].detect_anomalies()
        
        if anomalies:
            for anomaly in anomalies:
                st.error(f"**{anomaly['software_name']}** - {anomaly['anomaly_type']} ({anomaly['severity']})")
                st.write(f"Description: {anomaly['description']}")
        else:
            st.success("No anomalies detected")

def show_executive_summary(system):
    st.header("📋 Executive Summary")
    
    summary = system['advanced_analytics'].generate_executive_summary()
    
    if 'error' not in summary:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Licenses", summary['total_licenses'])
        with col2:
            st.metric("Annual Spend", f"${summary['total_annual_spend']:,.0f}")
        with col3:
            st.metric("Potential Savings", f"${summary['potential_annual_savings']:,.0f}")
        with col4:
            st.metric("Efficiency Score", summary['efficiency_score'])
        
        st.subheader("Risk Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("High Risk Licenses", summary['high_risk_licenses'])
        with col2:
            st.metric("Underutilized", summary['underutilized_licenses'])
        with col3:
            st.metric("Expired", summary['expired_licenses'])
        with col4:
            st.metric("Expiring Soon", summary['expiring_soon'])
    else:
        st.error(summary['error'])

def show_risk_assessment(system):
    st.header("⚠️ Risk Assessment")
    
    risk_data = system['advanced_analytics'].generate_compliance_risk_score()
    
    if 'error' not in risk_data:
        risk_score = float(risk_data['risk_score'])
        risk_level = risk_data['risk_level']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Risk Score", f"{risk_score:.1f}/100")
        with col2:
            risk_colors = {"LOW": "green", "MEDIUM": "orange", "HIGH": "red", "CRITICAL": "red"}
            st.markdown(f"**Risk Level:** :{risk_colors[risk_level]}[{risk_level}]")
        with col3:
            st.metric("Licenses Evaluated", risk_data['total_licenses_evaluated'])
        
        if risk_data['risk_factors']:
            st.subheader("Risk Factors")
            for factor in risk_data['risk_factors']:
                st.warning(f"• {factor}")
        
        if risk_data['recommendations']:
            st.subheader("Risk Mitigation Recommendations")
            for rec in risk_data['recommendations']:
                st.info(f"• {rec}")
    else:
        st.error(risk_data['error'])

def show_operations(system):
    st.header("⚙️ Operations Center")
    
    tab1, tab2, tab3 = st.tabs(["Daily Operations", "Health Check", "Backup & Recovery"])
    
    with tab1:
        st.subheader("Daily Operations")
        if st.button("Run Daily Operations"):
            with st.spinner("Running daily operations..."):
                results = system['operations'].daily_operations()
                
                st.success("Daily operations completed!")
                
                for task, result in results['tasks'].items():
                    if result['status'] == 'success':
                        st.success(f"[OK] {task.replace('_', ' ').title()}: Success")
                    else:
                        st.error(f"[ERROR] {task.replace('_', ' ').title()}: {result.get('message', 'Failed')}")
    
    with tab2:
        st.subheader("System Health Check")
        if st.button("Check System Health"):
            health = system['operations'].health_check()
            
            if health['status'] == 'success':
                st.success("[OK] System is healthy")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("License Count", health.get('license_count', 0))
                with col2:
                    st.metric("System Status", health.get('system_health', 'unknown'))
            else:
                st.error(f"[ERROR] System unhealthy: {health.get('message', 'Unknown error')}")
    
    with tab3:
        st.subheader("Backup & Recovery")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Create Backup**")
            if st.button("Create Backup"):
                result = system['operations'].backup_data()
                if result['status'] == 'success':
                    st.success(f"Backup created: {result['backup_file']}")
                else:
                    st.error(f"Backup failed: {result['message']}")
        
        with col2:
            st.write("**Restore from Backup**")
            backup_file = st.text_input("Backup file path:")
            if st.button("Restore") and backup_file:
                result = system['operations'].disaster_recovery(backup_file)
                if result['status'] == 'success':
                    st.success(f"Restored {result['restored_licenses']} licenses")
                else:
                    st.error(f"Restore failed: {result['message']}")

def show_audit_reports(system):
    st.header("📄 Audit Reports")
    
    tab1, tab2 = st.tabs(["Compliance Audit", "Generate Report"])
    
    with tab1:
        st.subheader("Compliance Audit")
        if st.button("Generate Compliance Audit"):
            with st.spinner("Generating compliance audit..."):
                audit_report = system['audit'].compliance_audit()
                
                if 'error' not in audit_report:
                    st.success("Compliance audit completed!")
                    
                    status_color = {"COMPLIANT": "green", "WARNING": "orange", "VIOLATION": "red"}
                    st.markdown(f"**Overall Status:** :{status_color.get(audit_report['overall_status'], 'gray')}[{audit_report['overall_status']}]")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Licenses", audit_report['total_licenses'])
                    with col2:
                        st.metric("Compliant", audit_report['compliance_summary']['compliant'])
                    with col3:
                        st.metric("Warnings", audit_report['compliance_summary']['warnings'])
                    with col4:
                        st.metric("Violations", audit_report['compliance_summary']['violations'])
                    
                    if audit_report['recommendations']:
                        st.subheader("Recommendations")
                        for rec in audit_report['recommendations']:
                            st.info(f"• {rec}")
                else:
                    st.error(f"Audit failed: {audit_report['error']}")
    
    with tab2:
        st.subheader("Generate Custom Audit Report")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")
        
        if st.button("Generate Report") and start_date and end_date:
            start_str = start_date.strftime('%Y-%m-%d')
            end_str = end_date.strftime('%Y-%m-%d')
            
            with st.spinner("Generating audit report..."):
                report = system['audit'].generate_audit_report(start_str, end_str)
                
                if 'error' not in report:
                    st.success(f"Report generated with {report['total_entries']} entries")
                else:
                    st.error(f"Report generation failed: {report['error']}")

def show_logs():
    st.header("📋 System Logs")
    
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    
    if not os.path.exists(logs_dir):
        st.info("Chưa có log files.")
        return
    
    log_files = [f for f in os.listdir(logs_dir) if f.endswith('.log')]
    
    if not log_files:
        st.info("Chưa có log files.")
        return
    
    selected_file = st.selectbox("Chọn log file:", sorted(log_files, reverse=True))
    
    if selected_file:
        log_path = os.path.join(logs_dir, selected_file)
        
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                log_content = f.read()
            
            st.text_area("Log Content:", log_content, height=400)
            
            st.download_button(
                "Download Log File",
                log_content,
                file_name=selected_file,
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"Lỗi đọc log file: {e}")

if __name__ == "__main__":
    main()