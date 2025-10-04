#!/usr/bin/env python3
"""
Extract All References from Academic Paper
==========================================

This script extracts all references from the bibliography section of paperFull.md
and saves them to a structured JSON file for individual citation searching.

Created: 2024-10-04
Author: Citation Mapping System
"""

import re
import json
import os
from datetime import datetime

def extract_all_references(file_path):
    """
    Extract all references from the paper's bibliography section.
    
    Args:
        file_path (str): Path to the markdown file
    
    Returns:
        list: List of dictionaries containing reference information
    """
    references = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find the References section
        references_pattern = r'## References\s*\n(.*?)(?=\n##|\n#|$)'
        references_match = re.search(references_pattern, content, re.DOTALL)
        
        if not references_match:
            print("References section not found!")
            return references
        
        references_text = references_match.group(1)
        print(f"Found references section with {len(references_text)} characters")
        
        # Pattern 1: Standard numbered references (## 1. Author...)
        pattern1 = r'## (\d+)\.\s+(.+?)(?=\n## \d+\.|\n[^\s]|\Z)'
        matches1 = re.findall(pattern1, references_text, re.DOTALL)
        
        for match in matches1:
            ref_num = int(match[0])
            ref_text = match[1].strip().replace('\n', ' ')
            ref_text = re.sub(r'\s+', ' ', ref_text)  # Clean up extra spaces
            
            references.append({
                'number': ref_num,
                'text': ref_text,
                'type': 'standard'
            })
        
        # Pattern 2: References without leading ##
        pattern2 = r'^(\d+)\.\s+(.+?)(?=\n\d+\.|\n[^\s]|\Z)'
        matches2 = re.findall(pattern2, references_text, re.MULTILINE | re.DOTALL)
        
        for match in matches2:
            ref_num = int(match[0])
            # Skip if already found in pattern1
            if any(ref['number'] == ref_num for ref in references):
                continue
                
            ref_text = match[1].strip().replace('\n', ' ')
            ref_text = re.sub(r'\s+', ' ', ref_text)
            
            references.append({
                'number': ref_num,
                'text': ref_text,
                'type': 'alternative'
            })
        
        # Pattern 3: Handle spaced numbers (like "5 6." for reference 56)
        pattern3 = r'(\d+\s+\d+)\.\s+(.+?)(?=\n\d+\s+\d+\.|\n\d+\.|\n[^\s]|\Z)'
        matches3 = re.findall(pattern3, references_text, re.MULTILINE | re.DOTALL)
        
        for match in matches3:
            # Convert spaced number to actual number
            spaced_num = match[0].replace(' ', '')
            ref_num = int(spaced_num)
            
            # Skip if already found
            if any(ref['number'] == ref_num for ref in references):
                continue
                
            ref_text = match[1].strip().replace('\n', ' ')
            ref_text = re.sub(r'\s+', ' ', ref_text)
            
            references.append({
                'number': ref_num,
                'text': ref_text,
                'type': 'spaced'
            })
        
        # Sort by reference number
        references.sort(key=lambda x: x['number'])
        
        # Check for missing references
        if references:
            max_ref = max(ref['number'] for ref in references)
            all_numbers = set(ref['number'] for ref in references)
            missing = [i for i in range(1, max_ref + 1) if i not in all_numbers]
            
            if missing:
                print(f"Missing reference numbers: {missing}")
        
        print(f"Successfully extracted {len(references)} references")
        return references
        
    except Exception as e:
        print(f"Error extracting references: {e}")
        return references

def save_references_to_json(references, output_dir):
    """Save references to JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"all_references_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    data = {
        'extraction_date': datetime.now().isoformat(),
        'total_references': len(references),
        'references': references
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"References saved to: {filepath}")
    return filepath

def print_reference_summary(references):
    """Print a summary of extracted references."""
    print("\n" + "="*80)
    print("REFERENCE EXTRACTION SUMMARY")
    print("="*80)
    
    if not references:
        print("No references found!")
        return
    
    print(f"Total references extracted: {len(references)}")
    
    # Group by type
    types = {}
    for ref in references:
        ref_type = ref['type']
        if ref_type not in types:
            types[ref_type] = []
        types[ref_type].append(ref['number'])
    
    for ref_type, numbers in types.items():
        print(f"  {ref_type}: {len(numbers)} references")
        if len(numbers) <= 10:
            print(f"    Numbers: {numbers}")
    
    # Show first and last few references
    print(f"\nFirst 5 references:")
    for ref in references[:5]:
        print(f"  {ref['number']}. {ref['text'][:100]}...")
    
    if len(references) > 10:
        print(f"\nLast 5 references:")
        for ref in references[-5:]:
            print(f"  {ref['number']}. {ref['text'][:100]}...")
    
    # Check for gaps
    numbers = [ref['number'] for ref in references]
    if numbers:
        expected = list(range(1, max(numbers) + 1))
        missing = [n for n in expected if n not in numbers]
        if missing:
            print(f"\nMissing reference numbers: {missing}")
        else:
            print(f"\nNo missing references found (1-{max(numbers)})")

def main():
    """Main execution function."""
    # File paths
    paper_file = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output/paperFull.md"
    output_dir = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output"
    
    # Extract references
    print("Starting reference extraction...")
    references = extract_all_references(paper_file)
    
    # Print summary
    print_reference_summary(references)
    
    # Save to JSON
    if references:
        json_path = save_references_to_json(references, output_dir)
        
        # Save a simple text list too
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt_path = os.path.join(output_dir, f"reference_list_{timestamp}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("ALL EXTRACTED REFERENCES\n")
            f.write("="*50 + "\n\n")
            for ref in references:
                f.write(f"{ref['number']}. {ref['text']}\n\n")
        
        print(f"Reference list also saved to: {txt_path}")
        
        return json_path
    else:
        print("No references extracted!")
        return None

if __name__ == "__main__":
    main()