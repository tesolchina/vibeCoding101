#!/usr/bin/env python3
"""
Enhanced PDF to Markdown Converter
This script converts PDF files to Markdown format with improved structure detection,
including proper headings, sub-sections, and formatting preservation.

Author: Dr Simon Wang
Date: October 2024
"""

import os
import re
import sys
from pathlib import Path
import logging
from datetime import datetime

try:
    import PyPDF2
    import fitz  # pymupdf
    import pdfplumber
except ImportError as e:
    print(f"Error: Missing required library. Please install: {e}")
    print("Run: pip install PyPDF2 pymupdf pdfplumber")
    sys.exit(1)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedPDFToMarkdown:
    def __init__(self, pdf_path, output_path):
        self.pdf_path = Path(pdf_path)
        self.output_path = Path(output_path)
        self.ensure_output_directory()
        
    def ensure_output_directory(self):
        """Ensure the output directory exists."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
    def extract_with_pymupdf(self):
        """Extract text using PyMuPDF (fitz) with formatting preservation."""
        logger.info("Extracting text with PyMuPDF...")
        doc = fitz.open(self.pdf_path)
        content = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Get text with formatting information
            blocks = page.get_text("dict")
            page_content = self.process_page_blocks(blocks)
            
            if page_content.strip():
                content.append(f"<!-- Page {page_num + 1} -->\n")
                content.append(page_content)
                content.append("\n")
        
        doc.close()
        return "\n".join(content)
    
    def process_page_blocks(self, blocks_dict):
        """Process page blocks to identify structure and formatting."""
        content = []
        
        for block in blocks_dict["blocks"]:
            if "lines" in block:
                block_text = self.process_text_block(block)
                if block_text.strip():
                    content.append(block_text)
        
        return "\n".join(content)
    
    def process_text_block(self, block):
        """Process individual text blocks to detect headings and formatting."""
        lines = []
        
        for line in block["lines"]:
            line_text = ""
            font_sizes = []
            is_bold = False
            
            for span in line["spans"]:
                text = span["text"].strip()
                if text:
                    font_size = span["size"]
                    font_flags = span["flags"]
                    
                    # Check if text is bold (flag 16 indicates bold)
                    if font_flags & 2**4:
                        is_bold = True
                    
                    font_sizes.append(font_size)
                    line_text += text + " "
            
            line_text = line_text.strip()
            if line_text:
                # Determine if this is a heading based on font size and formatting
                if font_sizes:
                    avg_font_size = sum(font_sizes) / len(font_sizes)
                    formatted_line = self.format_line(line_text, avg_font_size, is_bold)
                    lines.append(formatted_line)
        
        return "\n".join(lines)
    
    def format_line(self, text, font_size, is_bold):
        """Format line based on font size and other characteristics."""
        # Clean up the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Skip very short lines that might be artifacts
        if len(text) < 3:
            return text
        
        # Detect potential headings based on various criteria
        if self.is_heading(text, font_size, is_bold):
            heading_level = self.determine_heading_level(text, font_size)
            return f"{'#' * heading_level} {text}\n"
        
        # Detect sub-sections with patterns like "a)", "b)", "2.1", etc.
        if self.is_subsection(text):
            return f"#### {text}\n"
        
        return text
    
    def is_heading(self, text, font_size, is_bold):
        """Determine if text is likely a heading."""
        # Common heading patterns
        heading_patterns = [
            r'^\d+\.?\s+[A-Z]',  # "1. Introduction", "2 Methods"
            r'^[A-Z][A-Z\s]+$',  # All caps
            r'^\d+\.\d+\.?\s+',  # "2.1 Subsection"
            r'^Abstract$',
            r'^Introduction$',
            r'^Conclusion$',
            r'^References$',
            r'^Acknowledgment',
            r'^\d+\s+[A-Z]',  # "1 Introduction"
        ]
        
        for pattern in heading_patterns:
            if re.match(pattern, text):
                return True
        
        # Check if it's a short line that might be a heading
        if len(text) < 100 and (is_bold or font_size > 11):
            # Additional checks for heading-like content
            if not text.endswith('.') or text.endswith('...'):
                return True
        
        return False
    
    def is_subsection(self, text):
        """Detect subsection patterns."""
        subsection_patterns = [
            r'^[a-z]\)\s+\w+',  # "a) Something"
            r'^[A-Z]\)\s+\w+',  # "A) Something"
            r'^\([a-z]\)\s+\w+',  # "(a) Something"
            r'^\([A-Z]\)\s+\w+',  # "(A) Something"
            r'^\d+\.\d+\.\d+\s+',  # "2.1.1 Sub-subsection"
        ]
        
        for pattern in subsection_patterns:
            if re.match(pattern, text):
                return True
        
        return False
    
    def determine_heading_level(self, text, font_size):
        """Determine the appropriate heading level."""
        # Title/Abstract level
        if re.match(r'^(Abstract|Introduction|Conclusion|References)$', text, re.IGNORECASE):
            return 2
        
        # Main sections
        if re.match(r'^\d+\.?\s+[A-Z]', text):
            return 2
        
        # Sub-sections
        if re.match(r'^\d+\.\d+\.?\s+', text):
            return 3
        
        # Sub-sub-sections
        if re.match(r'^\d+\.\d+\.\d+\.?\s+', text):
            return 4
        
        # Default for other headings
        return 3
    
    def extract_with_pdfplumber(self):
        """Extract text using pdfplumber for table and structure detection."""
        logger.info("Extracting text with pdfplumber...")
        content = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_content = []
                
                # Extract tables first
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        page_content.append(self.format_table_as_markdown(table))
                
                # Extract regular text
                text = page.extract_text()
                if text:
                    formatted_text = self.post_process_text(text)
                    page_content.append(formatted_text)
                
                if page_content:
                    content.append(f"<!-- Page {i + 1} -->\n")
                    content.extend(page_content)
                    content.append("\n")
        
        return "\n".join(content)
    
    def format_table_as_markdown(self, table):
        """Convert table to Markdown format."""
        if not table or len(table) == 0:
            return ""
        
        md_table = []
        
        # Header row
        header = table[0]
        md_table.append("| " + " | ".join(str(cell) if cell else "" for cell in header) + " |")
        md_table.append("| " + " | ".join("---" for _ in header) + " |")
        
        # Data rows
        for row in table[1:]:
            md_table.append("| " + " | ".join(str(cell) if cell else "" for cell in row) + " |")
        
        return "\n".join(md_table) + "\n\n"
    
    def post_process_text(self, text):
        """Post-process extracted text to improve formatting."""
        # Split into lines for processing
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Apply formatting based on patterns
            if self.is_heading(line, 12, False):  # Default font size for pattern matching
                heading_level = self.determine_heading_level(line, 12)
                processed_lines.append(f"{'#' * heading_level} {line}")
            elif self.is_subsection(line):
                processed_lines.append(f"#### {line}")
            else:
                processed_lines.append(line)
        
        return "\n".join(processed_lines)
    
    def combine_extractions(self, pymupdf_content, pdfplumber_content):
        """Combine and deduplicate content from different extraction methods."""
        # For now, we'll use the PyMuPDF content as it has better formatting detection
        # In future iterations, we could implement more sophisticated merging
        return pymupdf_content
    
    def clean_and_structure_content(self, content):
        """Final cleaning and structuring of the extracted content."""
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and page markers in final output
            if not line or line.startswith('<!-- Page'):
                cleaned_lines.append(line)
                continue
            
            # Remove multiple consecutive spaces
            line = re.sub(r'\s+', ' ', line)
            
            # Fix common PDF extraction artifacts
            line = re.sub(r'([a-z])([A-Z])', r'\1 \2', line)  # Add space between camelCase
            line = re.sub(r'(\w)(\d)', r'\1 \2', line)  # Add space between word and number
            line = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', line)  # Add space between number and word
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def convert(self):
        """Main conversion method."""
        logger.info(f"Converting {self.pdf_path} to {self.output_path}")
        
        try:
            # Extract using both methods
            pymupdf_content = self.extract_with_pymupdf()
            pdfplumber_content = self.extract_with_pdfplumber()
            
            # Combine the extractions
            combined_content = self.combine_extractions(pymupdf_content, pdfplumber_content)
            
            # Clean and structure the final content
            final_content = self.clean_and_structure_content(combined_content)
            
            # Add metadata header
            header = f"""# {self.pdf_path.stem}

*Converted from PDF to Markdown*
*Generated by Enhanced PDF to Markdown Converter*
*Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

"""
            
            final_content = header + final_content
            
            # Write to output file
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            logger.info(f"Conversion completed. Output saved to {self.output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error during conversion: {e}")
            return False

def main():
    """Main function to run the converter."""
    import datetime
    
    # Define paths
    pdf_path = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/data/s11042-022-13428-4.pdf"
    output_path = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output/paperFull.md"
    
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        return False
    
    # Create converter and run
    converter = EnhancedPDFToMarkdown(pdf_path, output_path)
    success = converter.convert()
    
    if success:
        print(f"✅ Successfully converted PDF to Markdown!")
        print(f"📄 Input: {pdf_path}")
        print(f"📝 Output: {output_path}")
    else:
        print("❌ Conversion failed. Check the logs for details.")
    
    return success

if __name__ == "__main__":
    main()