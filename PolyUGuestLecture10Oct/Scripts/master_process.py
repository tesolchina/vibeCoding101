#!/usr/bin/env python3
"""
Master PDF Processing Script
This script orchestrates the complete PDF to Markdown conversion and metadata revision process.

Author: Dr Simon Wang
Date: October 2024
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

class MasterProcessor:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_dir = self.script_dir.parent
        
    def run_script(self, script_name, description):
        """Run a Python script and return success status."""
        print(f"\n🔄 {description}")
        print("-" * 50)
        
        script_path = self.script_dir / script_name
        
        if not script_path.exists():
            print(f"❌ Script not found: {script_path}")
            return False
        
        try:
            result = subprocess.run([
                sys.executable, str(script_path)
            ], capture_output=True, text=True)
            
            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("Errors:", result.stderr)
            
            if result.returncode == 0:
                print(f"✅ {description} completed successfully!")
                return True
            else:
                print(f"❌ {description} failed with return code {result.returncode}")
                return False
                
        except Exception as e:
            print(f"❌ Error running {script_name}: {e}")
            return False
    
    def check_file_exists(self, file_path):
        """Check if a file exists and show its size."""
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ File exists: {path} ({size} bytes)")
            return True
        else:
            print(f"❌ File not found: {path}")
            return False
    
    def show_file_summary(self, file_path, max_lines=10):
        """Show a summary of the file content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                total_lines = len(lines)
                
                print(f"\n📄 File Summary: {Path(file_path).name}")
                print(f"   Total lines: {total_lines}")
                print(f"   First {min(max_lines, total_lines)} lines:")
                
                for i, line in enumerate(lines[:max_lines]):
                    print(f"   {i+1:2d}: {line.rstrip()}")
                
                if total_lines > max_lines:
                    print(f"   ... ({total_lines - max_lines} more lines)")
                    
        except Exception as e:
            print(f"❌ Error reading file summary: {e}")
    
    def process(self):
        """Main processing workflow."""
        print("🎯 Master PDF Processing Workflow")
        print("=" * 50)
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Project directory: {self.project_dir}")
        
        # Step 1: Run PDF conversion
        conversion_success = self.run_script(
            "run_conversion.py", 
            "Step 1: PDF to Markdown Conversion"
        )
        
        if not conversion_success:
            print("\n⚠️  PDF conversion had issues, but continuing with metadata revision...")
        
        # Step 2: Check if paperFull.md was created
        paper_full_path = self.project_dir / "output" / "paperFull.md"
        if self.check_file_exists(paper_full_path):
            self.show_file_summary(paper_full_path)
        
        # Step 3: Run metadata revision
        revision_success = self.run_script(
            "revise_metadata.py",
            "Step 2: Metadata Revision"
        )
        
        # Step 4: Show final results
        print("\n📊 FINAL RESULTS")
        print("=" * 30)
        
        # Check all output files
        output_files = [
            ("paperFull.md", "Full paper in Markdown"),
            ("paperMetaData.md", "Enhanced metadata"),
            ("paperMetaData.md.backup", "Original metadata backup")
        ]
        
        for filename, description in output_files:
            file_path = self.project_dir / "output" / filename
            if self.check_file_exists(file_path):
                print(f"   📝 {description}")
            else:
                print(f"   ❌ Missing: {description}")
        
        # Final summary
        print(f"\n🏁 Process completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if conversion_success and revision_success:
            print("🎉 All steps completed successfully!")
            self.show_completion_summary()
            return True
        elif revision_success:
            print("✅ Metadata revision completed (PDF conversion had issues)")
            return True
        else:
            print("❌ Some steps failed - please check the output above")
            return False
    
    def show_completion_summary(self):
        """Show a summary of what was accomplished."""
        print("\n📋 COMPLETION SUMMARY")
        print("-" * 30)
        print("✅ PDF successfully converted to Markdown")
        print("✅ Document structure and headings extracted")
        print("✅ Metadata file enhanced with full paper analysis")
        print("✅ Sub-sections and lettered items identified")
        print("✅ Original metadata backed up")
        print("\n📁 Output files location:")
        print(f"   {self.project_dir / 'output'}")
        print("\n🔧 Scripts available in:")
        print(f"   {self.script_dir}")

def main():
    """Main function."""
    processor = MasterProcessor()
    success = processor.process()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()