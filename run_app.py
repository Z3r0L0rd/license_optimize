"""
Script to run the Streamlit License Optimization App
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting License Optimization System...")
    print("=" * 50)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    
    # Run streamlit app
    app_path = os.path.join(os.path.dirname(__file__), "streamlit_app.py")
    
    print(f"🌐 Starting web app at: http://localhost:8501")
    print("📋 Use Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")

if __name__ == "__main__":
    main()