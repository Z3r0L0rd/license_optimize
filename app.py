#!/usr/bin/env python3
"""
AWS Amplify entry point for License Optimization System
"""

import subprocess
import sys
import os

def main():
    """Start Streamlit app for Amplify deployment"""
    try:
        # Set environment for production
        os.environ['STREAMLIT_SERVER_PORT'] = '8501'
        os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
        
        # Run Streamlit app
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'streamlit_app.py',
            '--server.port=8501',
            '--server.address=0.0.0.0',
            '--server.headless=true'
        ])
    except Exception as e:
        print(f"Error starting app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()