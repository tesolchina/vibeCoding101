#!/usr/bin/env python3
"""
Comprehensive Reference Extractor and Individual Citation Searcher
================================================================

This script extracts all references from the bibliography section and then
searches for each reference individually using systematic pattern matching.

Created: 2024-10-04
Author: Citation Mapping System
"""

import re
import json
import os
from datetime import datetime

def extract_all_references(file_path):
    """Extract all references from the bibliography section."""
    references = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find the References section more precisely
        # Look for "## References" and go until "Publisher" or end of file
        references_pattern = r'## References\s*\n(.*?)(?=\nPublisher|\Z)'
        references_match = re.search(references_pattern, content, re.DOTALL)
        
        if not references_match:
            print("References section not found!")
            return references
        
        references_text = references_match.group(1)
        print(f"Found references section with {len(references_text)} characters")
        
        # Main pattern: ## number. reference_text
        # This captures everything until the next ## number. or end
        pattern = r'## (\d+)\. (.+?)(?=\n## \d+\.|\Z)'
        matches = re.findall(pattern, references_text, re.DOTALL)
        
        print(f\"Found {len(matches)} reference matches with main pattern")
        
        for match in matches:
            ref_num = int(match[0])
            ref_text = match[1].strip()
            
            # Clean up the reference text
            ref_text = re.sub(r'\s+', ' ', ref_text)  # Multiple whitespace to single space
            ref_text = ref_text.strip()
            
            references.append({
                'number': ref_num,
                'text': ref_text,
                'type': 'standard'
            })
        
        # Look for any remaining standalone references that might not have ## prefix
        # Find lines that start with just numbers
        lines = references_text.split('\\n')
        for i, line in enumerate(lines):
            # Look for lines like "56. text" or "9 1. text" (for spaced numbers)
            standalone_match = re.match(r'^(\d+(?:\s+\d+)?)\. (.+)', line.strip())
            if standalone_match:
                ref_num_str = standalone_match.group(1).replace(' ', '')
                if ref_num_str.isdigit():
                    ref_num = int(ref_num_str)
                    
                    # Skip if already found
                    if any(ref['number'] == ref_num for ref in references):
                        continue
                    
                    # Collect the full reference text (may span multiple lines)
                    ref_text = standalone_match.group(2)
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j].strip()
                        # Stop if we hit another reference or section
                        if re.match(r'^\d+(?:\s+\d+)?\.|^##|^Publisher', next_line):
                            break
                        if next_line:  # Add non-empty lines
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
        
        # Check for missing references
        if references:
            max_ref = max(ref['number'] for ref in references)
            all_numbers = set(ref['number'] for ref in references)
            missing = [i for i in range(1, max_ref + 1) if i not in all_numbers]
            
            if missing and len(missing) < 20:  # Only show if reasonable number missing
                print(f"Missing reference numbers: {missing}")
            elif missing:
                print(f"Missing {len(missing)} references from total range 1-{max_ref}")
        
        print(f"Successfully extracted {len(references)} references")
        return references
        
    except Exception as e:
        print(f"Error extracting references: {e}")
        return references

def search_reference_in_text(content, ref_num, ref_text):
    """Search for a specific reference in the text using multiple patterns."""
    citations = []
    
    # Extract key info from reference for better matching
    # Get author name(s) - usually first word(s) before date
    author_match = re.search(r'^([A-Za-z\\s,&]+?)\\s*\\([12]\\d{3}', ref_text)
    authors = author_match.group(1).strip() if author_match else ""
    
    # Get year
    year_match = re.search(r'\\((\\d{4})\\)', ref_text)
    year = year_match.group(1) if year_match else ""
    
    # Normalize the reference number for search
    ref_str = str(ref_num)
    
    # Pattern 1: Direct number in brackets [number]
    patterns = [
        f'\\[{ref_str}\\]',  # [23]
        f'\\[ {ref_str} \\]',  # [ 23 ]
    ]
    
    # Pattern 2: For numbers >=10, try spaced format
    if len(ref_str) >= 2:
        spaced = ' '.join(ref_str)  # "23" -> "2 3"
        patterns.extend([
            f'\\[ {spaced} \\]',  # [ 2 3 ]
            f'\\[{spaced}\\]',    # [2 3]
        ])
    
    # Pattern 3: Author-year combinations
    if authors and year:
        first_author = authors.split(',')[0].split('&')[0].strip()
        patterns.extend([
            f'{first_author}.*?{year}.*?\\[{ref_str}\\]',
            f'{first_author}.*?{year}.*?\\[ {ref_str} \\]',
        ])
        
        if len(ref_str) >= 2:
            spaced = ' '.join(ref_str)
            patterns.extend([
                f'{first_author}.*?{year}.*?\\[ {spaced} \\]',
                f'{first_author}.*?{year}.*?\\[{spaced}\\]',
            ])
    
    # Search for each pattern
    for pattern in patterns:
        try:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            for match in matches:
                # Get context around the match
                start = max(0, match.start() - 100)
                end = min(len(content), match.end() + 100)
                context = content[start:end].strip()
                
                # Clean up context
                context = re.sub(r'\\s+', ' ', context)
                
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
        if citation['position'] not in seen_positions:
            unique_citations.append(citation)
            seen_positions.add(citation['position'])
    
    return unique_citations

def individual_reference_search(paper_file, references_data):
    """Search for each reference individually in the paper."""
    print("\\n" + "="*80)
    print("INDIVIDUAL REFERENCE SEARCH")
    print("="*80)
    
    try:
        with open(paper_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading paper file: {e}")
        return []
    
    all_results = []
    total_citations = 0
    
    references = references_data['references'] if 'references' in references_data else references_data
    
    for i, ref in enumerate(references, 1):
        ref_num = ref['number']
        ref_text = ref['text']
        
        print(f"\\nSearching {i}/{len(references)}: Reference {ref_num}")
        print(f"Reference: {ref_text[:100]}...")
        
        citations = search_reference_in_text(content, ref_num, ref_text)
        
        if citations:
            print(f"  Found {len(citations)} citations")
            total_citations += len(citations)
        else:
            print(f"  No citations found")
        
        all_results.append({
            'reference_number': ref_num,
            'reference_text': ref_text,
            'citations_found': len(citations),
            'citations': citations
        })
        
        # Show progress every 20 references
        if i % 20 == 0:
            print(f"\\nProgress: {i}/{len(references)} references searched, {total_citations} total citations found")
    
    print(f"\\nSEARCH COMPLETE: Found {total_citations} total citations across {len(references)} references")
    return all_results

def save_results(results, output_dir, references_count):
    """Save the individual search results."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save detailed results as JSON
    json_filename = f"individual_reference_search_{timestamp}.json"
    json_filepath = os.path.join(output_dir, json_filename)
    
    summary_data = {
        'search_date': datetime.now().isoformat(),
        'total_references': references_count,
        'total_citations_found': sum(r['citations_found'] for r in results),
        'references_with_citations': len([r for r in results if r['citations_found'] > 0]),
        'results': results
    }
    
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    print(f"\\nDetailed results saved to: {json_filepath}")
    
    # Save CSV summary
    csv_filename = f"individual_search_summary_{timestamp}.csv"
    csv_filepath = os.path.join(output_dir, csv_filename)
    
    with open(csv_filepath, 'w', encoding='utf-8') as f:
        f.write("Reference_Number,Citations_Found,Reference_Text\\n")
        for result in results:
            ref_text = result['reference_text'].replace('"', '""')  # Escape quotes
            f.write(f'{result["reference_number"]},{result["citations_found"]},"{ref_text}"\\n')
    
    print(f"CSV summary saved to: {csv_filepath}")
    
    return json_filepath, csv_filepath

def main():
    """Main execution function."""
    # File paths
    paper_file = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output/paperFull.md"
    output_dir = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output"
    
    # Step 1: Extract all references
    print("STEP 1: Extracting all references from bibliography...")
    references = extract_all_references(paper_file)
    
    if not references:
        print("No references found! Cannot proceed with individual search.")
        return
    
    # Save references list
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    references_data = {
        'extraction_date': datetime.now().isoformat(),
        'total_references': len(references),
        'references': references
    }
    
    json_path = os.path.join(output_dir, f"all_references_{timestamp}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(references_data, f, indent=2, ensure_ascii=False)
    print(f"\\nReferences saved to: {json_path}")
    
    # Step 2: Search for each reference individually
    print("\\nSTEP 2: Searching for individual references in text...")
    search_results = individual_reference_search(paper_file, references_data)
    
    # Step 3: Save results
    print("\\nSTEP 3: Saving results...")
    save_results(search_results, output_dir, len(references))
    
    # Print final summary
    total_citations = sum(r['citations_found'] for r in search_results)
    refs_with_citations = len([r for r in search_results if r['citations_found'] > 0])
    
    print(f"\\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"Total references extracted: {len(references)}")
    print(f"Total citations found: {total_citations}")
    print(f"References with citations: {refs_with_citations}")
    print(f"Coverage: {refs_with_citations/len(references)*100:.1f}%")

if __name__ == "__main__":
    main()