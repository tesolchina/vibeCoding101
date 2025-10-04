#!/usr/bin/env python3
"""
Citation Mapping Script

This script analyzes a markdown paper file to map in-text citations to their full references
and generates a CSV file showing where each citation appears in the document.

Author: Simon Wang
Date: 2025-10-04
"""

import re
import csv
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/Plan&test/citeMappinglog.md'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class CitationMapper:
    def __init__(self, input_file: str, output_dir: str):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.citations = {}  # {citation_key: {ref_number, full_reference, paragraphs}}
        self.references = {}  # {ref_number: full_reference}
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized CitationMapper for {input_file}")
        logger.info(f"Output directory: {output_dir}")
    
    def read_paper(self) -> str:
        """Read the markdown paper file"""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"Successfully read paper file: {self.input_file}")
            logger.info(f"File size: {len(content)} characters")
            return content
        except Exception as e:
            logger.error(f"Error reading file {self.input_file}: {e}")
            raise
    
    def extract_references(self, content: str) -> Dict[str, str]:
        """Extract all references from the References section"""
        references = {}
        
        # Find the references section - look for numbered references
        # Pattern to match references like "## 66. Author (Year) Title..." or "## 6 6. Author..."
        ref_patterns = [
            r'^##\s*(\d+)\.\s*(.+?)(?=^##\s*\d+\.|$)',  # ## 66. format
            r'^##\s*(\d+)\s+(\d+)\.\s*(.+?)(?=^##\s*\d+\s+\d+\.|$)',  # ## 6 6. format
        ]
        
        for pattern in ref_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            
            for match in matches:
                if len(match) == 2:  # Single number format
                    ref_num, ref_text = match
                else:  # Split number format
                    ref_num1, ref_num2, ref_text = match
                    ref_num = ref_num1 + ref_num2
                
                # Clean up the reference text
                ref_text = re.sub(r'\s+', ' ', ref_text.strip())
                # Remove any trailing page numbers or publication info
                ref_text = re.sub(r'\n.*$', '', ref_text)
                references[ref_num] = ref_text
            
        logger.info(f"Extracted {len(references)} references")
        
        # Log a few examples for debugging
        for i, (ref_num, ref_text) in enumerate(list(references.items())[:5]):
            logger.debug(f"Reference {ref_num}: {ref_text[:100]}...")
            
        return references
    
    def extract_in_text_citations(self, content: str) -> List[Tuple[str, str, str]]:
        """
        Extract in-text citations and their context
        Returns list of (citation_key, reference_number, paragraph_context)
        """
        citations = []
        
        # Split content into paragraphs
        paragraphs = content.split('\n\n')
        
        # Multiple patterns to match different citation formats
        patterns = [
            # Pattern 1: "(Author et al., Year) [ number ]"
            r'\(([^)]+)\)\s*\[\s*(\d+)\s*\]',
            # Pattern 2: "Author Year [ number ]" (with spaces in year)
            r'([A-Z]\w+(?:\s+et\s+al\.?)?\s*\d{1,2}\s*\d{2})\s*\[\s*(\d+)\s*\]',
            # Pattern 3: Citations at end of sentences like "[ number ]"
            r'([^.!?]+)\[\s*(\d+)\s*\]',
            # Pattern 4: Multiple citations like "[ num1 , num2 , num3 ]"
            r'\[\s*(\d+(?:\s*,\s*\d+)*)\s*\]',
            # Pattern 5: Range citations like "[ num1 – num2 ]"
            r'\[\s*(\d+\s*[–-]\s*\d+)\s*\]'
        ]
        
        for para_idx, paragraph in enumerate(paragraphs):
            # Skip empty paragraphs and headers
            if not paragraph.strip() or paragraph.startswith('#'):
                continue
                
            # Try each pattern
            for pattern_idx, pattern in enumerate(patterns):
                matches = re.finditer(pattern, paragraph)
                
                for match in matches:
                    citation_key = None
                    ref_number = None
                    
                    if pattern_idx == 0:  # (Author, Year) format
                        citation_key = match.group(1).strip()
                        ref_number = match.group(2)
                        
                    elif pattern_idx == 1:  # Author Year format
                        citation_key = match.group(1).strip()
                        ref_number = match.group(2)
                        
                    elif pattern_idx == 2:  # End of sentence citations
                        # Extract the last few words before the citation
                        text_before = match.group(1).strip()
                        words = text_before.split()
                        if len(words) >= 2:
                            citation_key = ' '.join(words[-2:])  # Last 2 words
                        else:
                            citation_key = text_before[-50:] if len(text_before) > 50 else text_before
                        ref_number = match.group(2)
                        
                    elif pattern_idx == 3:  # Multiple citations
                        ref_numbers = re.findall(r'\d+', match.group(1))
                        for ref_num in ref_numbers:
                            citations.append((f"Ref_{ref_num}", ref_num, paragraph[:300] + "..." if len(paragraph) > 300 else paragraph))
                        continue
                        
                    elif pattern_idx == 4:  # Range citations
                        range_match = re.search(r'(\d+)\s*[–-]\s*(\d+)', match.group(1))
                        if range_match:
                            start_ref = int(range_match.group(1))
                            end_ref = int(range_match.group(2))
                            for ref_num in range(start_ref, end_ref + 1):
                                citations.append((f"Ref_{ref_num}", str(ref_num), paragraph[:300] + "..." if len(paragraph) > 300 else paragraph))
                        continue
                    
                    # Only process if we have valid citation_key and ref_number
                    if citation_key is not None and ref_number is not None:
                        # Clean up citation key
                        citation_key = re.sub(r'\s+', ' ', citation_key.strip())
                        
                        # Get some context around the citation
                        context = paragraph[:300] + "..." if len(paragraph) > 300 else paragraph
                        context = re.sub(r'\s+', ' ', context.strip())
                        
                        citations.append((citation_key, ref_number, context))
                        logger.debug(f"Found citation: {citation_key} -> [{ref_number}] in paragraph {para_idx}")
        
        logger.info(f"Extracted {len(citations)} total citations")
        return citations
    
    def map_citations_to_references(self, citations: List[Tuple[str, str, str]], references: Dict[str, str]):
        """Map citations to their full references and organize by citation"""
        citation_map = {}
        
        for citation_key, ref_number, context in citations:
            if ref_number in references:
                full_ref = references[ref_number]
                
                if citation_key not in citation_map:
                    citation_map[citation_key] = {
                        'reference_number': ref_number,
                        'full_reference': full_ref,
                        'contexts': []
                    }
                
                citation_map[citation_key]['contexts'].append(context)
            else:
                logger.warning(f"Reference number {ref_number} not found for citation {citation_key}")
        
        logger.info(f"Mapped {len(citation_map)} unique citations")
        return citation_map
    
    def generate_csv(self, citation_map: Dict):
        """Generate CSV file with citation mappings"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_file = self.output_dir / f'citation_mapping_{timestamp}.csv'
        
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    'Citation_Key',
                    'Reference_Number', 
                    'Full_Reference',
                    'Number_of_Occurrences',
                    'Context_1',
                    'Context_2', 
                    'Context_3',
                    'Additional_Contexts'
                ])
                
                # Write data
                for citation_key, data in sorted(citation_map.items()):
                    contexts = data['contexts']
                    row = [
                        citation_key,
                        data['reference_number'],
                        data['full_reference'],
                        len(contexts)
                    ]
                    
                    # Add up to 3 contexts in separate columns
                    for i in range(3):
                        if i < len(contexts):
                            row.append(contexts[i])
                        else:
                            row.append('')
                    
                    # If more than 3 contexts, combine the rest
                    if len(contexts) > 3:
                        additional = ' | '.join(contexts[3:])
                        row.append(additional)
                    else:
                        row.append('')
                    
                    writer.writerow(row)
            
            logger.info(f"Generated CSV file: {csv_file}")
            return csv_file
            
        except Exception as e:
            logger.error(f"Error generating CSV: {e}")
            raise
    
    def generate_summary_report(self, citation_map: Dict, csv_file: Path):
        """Generate a summary report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.output_dir / f'citation_summary_{timestamp}.md'
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("# Citation Mapping Summary Report\n\n")
                f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Source file:** {self.input_file}\n")
                f.write(f"**CSV output:** {csv_file}\n\n")
                
                f.write("## Statistics\n\n")
                f.write(f"- Total unique citations: {len(citation_map)}\n")
                
                total_occurrences = sum(len(data['contexts']) for data in citation_map.values())
                f.write(f"- Total citation occurrences: {total_occurrences}\n")
                
                # Most cited references
                sorted_citations = sorted(citation_map.items(), 
                                        key=lambda x: len(x[1]['contexts']), 
                                        reverse=True)
                
                f.write("\n## Most Frequently Cited (Top 10)\n\n")
                for i, (citation_key, data) in enumerate(sorted_citations[:10]):
                    f.write(f"{i+1}. **{citation_key}** - {len(data['contexts'])} occurrences\n")
                    f.write(f"   - Reference #{data['reference_number']}: {data['full_reference'][:100]}...\n\n")
                
                f.write("\n## All Citations (Alphabetical)\n\n")
                for citation_key, data in sorted(citation_map.items()):
                    f.write(f"### {citation_key}\n")
                    f.write(f"- **Reference #{data['reference_number']}**\n")
                    f.write(f"- **Full Reference:** {data['full_reference']}\n")
                    f.write(f"- **Occurrences:** {len(data['contexts'])}\n\n")
            
            logger.info(f"Generated summary report: {report_file}")
            return report_file
            
        except Exception as e:
            logger.error(f"Error generating summary report: {e}")
            raise
    
    def process(self):
        """Main processing function"""
        logger.info("Starting citation mapping process...")
        
        try:
            # Read the paper
            content = self.read_paper()
            
            # Extract references
            references = self.extract_references(content)
            
            # Extract in-text citations
            citations = self.extract_in_text_citations(content)
            
            # Map citations to references
            citation_map = self.map_citations_to_references(citations, references)
            
            # Generate outputs
            csv_file = self.generate_csv(citation_map)
            report_file = self.generate_summary_report(citation_map, csv_file)
            
            logger.info("Citation mapping process completed successfully!")
            logger.info(f"Output files generated:")
            logger.info(f"  - CSV: {csv_file}")
            logger.info(f"  - Summary: {report_file}")
            
            return csv_file, report_file
            
        except Exception as e:
            logger.error(f"Error in citation mapping process: {e}")
            raise

def main():
    """Main function"""
    input_file = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output/paperFull.md"
    output_dir = "/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/OneDriveCursor/vibeCoding101/vibeCoding101/PolyUGuestLecture10Oct/output"
    
    mapper = CitationMapper(input_file, output_dir)
    csv_file, report_file = mapper.process()
    
    print(f"\n✅ Citation mapping completed!")
    print(f"📊 CSV file: {csv_file}")
    print(f"📋 Summary report: {report_file}")

if __name__ == "__main__":
    main()