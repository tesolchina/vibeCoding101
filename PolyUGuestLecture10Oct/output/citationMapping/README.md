# Citation Mapping Files Organization

**Created**: October 4, 2025  
**Project**: Academic Paper Citation Mapping  
**User**: Dr. Simon Wang, Hong Kong Baptist University

---

## Folder Contents Summary

This folder contains all files related to the citation mapping project for the academic paper "Natural Language Processing: State of the Art, Current Trends and Challenges" (Khurana et al. 2022).

### 📊 Final Results (Most Important)

#### Primary Outputs
- **`FINAL_comprehensive_citation_mapping_20251004_152240.csv`** (55KB)
  - **THE MAIN RESULT**: 87 citation instances with full context
  - Each row shows: Reference_Number, Reference_Text, Citation_Count, Context
  - Ready for analysis and research use

- **`FINAL_citation_analysis_report_20251004_152240.md`** (2KB)
  - Statistical summary and top 10 most cited references
  - Coverage analysis: 71/152 references cited (46.7%)
  - Reference 1 (Ahonen et al.) most cited with 9 instances

#### Reference Database
- **`all_references_20251004_152239.json`** (42KB)
  - Complete database of 152 extracted references
  - Structured format with number, text, and type for each reference

### 📈 Evolution and Iterations

#### Early Attempts (Learning Phase)
- `citation_mapping_*.csv` - Initial mapping attempts (25-60 citations)
- `citation_summary_*.md` - Early analysis reports
- Shows progression from basic to comprehensive approach

#### Comprehensive Development
- `comprehensive_citations_*.csv` - Improved extraction results
- `complete_citation_*.csv` - Further refinements
- `all_references_*.json` - Reference database versions

### 🔄 Process Iterations

The files show the evolution of our approach:

1. **Initial Basic Matching** → Found ~25 citations
2. **Improved Patterns** → Found ~60 citations  
3. **Individual Reference Search** → Found 87 citations
4. **Spaced Format Discovery** → Extracted 152 references

### 📋 File Naming Convention

- **Timestamp Format**: `YYYYMMDD_HHMMSS`
- **Prefixes**:
  - `FINAL_*` - Final production results
  - `all_references_*` - Reference extraction outputs
  - `citation_mapping_*` - Early mapping attempts
  - `comprehensive_*` - Improved comprehensive results
  - `complete_*` - Near-final comprehensive results

### 🎯 Key Technical Discoveries

1. **Citation Format**: References use spaced numbers (e.g., `[ 6 8 ]` not `[68]`)
2. **Reference Format**: Bibliography uses spaced numbers (e.g., `## 1 0.` for ref 10)
3. **Individual Search**: Searching each reference individually was more effective than bulk extraction
4. **Pattern Matching**: Required multiple citation patterns for comprehensive coverage

### 📊 Final Statistics

- **Total References in Bibliography**: 152 (target was 160)
- **Total Citation Instances Found**: 87
- **References with Citations**: 71
- **Coverage Rate**: 46.7%
- **Most Cited**: Reference 1 (Ahonen et al.) with 9 citations

### 🔍 For Further Analysis

The main files you'll want to use:
1. **For citation analysis**: `FINAL_comprehensive_citation_mapping_20251004_152240.csv`
2. **For statistics**: `FINAL_citation_analysis_report_20251004_152240.md`
3. **For reference database**: `all_references_20251004_152239.json`

### 📝 Documentation

- **Process Log**: Available in `/Plan&test/citeMappinglog.md`
- **Chat History**: Available in `/chatHistory/chat_citation_map.md`
- **Scripts Used**: Available in `/Scripts/` directory

---

*This organization provides a complete archive of the citation mapping project, from initial attempts to final comprehensive results.*