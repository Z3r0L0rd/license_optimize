"""
Audit System for License Optimization
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from logger import LicenseLogger

class AuditSystem:
    def __init__(self):
        self.logger = LicenseLogger()
        self.audit_dir = os.path.join(os.path.dirname(__file__), '..', 'audit')
        os.makedirs(self.audit_dir, exist_ok=True)
    
    def log_change(self, action: str, entity_type: str, entity_id: str, 
                   old_data: Optional[Dict] = None, new_data: Optional[Dict] = None,
                   user: str = 'system') -> str:
        """Log audit trail for changes"""
        
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'audit_id': f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            'action': action,  # CREATE, UPDATE, DELETE, VIEW
            'entity_type': entity_type,  # LICENSE, USER, SYSTEM
            'entity_id': entity_id,
            'user': user,
            'old_data': old_data,
            'new_data': new_data,
            'ip_address': self._get_client_ip(),
            'session_id': self._get_session_id()
        }
        
        # Save to audit log
        audit_file = os.path.join(self.audit_dir, f"audit_{datetime.now().strftime('%Y%m')}.json")
        
        try:
            # Append to monthly audit file
            if os.path.exists(audit_file):
                with open(audit_file, 'r') as f:
                    audit_data = json.load(f)
            else:
                audit_data = {'entries': []}
            
            audit_data['entries'].append(audit_entry)
            
            with open(audit_file, 'w') as f:
                json.dump(audit_data, f, indent=2)
            
            self.logger.info(f"Audit logged: {audit_entry['audit_id']}")
            return audit_entry['audit_id']
            
        except Exception as e:
            self.logger.error(f"Failed to log audit entry: {e}")
            return ""
    
    def generate_audit_report(self, start_date: str, end_date: str) -> Dict:
        """Generate audit report for date range"""
        
        try:
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            
            audit_entries = []
            
            # Read audit files in date range
            current_date = start_dt.replace(day=1)
            while current_date <= end_dt:
                audit_file = os.path.join(self.audit_dir, f"audit_{current_date.strftime('%Y%m')}.json")
                
                if os.path.exists(audit_file):
                    with open(audit_file, 'r') as f:
                        audit_data = json.load(f)
                        
                    for entry in audit_data['entries']:
                        entry_date = datetime.fromisoformat(entry['timestamp'])
                        if start_dt <= entry_date <= end_dt:
                            audit_entries.append(entry)
                
                # Move to next month
                if current_date.month == 12:
                    current_date = current_date.replace(year=current_date.year + 1, month=1)
                else:
                    current_date = current_date.replace(month=current_date.month + 1)
            
            # Generate summary
            summary = self._generate_audit_summary(audit_entries)
            
            report = {
                'report_id': f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'generated_at': datetime.now().isoformat(),
                'period': {'start': start_date, 'end': end_date},
                'total_entries': len(audit_entries),
                'summary': summary,
                'entries': audit_entries
            }
            
            # Save report
            report_file = os.path.join(self.audit_dir, f"{report['report_id']}.json")
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate audit report: {e}")
            return {'error': str(e)}
    
    def _generate_audit_summary(self, entries: List[Dict]) -> Dict:
        """Generate summary statistics from audit entries"""
        
        summary = {
            'actions': {},
            'entity_types': {},
            'users': {},
            'daily_activity': {}
        }
        
        for entry in entries:
            # Count actions
            action = entry['action']
            summary['actions'][action] = summary['actions'].get(action, 0) + 1
            
            # Count entity types
            entity_type = entry['entity_type']
            summary['entity_types'][entity_type] = summary['entity_types'].get(entity_type, 0) + 1
            
            # Count users
            user = entry['user']
            summary['users'][user] = summary['users'].get(user, 0) + 1
            
            # Daily activity
            date = entry['timestamp'][:10]  # YYYY-MM-DD
            summary['daily_activity'][date] = summary['daily_activity'].get(date, 0) + 1
        
        return summary
    
    def compliance_audit(self) -> Dict:
        """Generate compliance audit report"""
        
        try:
            from compliance_checker import ComplianceChecker
            from license_tracker import LicenseTracker
            
            compliance = ComplianceChecker()
            tracker = LicenseTracker()
            
            # Get current compliance status
            compliance_data = compliance.check_compliance_status()
            licenses = tracker.get_all_licenses()
            
            # Generate compliance report
            report = {
                'audit_type': 'compliance',
                'generated_at': datetime.now().isoformat(),
                'overall_status': compliance_data['overall_status'],
                'total_licenses': len(licenses),
                'compliance_summary': {
                    'compliant': len(compliance_data['compliant']),
                    'warnings': len(compliance_data['warnings']),
                    'violations': len(compliance_data['violations'])
                },
                'violations': compliance_data['violations'],
                'recommendations': self._generate_compliance_recommendations(compliance_data)
            }
            
            # Save compliance audit
            audit_file = os.path.join(self.audit_dir, f"compliance_audit_{datetime.now().strftime('%Y%m%d')}.json")
            with open(audit_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            # Log audit action
            self.log_change('AUDIT', 'COMPLIANCE', 'system', user='audit_system')
            
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate compliance audit: {e}")
            return {'error': str(e)}
    
    def _generate_compliance_recommendations(self, compliance_data: Dict) -> List[str]:
        """Generate compliance recommendations"""
        
        recommendations = []
        
        if compliance_data['violations']:
            recommendations.append("Immediate action required for license violations")
            recommendations.append("Review and renew expired licenses")
            recommendations.append("Implement automated compliance monitoring")
        
        if compliance_data['warnings']:
            recommendations.append("Monitor licenses approaching limits")
            recommendations.append("Plan for license renewals")
        
        if compliance_data['overall_status'] != 'COMPLIANT':
            recommendations.append("Establish regular compliance review process")
            recommendations.append("Implement preventive controls")
        
        return recommendations
    
    def _get_client_ip(self) -> str:
        """Get client IP address (placeholder)"""
        return "127.0.0.1"  # Local system
    
    def _get_session_id(self) -> str:
        """Get session ID (placeholder)"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"