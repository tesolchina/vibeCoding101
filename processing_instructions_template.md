# AI Agent Processing Instructions Template

## File Processing Instructions

### Input File
- **File Path**: `data/2SeptWeek1lecture.vtt`
- **File Type**: WebVTT (Video Text Track) format
- **Content**: Lecture transcript with timestamps

### Processing Steps
1. **Clean VTT Formatting**
   - Remove timestamp markers (e.g., `00:00:00.000 --> 00:00:05.000`)
   - Remove VTT header and metadata
   - Extract only the spoken text content

2. **Text Processing**
   - Remove speaker identification if present
   - Clean up formatting artifacts
   - Ensure proper paragraph breaks
   - Remove any remaining technical markers

3. **Content Organization**
   - Maintain logical flow of the lecture
   - Preserve important pauses as paragraph breaks
   - Ensure readability

### Output Files
1. **Primary Output**: `cleaned_lecture.txt`
   - Clean text content without timestamps
   - Properly formatted paragraphs
   - Ready for further processing

2. **Secondary Output**: `lecture_summary.md`
   - Comprehensive summary of main topics
   - Key concepts and definitions
   - Important points for students
   - Discussion questions or topics raised

### Quality Checks
- Verify all timestamps are removed
- Ensure text flows naturally
- Check that important content is preserved
- Confirm output files are properly formatted

### Usage Instructions
1. Read this instructions file
2. Locate the input file at the specified path
3. Follow all processing steps in order
4. Create both output files as specified
5. Verify quality of outputs
6. Report completion status

---

**Note**: This template can be customized for different file types and processing needs. The AI Agent should follow these instructions precisely to ensure consistent results.
