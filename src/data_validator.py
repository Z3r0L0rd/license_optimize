"""
Data Validation for License System
"""

from datetime import datetime
from typing import Dict, List

class LicenseValidator:
    @staticmethod
    def validate_license_data(data: Dict) -> List[str]:
        """Validate license data"""
        errors = []
        
        # Required fields
        required = ['license_id', 'software_name', 'license_type', 'total_licenses']
        for field in required:
            if not data.get(field):
                errors.append(f"Missing {field}")
        
        # Validate license type
        valid_types = ['SUBSCRIPTION', 'PERPETUAL', 'CONCURRENT', 'NAMED_USER']
        if data.get('license_type') not in valid_types:
            errors.append(f"Invalid license_type. Must be one of: {valid_types}")
        
        # Validate numbers
        if data.get('total_licenses', 0) <= 0:
            errors.append("total_licenses must be positive")
        
        if data.get('used_licenses', 0) < 0:
            errors.append("used_licenses cannot be negative")
        
        # Validate date format
        if data.get('expiry_date'):
            try:
                datetime.strptime(data['expiry_date'], '%Y-%m-%d')
            except ValueError:
                errors.append("expiry_date must be in YYYY-MM-DD format")
        
        return errors