#!/usr/bin/env python3
"""
Final Comprehensive Citation Mapper
===================================

This script comprehensively extracts all references and maps all citations in the paper,
using the correct spaced citation format discovered in the text.

Created: 2024-10-04
Author: Citation Mapping System
"""

import re
import json
import csv
import os
from datetime import datetime

def extract_all_references(file_path):
    """Extract all references from the bibliography section."""
    references = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find the References section
        references_pattern = r'## References\s*\n(.*?)(?=\nPublisher|\Z)'
        references_match = re.search(references_pattern, content, re.DOTALL)
        
        if not references_match:
            print("References section not found!")
            return references
        
        references_text = references_match.group(1)
        print(f"Found references section with {len(references_text)} characters")
        
        # IMPORTANT: All reference numbers >=10 are in spaced format in this document
        # Pattern 1: Single digit references (## 1. to ## 9.)
        pattern1 = r'## ([1-9])\. (.+?)(?=\n## [1-9]\\.|\n## \d+ \d+\.|\Z)'
        matches1 = re.findall(pattern1, references_text, re.DOTALL)
        
        # Pattern 2: All multi-digit references are spaced (## 1 0., ## 1 1., etc.)
        pattern2 = r'## (\d+ \d+)\. (.+?)(?=\n## \d+ \d+\.|\n## [1-9]\.|\Z)'
        matches2 = re.findall(pattern2, references_text, re.DOTALL)
        
        print(f"Found {len(matches1)} single-digit and {len(matches2)} spaced multi-digit references")
        
        # Process single-digit references
        for match in matches1:
            ref_num = int(match[0])
            ref_text = match[1].strip()
            ref_text = re.sub(r'\s+', ' ', ref_text)
            
            references.append({
                'number': ref_num,
                'text': ref_text,
                'type': 'single-digit'
            })
        
        # Process multi-digit references
        for match in matches2:
            # Convert spaced number to actual number ("1 0" -> 10)
            spaced_num = match[0].replace(' ', '')
            ref_num = int(spaced_num)
            ref_text = match[1].strip()
            ref_text = re.sub(r'\s+', ' ', ref_text)
            
            references.append({
                'number': ref_num,
                'text': ref_text,
                'type': 'multi-digit'
            })
        
        # Look for standalone references without ## prefix
        lines = references_text.split('\n')
        for i, line in enumerate(lines):
            # Look for lines like "56. text" or "9 1. text" 
            standalone_match = re.match(r'^(\d+(?:\s+\d+)?)\. (.+)', line.strip())
            if standalone_match:
                ref_num_str = standalone_match.group(1).replace(' ', '')
                if ref_num_str.isdigit():
                    ref_num = int(ref_num_str)
                    
                    # Skip if already found
                    if any(ref['number'] == ref_num for ref in references):
                        continue
                    
                    # Collect the full reference text
                    ref_text = standalone_match.group(2)
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j].strip()
                        if re.match(r'^\d+(?:\s+\d+)?\.|^##|^Publisher', next_line):
                            break
                        if next_line:
                            ref_text += ' ' + next_line
                        j += 1
                    
                    ref_text = re.sub(r'\s+', ' ', ref_text).strip()
                    
                    references.append({
                        'number': ref_num,
                        'text': ref_text,
                        'type': 'standalone'
                    })
        
        # Sort by reference number
        references.sort(key=lambda x: x['number'])
        
        print(f"Successfully extracted {len(references)} references")
        return references
        
    except Exception as e:
        print(f"Error extracting references: {e}")
        return references

def format_ref_number_for_search(ref_num):
    """Convert reference number to search patterns based on paper format."""
    ref_str = str(ref_num)
    
    # For numbers >= 10, they appear as spaced format like "1 2" for 12
    if len(ref_str) >= 2:
        spaced = ' '.join(ref_str)  # "12" -> "1 2"
        return [ref_str, spaced]  # Return both formats
    else:
        return [ref_str]  # Single digit numbers stay as is

def search_reference_comprehensive(content, ref_num, ref_text):
    """Search for a specific reference using comprehensive patterns."""
    citations = []
    
    # Get different number formats
    number_formats = format_ref_number_for_search(ref_num)
    
    # Extract author and year for additional patterns
    author_match = re.search(r'^([A-Za-z\s,&]+?)\s*\([12]\d{3}', ref_text)
    authors = author_match.group(1).strip() if author_match else ""
    
    year_match = re.search(r'\((\d{4})\)', ref_text)
    year = year_match.group(1) if year_match else ""
    
    # Build comprehensive search patterns
    patterns = []
    
    for num_format in number_formats:
        # Direct citation patterns
        patterns.extend([
            f'\\[ {num_format} \\]',  # [ 1 2 ]
            f'\\[{num_format}\\]',    # [12]
            f'\\( {num_format} \\)',  # ( 1 2 )
            f'\\({num_format}\\)',    # (12)
        ])
        
        # Citation in lists and ranges
        patterns.extend([
            f'\\[ {num_format},',     # [ 1 2, others]
            f'\\[{num_format},',      # [12, others]
            f', {num_format} \\]',    # [others, 1 2 ]
            f',{num_format}\\]',      # [others,12]
            f', {num_format},',       # [others, 1 2, more]
            f',{num_format},',        # [others,12,more]
        ])
        
        # Author-year combinations
        if authors and year:
            first_author = authors.split(',')[0].split('&')[0].strip()
            patterns.extend([
                f'{first_author}.*?{year}.*?\\[ {num_format} \\]',
                f'{first_author}.*?{year}.*?\\[{num_format}\\]',
                f'\\( {first_author}.*?{year} \\).*?\\[ {num_format} \\]',
            ])
    
    # Search for each pattern
    for pattern in patterns:
        try:
            matches = list(re.finditer(pattern, content, re.IGNORECASE | re.DOTALL))
            for match in matches:
                # Get context around the match
                start = max(0, match.start() - 150)
                end = min(len(content), match.end() + 150)
                context = content[start:end].strip()
                
                # Clean up context
                context = re.sub(r'\s+', ' ', context)
                
                citations.append({
                    'pattern': pattern,
                    'match': match.group(),
                    'context': context,
                    'position': match.start()
                })
        except re.error as e:
            print(f"Regex error with pattern '{pattern}': {e}")
    
    # Remove duplicates based on position
    seen_positions = set()
    unique_citations = []
    for citation in citations:
        pos_range = range(citation['position'] - 5, citation['position'] + 6)
        if not any(p in seen_positions for p in pos_range):
            unique_citations.append(citation)
            seen_positions.add(citation['position'])
    
    return unique_citations

def search_all_references(paper_file, references):
    """Search for all references in the paper."""
    print("\n" + "="*80)
    print("COMPREHENSIVE CITATION SEARCH")
    print("="*80)
    
    try:
        with open(paper_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading paper file: {e}")
        return []
    
    all_results = []
    total_citations = 0
    
    for i, ref in enumerate(references, 1):
        ref_num = ref['number']
        ref_text = ref['text']
        
        print(f"\nSearching {i}/{len(references)}: Reference {ref_num}")
        
        citations = search_reference_comprehensive(content, ref_num, ref_text)
        
        if citations:
            print(f"  Found {len(citations)} citations")
            total_citations += len(citations)
        
        all_results.append({
            'reference_number': ref_num,
            'reference_text': ref_text,
            'citations_found': len(citations),
            'citations': citations
        })
        
        # Show progress
        if i % 25 == 0:
            print(f"\nProgress: {i}/{len(references)} references, {total_citations} citations found")
    
    print(f"\nSEARCH COMPLETE: Found {total_citations} total citations")
    return all_results

def save_comprehensive_results(results, output_dir, references_count):
    """Save comprehensive results to CSV and JSON."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save CSV with all citation instances
    csv_filename = f"FINAL_comprehensive_citation_mapping_{timestamp}.csv"
    csv_filepath = os.path.join(output_dir, csv_filename)
    
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Reference_Number', 'Reference_Text', 'Citation_Count', 'Context'])
        
        for result in results:
            if result['citations_found'] > 0:
                ref_num = result['reference_number']
                ref_text = result['reference_text']
                
                for citation in result['citations']:
                    writer.writerow([
                        ref_num,
                        ref_text,
                        result['citations_found'],
                        citation['context']
                    ])
    
    # Save detailed analysis report
    report_filename = f"FINAL_citation_analysis_report_{timestamp}.md"
    report_filepath = os.path.join(output_dir, report_filename)
    
    total_citations = sum(r['citations_found'] for r in results)
    refs_with_citations = len([r for r in results if r['citations_found'] > 0])
    
    # Find most cited references
    sorted_results = sorted(results, key=lambda x: x['citations_found'], reverse=True)
    top_cited = sorted_results[:10]
    
    with open(report_filepath, 'w', encoding='utf-8') as f:
        f.write("# Final Comprehensive Citation Analysis Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Summary Statistics\n\n")
        f.write(f"- **Total References in Bibliography:** {references_count}\n")
        f.write(f"- **Total Citation Instances Found:** {total_citations}\n")
        f.write(f"- **References with Citations:** {refs_with_citations}\n")
        f.write(f"- **Coverage:** {refs_with_citations/references_count*100:.1f}%\n\n")
        
        f.write("## Top 10 Most Cited References\n\n")
        for i, result in enumerate(top_cited, 1):
            if result['citations_found'] > 0:
                f.write(f"{i}. **Reference {result['reference_number']}** ({result['citations_found']} citations)\n")
                f.write(f"   {result['reference_text'][:200]}...\n\n")
        
        f.write("## Citation Distribution\n\n")
        citation_counts = {}
        for result in results:
            count = result['citations_found']
            if count > 0:
                citation_counts[count] = citation_counts.get(count, 0) + 1
        
        for count in sorted(citation_counts.keys(), reverse=True):
            f.write(f"- {citation_counts[count]} references cited {count} time(s)\n")
    
    print(f"\nFINAL RESULTS SAVED:")
    print(f"  CSV mapping: {csv_filepath}")
    print(f"  Analysis report: {report_filepath}")
    
    return csv_filepath, report_filepath

def main():
    """Main execution function."""
    # File paths
    paper_file = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output/paperFull.md"
    output_dir = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output"
    
    print("="*80)
    print("FINAL COMPREHENSIVE CITATION MAPPING")
    print("="*80)
    
    # Step 1: Extract all references
    print("\nSTEP 1: Extracting all references...")
    references = extract_all_references(paper_file)
    
    if not references:
        print("ERROR: No references found!")
        return
    
    # Save references list
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(output_dir, f"all_references_{timestamp}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'extraction_date': datetime.now().isoformat(),
            'total_references': len(references),
            'references': references
        }, f, indent=2, ensure_ascii=False)
    
    print(f"References saved to: {json_path}")
    
    # Step 2: Search for all citations
    print("\nSTEP 2: Searching for all citations...")
    search_results = search_all_references(paper_file, references)
    
    # Step 3: Save comprehensive results
    print("\nSTEP 3: Saving comprehensive results...")
    csv_path, report_path = save_comprehensive_results(search_results, output_dir, len(references))
    
    # Final summary
    total_citations = sum(r['citations_found'] for r in search_results)
    refs_with_citations = len([r for r in search_results if r['citations_found'] > 0])
    
    print(f"\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"References extracted: {len(references)}")
    print(f"Citations found: {total_citations}")
    print(f"References with citations: {refs_with_citations} ({refs_with_citations/len(references)*100:.1f}%)")
    print("="*80)

if __name__ == "__main__":
    main()