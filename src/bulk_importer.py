"""
Bulk Import/Export for License Data
"""

import csv
import json
from typing import List, Dict
from license_tracker import LicenseTracker
from data_validator import LicenseValidator

class BulkImporter:
    def __init__(self):
        self.tracker = LicenseTracker()
        self.validator = LicenseValidator()
    
    def import_from_csv(self, file_path: str) -> Dict:
        """Import licenses from CSV"""
        results = {'success': 0, 'errors': []}
        
        # Auto-create database table if not exists
        try:
            self.tracker.create_table_if_not_exists()
        except Exception as e:
            results['errors'].append(f"Database setup failed: {str(e)}")
            return results
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Check if file has required headers
                required_headers = ['license_id', 'software_name', 'license_type', 'total_licenses', 'cost_per_license']
                if not all(header in reader.fieldnames for header in required_headers):
                    results['errors'].append(f"Missing required headers. Expected: {required_headers}")
                    return results
                
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Clean and convert data
                        cleaned_row = {}
                        
                        # String fields
                        cleaned_row['license_id'] = str(row.get('license_id', '')).strip()
                        cleaned_row['software_name'] = str(row.get('software_name', '')).strip()
                        cleaned_row['license_type'] = str(row.get('license_type', 'SUBSCRIPTION')).strip().upper()
                        cleaned_row['expiry_date'] = str(row.get('expiry_date', '')).strip()
                        
                        # Numeric fields with better error handling
                        try:
                            cleaned_row['total_licenses'] = int(float(str(row.get('total_licenses', 0)).strip()))
                        except (ValueError, TypeError):
                            results['errors'].append(f"Row {row_num}: Invalid total_licenses value: {row.get('total_licenses')}")
                            continue
                        
                        try:
                            cleaned_row['used_licenses'] = int(float(str(row.get('used_licenses', 0)).strip()))
                        except (ValueError, TypeError):
                            cleaned_row['used_licenses'] = 0
                        
                        try:
                            cleaned_row['cost_per_license'] = float(str(row.get('cost_per_license', 0)).strip())
                        except (ValueError, TypeError):
                            results['errors'].append(f"Row {row_num}: Invalid cost_per_license value: {row.get('cost_per_license')}")
                            continue
                        
                        # Skip empty rows
                        if not cleaned_row['license_id'] or not cleaned_row['software_name']:
                            continue
                        
                        # Validate data
                        errors = self.validator.validate_license_data(cleaned_row)
                        if errors:
                            results['errors'].append(f"Row {row_num}: {', '.join(errors)}")
                            continue
                        
                        # Add license
                        try:
                            if self.tracker.add_license(cleaned_row):
                                results['success'] += 1
                            else:
                                results['errors'].append(f"Row {row_num}: Database error adding license {cleaned_row['license_id']}")
                        except Exception as e:
                            results['errors'].append(f"Row {row_num}: Exception adding license {cleaned_row['license_id']}: {str(e)}")
                    
                    except Exception as e:
                        results['errors'].append(f"Row {row_num}: Processing error - {str(e)}")
                        continue
        
        except FileNotFoundError:
            results['errors'].append("File not found")
        except UnicodeDecodeError:
            results['errors'].append("File encoding error - try saving as UTF-8")
        except Exception as e:
            results['errors'].append(f"File error: {str(e)}")
            import traceback
            results['errors'].append(f"Traceback: {traceback.format_exc()}")
        
        return results
    
    def export_to_csv(self, file_path: str) -> bool:
        """Export licenses to CSV"""
        # Auto-create database table if not exists
        try:
            self.tracker.create_table_if_not_exists()
        except Exception:
            return False
            
        try:
            licenses = self.tracker.get_all_licenses()
            if not licenses:
                return False
            
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['license_id', 'software_name', 'license_type', 
                            'total_licenses', 'used_licenses', 'expiry_date', 'cost_per_license']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for license in licenses:
                    # Clean data for export
                    export_row = {}
                    for field in fieldnames:
                        value = license.get(field, '')
                        
                        # Convert Decimal to float
                        if field == 'cost_per_license':
                            export_row[field] = float(str(value)) if value else 0.0
                        # Convert int fields
                        elif field in ['total_licenses', 'used_licenses']:
                            export_row[field] = int(value) if value else 0
                        # String fields
                        else:
                            export_row[field] = str(value) if value else ''
                    
                    writer.writerow(export_row)
            
            return True
        except Exception as e:
            print(f"Export error: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return False