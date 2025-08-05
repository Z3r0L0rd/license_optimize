"""
Logging System for License Optimization
"""

import logging
import os
from datetime import datetime

class LicenseLogger:
    def __init__(self):
        # Create logs directory
        logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Setup logger
        self.logger = logging.getLogger('license_optimization')
        self.logger.setLevel(logging.INFO)
        
        # File handler
        log_file = os.path.join(logs_dir, f"license_system_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def warning(self, message: str):
        self.logger.warning(message)