#!/usr/bin/env python3
"""
Simple PDF to Markdown Converter
A fallback script that uses only PyPDF2 for basic PDF text extraction.

Author: Dr Simon Wang
Date: October 2024
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 is required. Install with: pip install PyPDF2")
    sys.exit(1)

class SimplePDFToMarkdown:
    def __init__(self, pdf_path, output_path):
        self.pdf_path = Path(pdf_path)
        self.output_path = Path(output_path)
        self.ensure_output_directory()
        
    def ensure_output_directory(self):
        """Ensure the output directory exists."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def extract_text_pypdf2(self):
        """Extract text using PyPDF2."""
        content = []
        
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text.strip():
                    content.append(f"<!-- Page {page_num + 1} -->\n")
                    content.append(text)
                    content.append("\n")
        
        return "\n".join(content)
    
    def detect_and_format_structure(self, text):
        """Detect and format headings and structure in the text."""
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append(line)
                continue
            
            # Clean up line
            line = re.sub(r'\s+', ' ', line)
            
            # Skip page markers
            if line.startswith('<!-- Page'):
                formatted_lines.append(line)
                continue
            
            # Detect various heading patterns
            if self.is_main_heading(line):
                formatted_lines.append(f"## {line}")
            elif self.is_section_heading(line):
                formatted_lines.append(f"### {line}")
            elif self.is_subsection_heading(line):
                formatted_lines.append(f"#### {line}")
            elif self.is_sub_item(line):
                formatted_lines.append(f"##### {line}")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def is_main_heading(self, line):
        """Detect main headings."""
        patterns = [
            r'^Abstract$',
            r'^Introduction$',
            r'^Conclusion$',
            r'^References$',
            r'^Acknowledgment',
            r'^[A-Z][A-Z\s]+$',  # All caps short lines
        ]
        
        return any(re.match(pattern, line, re.IGNORECASE) for pattern in patterns)
    
    def is_section_heading(self, line):
        """Detect section headings."""
        patterns = [
            r'^\d+\.?\s+[A-Z]',  # "1. Introduction", "2 Methods"
            r'^\d+\s+[A-Z]',     # "1 Introduction"
        ]
        
        return any(re.match(pattern, line) for pattern in patterns)
    
    def is_subsection_heading(self, line):
        """Detect subsection headings."""
        patterns = [
            r'^\d+\.\d+\.?\s+',   # "2.1 Subsection"
            r'^\d+\.\d+\s+[A-Z]', # "2.1 Something"
        ]
        
        return any(re.match(pattern, line) for pattern in patterns)
    
    def is_sub_item(self, line):
        """Detect sub-items like a), b), etc."""
        patterns = [
            r'^[a-z]\)\s+\w+',     # "a) Something"
            r'^[A-Z]\)\s+\w+',     # "A) Something"
            r'^\([a-z]\)\s+\w+',   # "(a) Something"
            r'^\([A-Z]\)\s+\w+',   # "(A) Something"
            r'^\d+\.\d+\.\d+\s+',  # "2.1.1 Sub-subsection"
        ]
        
        return any(re.match(pattern, line) for pattern in patterns)
    
    def clean_text(self, text):
        """Clean and improve the extracted text."""
        # Fix common PDF extraction issues
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between words
        text = re.sub(r'(\w)(\d)', r'\1 \2', text)        # Add space between word and number
        text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)  # Add space between number and word
        
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)     # Max 2 consecutive newlines
        text = re.sub(r' +', ' ', text)                   # Multiple spaces to single
        
        return text
    
    def convert(self):
        """Main conversion method."""
        print(f"Converting {self.pdf_path} to {self.output_path}")
        
        try:
            # Extract text
            raw_text = self.extract_text_pypdf2()
            
            # Clean the text
            cleaned_text = self.clean_text(raw_text)
            
            # Format structure
            formatted_text = self.detect_and_format_structure(cleaned_text)
            
            # Add metadata header
            header = f"""# {self.pdf_path.stem}

*Converted from PDF to Markdown*
*Generated by Simple PDF to Markdown Converter*
*Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

"""
            
            final_content = header + formatted_text
            
            # Write to output file
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            print(f"✅ Conversion completed. Output saved to {self.output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error during conversion: {e}")
            return False

def main():
    """Main function."""
    # Define paths
    pdf_path = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/data/s11042-022-13428-4.pdf"
    output_path = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output/paperFull.md"
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return False
    
    # Create converter and run
    converter = SimplePDFToMarkdown(pdf_path, output_path)
    success = converter.convert()
    
    if success:
        print(f"📄 Input: {pdf_path}")
        print(f"📝 Output: {output_path}")
    
    return success

if __name__ == "__main__":
    main()