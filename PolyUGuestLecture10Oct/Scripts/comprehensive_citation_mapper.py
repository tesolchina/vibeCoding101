#!/usr/bin/env python3
"""
Comprehensive Citation Mapper - finds ALL citations in the paper

Author: Simon Wang
Date: 2025-10-04
"""

import re
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import logging

# Set up logging
log_file = '/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/Plan&test/citeMappinglog.md'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def extract_all_citations(content):
    """Extract ALL citations using simple regex"""
    # Find all citation patterns [number] or [number, number] etc.
    pattern = r'\[\s*([0-9\s,–\-]+)\s*\]'
    citations = []
    
    # Split into paragraphs for context
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.startswith('#')]
    
    for para_idx, paragraph in enumerate(paragraphs):
        matches = re.finditer(pattern, paragraph)
        
        for match in matches:
            citation_text = match.group(1)
            
            # Extract individual reference numbers
            ref_numbers = []
            
            # Handle ranges like "78 – 80"
            range_match = re.search(r'(\d+)\s*[–\-]\s*(\d+)', citation_text)
            if range_match:
                start = int(range_match.group(1))
                end = int(range_match.group(2))
                ref_numbers = list(range(start, min(end + 1, start + 10)))  # Limit range
            else:
                # Handle comma-separated numbers
                ref_numbers = [int(num.strip()) for num in re.findall(r'\d+', citation_text)]
            
            # Get context (truncated)
            context = paragraph[:250] + "..." if len(paragraph) > 250 else paragraph
            
            for ref_num in ref_numbers:
                citations.append({
                    'ref_number': str(ref_num),
                    'context': context,
                    'paragraph_index': para_idx,
                    'original_match': match.group(0)
                })
    
    return citations

def extract_references(content):
    """Extract reference list"""
    references = {}
    
    # Pattern for references with space-separated numbers: "## 6 6. Author..."
    pattern = r'^##\s*(\d+)\s*(\d+)?\.\s*(.+?)(?=^##\s*\d+|$)'
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        if match[1]:  # Two-digit format like "6 6"
            ref_num = match[0] + match[1]
        else:  # Single number format
            ref_num = match[0]
        
        ref_text = match[2] if match[1] else match[1]
        if not ref_text:  # If there's no third group, use the second
            ref_text = match[1] if not match[1] else match[0]
        
        # Clean up reference text
        ref_text = re.sub(r'\s+', ' ', str(ref_text).strip())
        ref_text = ref_text.split('\n')[0]  # Take only first line
        if len(ref_text) > 300:
            ref_text = ref_text[:300] + "..."
            
        references[ref_num] = ref_text
    
    return references

def create_comprehensive_csv(input_file, output_dir):
    """Create comprehensive citation mapping"""
    
    # Read file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    logger.info(f"Processing file: {input_file}")
    logger.info(f"File size: {len(content)} characters")
    
    # Extract data
    citations = extract_all_citations(content)
    references = extract_references(content)
    
    logger.info(f"Found {len(citations)} citation instances")
    logger.info(f"Found {len(references)} references")
    
    # Group citations by reference number
    citation_groups = defaultdict(list)
    for citation in citations:
        citation_groups[citation['ref_number']].append(citation)
    
    # Create output
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_file = Path(output_dir) / f'comprehensive_citations_{timestamp}.csv'
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'Ref_Number',
            'Reference_Text',
            'Citation_Count',
            'Context_1',
            'Context_2',
            'Context_3',
            'All_Contexts'
        ])
        
        # Data
        for ref_num in sorted(citation_groups.keys(), key=int):
            group = citation_groups[ref_num]
            ref_text = references.get(ref_num, "Reference not found")
            
            contexts = [c['context'] for c in group]
            
            row = [
                ref_num,
                ref_text,
                len(contexts),
                contexts[0] if len(contexts) > 0 else "",
                contexts[1] if len(contexts) > 1 else "",
                contexts[2] if len(contexts) > 2 else "",
                " | ".join(contexts) if len(contexts) <= 5 else " | ".join(contexts[:5]) + f" | ... and {len(contexts)-5} more"
            ]
            
            writer.writerow(row)
    
    # Create summary
    summary_file = Path(output_dir) / f'citation_summary_{timestamp}.md'
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# Comprehensive Citation Analysis\\n\\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
        f.write(f"**Source:** {input_file}\\n\\n")
        
        f.write("## Summary Statistics\\n\\n")
        f.write(f"- Total citation instances: {len(citations)}\\n")
        f.write(f"- Unique references cited: {len(citation_groups)}\\n")
        f.write(f"- Total references in bibliography: {len(references)}\\n")
        
        # Most cited
        f.write("\\n## Most Frequently Cited\\n\\n")
        sorted_groups = sorted(citation_groups.items(), key=lambda x: len(x[1]), reverse=True)
        
        for i, (ref_num, group) in enumerate(sorted_groups[:10]):
            ref_text = references.get(ref_num, "Reference not found")
            f.write(f"{i+1}. **Ref #{ref_num}** ({len(group)} times): {ref_text[:100]}...\\n")
        
        f.write("\\n## Reference Coverage\\n\\n")
        cited_refs = set(citation_groups.keys())
        all_refs = set(references.keys())
        uncited_refs = all_refs - cited_refs
        
        f.write(f"- References cited: {len(cited_refs)} / {len(all_refs)} ({len(cited_refs)/len(all_refs)*100:.1f}%)\\n")
        
        if uncited_refs:
            f.write(f"\\n### Uncited References\\n\\n")
            for ref_num in sorted(uncited_refs, key=int):
                f.write(f"- Ref #{ref_num}: {references[ref_num][:100]}...\\n")
    
    logger.info(f"Generated comprehensive CSV: {csv_file}")
    logger.info(f"Generated summary report: {summary_file}")
    
    return csv_file, summary_file

def main():
    input_file = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output/paperFull.md"
    output_dir = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output"
    
    csv_file, summary_file = create_comprehensive_csv(input_file, output_dir)
    
    print(f"\\n🎉 Comprehensive citation analysis completed!")
    print(f"📊 CSV file: {csv_file}")
    print(f"📋 Summary report: {summary_file}")

if __name__ == "__main__":
    main()