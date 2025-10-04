#!/usr/bin/env python3
"""
PDF Conversion Runner
This script installs dependencies and runs the PDF to Markdown conversion.

Author: Dr Simon Wang
Date: October 2024
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")
    
    requirements_path = Path(__file__).parent / "requirements.txt"
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_path)
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def run_enhanced_converter():
    """Try to run the enhanced converter."""
    print("🚀 Running enhanced PDF converter...")
    
    try:
        enhanced_script = Path(__file__).parent / "enhanced_pdf_to_md.py"
        subprocess.check_call([sys.executable, str(enhanced_script)])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Enhanced converter failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running enhanced converter: {e}")
        return False

def run_simple_converter():
    """Run the simple converter as fallback."""
    print("🔄 Running simple PDF converter as fallback...")
    
    try:
        simple_script = Path(__file__).parent / "simple_pdf_to_md.py"
        subprocess.check_call([sys.executable, str(simple_script)])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Simple converter failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running simple converter: {e}")
        return False

def main():
    """Main execution function."""
    print("🎯 PDF to Markdown Conversion Runner")
    print("=" * 40)
    
    # Try to install dependencies first
    if install_requirements():
        # Try enhanced converter
        if run_enhanced_converter():
            print("🎉 Conversion completed with enhanced converter!")
            return True
    
    # Fallback to simple converter
    print("⚠️  Falling back to simple converter...")
    if run_simple_converter():
        print("🎉 Conversion completed with simple converter!")
        return True
    
    print("❌ All conversion attempts failed.")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)