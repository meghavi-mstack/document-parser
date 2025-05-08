# Document Parser

A modular, production-grade tool for parsing PDF and DOCX documents and converting them to structured JSON with confidence scores. Includes a beautiful Streamlit UI for easy interaction.

## Features

- **Multi-Parser Approach**: Uses three different parsing methods (Mistral OCR, Docling, PyMuPDF) to extract text from PDFs and Mammoth for DOCX files
- **Dynamic Schema Generation**: Creates custom JSON schemas tailored to each document's specific structure
- **Confidence Scoring**: Provides confidence scores for each extracted field based on parser agreement
- **Structured JSON Output**: Generates clean, well-structured JSON that accurately represents the document
- **Modular Architecture**: Easily extensible with new parsers or processors
- **Production-Ready**: Includes error handling, retry mechanisms, and comprehensive logging
- **Command-Line Interface**: Simple CLI for processing single files or entire directories
- **Python API**: Can be used as a library in other Python applications
- **Beautiful UI**: Streamlit-based user interface for easy document processing and visualization

## Installation

### Prerequisites

- Python 3.8 or higher
- Mistral API key
- Gemini API key
- Streamlit 1.0.0 or higher (for the UI)
- Mammoth 1.9.0 or higher (for DOCX processing)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/document-parser.git
cd document-parser

# Install the package
pip install -e .
```

### Environment Setup

Create a `.env` file in the root directory with your API keys:

```
MISTRAL_API_KEY=your_mistral_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Multiple Gemini API keys for rotation (to handle quota limits)
GEMINI_API_KEY1=your_first_gemini_api_key
GEMINI_API_KEY2=your_second_gemini_api_key
# ... up to GEMINI_API_KEY10
```

Alternatively, you can set these as environment variables or pass them directly to the API.

## Usage

### Streamlit UI

The easiest way to use the Document Parser is through the Streamlit UI:

```bash
streamlit run run_ui.py
```

This will open a web interface where you can:

1. Upload PDF or DOCX documents for processing
2. View the original document and parsed JSON side by side
3. Search through the JSON data
4. Navigate multi-page PDFs or view DOCX content
5. Download the parsed JSON
6. View previously processed documents

### Command-Line Interface

Process a single document file:

```bash
document-parser path/to/your/file.pdf
# or
document-parser path/to/your/file.docx
```

Process all PDF and DOCX files in a directory:

```bash
document-parser path/to/your/document/directory
```

With custom output directory:

```bash
document-parser path/to/your/pdf/directory --output-dir custom_output
```

Process only the first 5 documents in a directory:

```bash
document-parser path/to/your/document/directory --limit 5
```

Specify API keys directly:

```bash
document-parser path/to/your/file.pdf --mistral-api-key YOUR_KEY --gemini-api-key YOUR_KEY
```

### Python API

```python
from document_parser.src.document_processor import DocumentProcessor

# Create a document processor
processor = DocumentProcessor(
    mistral_api_key="your_mistral_api_key",  # Optional, defaults to env var
    gemini_api_key="your_gemini_api_key",    # Optional, defaults to env var
    output_dir="parsed_outputs"              # Optional, defaults to "parsed_outputs"
)

# Process a single PDF file
processor.process_pdf("path/to/your/file.pdf")

# Process a single DOCX file
processor.process_docx("path/to/your/file.docx")

# Process all PDF and DOCX files in a directory
processor.process_directory("path/to/your/document/directory")

# Process with a limit
processor.process_directory("path/to/your/document/directory", limit=5)
```

## Output Structure

The tool creates the following directory structure for outputs:

```
output_dir/
├── raw_outputs/         # Raw parser outputs
│   ├── filename_mistral_ocr.md  # For PDF files
│   ├── filename_docling.md      # For PDF files
│   ├── filename_pymupdf.md      # For PDF files
│   ├── filename_html.html       # For DOCX files
│   └── filename_text.md         # For DOCX files
├── confidence_scores/   # Confidence score JSONs
│   └── filename_confidence.json
├── pdf_copies/          # Copies of processed PDF files
│   └── filename.pdf
├── docx_copies/         # Copies of processed DOCX files
│   └── filename.docx
└── json_outputs/        # Final structured JSONs
    └── filename.json
```

### Confidence Scores

Confidence scores range from 0.0 to 1.0 for each field:

- **1.0**: Field value appears consistently across all three parsing methods
- **0.8**: Field value appears in two parsing methods
- **0.6**: Field value appears in only one parsing method but is clearly correct
- **0.4**: Field value is present but with potential inconsistencies
- **0.2**: Field value is uncertain or potentially incorrect
- **0.0**: Field value is missing or completely uncertain

## Architecture

The document parser follows a modular architecture:

1. **Parsers**: Extract text from documents
   - `MistralParser`: Uses Mistral OCR for PDFs
   - `DoclingParser`: Uses Docling for PDFs
   - `PyMuPDFParser`: Uses PyMuPDF for PDFs
   - `DocxParser`: Uses Mammoth for DOCX files

2. **Processors**: Process the extracted text
   - `GeminiProcessor`: Uses Gemini to generate JSON schema, confidence scores, and final JSON

3. **Document Processor**: Orchestrates the parsing and processing workflow

4. **Utilities**: Helper functions for file operations, JSON cleaning, etc.

5. **Configuration**: Prompt templates and other configuration

6. **User Interface**: Streamlit-based UI for easy interaction
   - PDF viewer with navigation controls
   - DOCX viewer for Word documents
   - Interactive JSON viewer with search functionality
   - Upload and processing interface for both PDF and DOCX files

## Extending the Tool

### Adding a New Parser

1. Create a new parser class in the `src/parsers` directory
2. Implement the `parse` method that takes a document path and returns extracted text
3. Update the `DocumentProcessor` class to use your new parser

### Adding a New Processor

1. Create a new processor class in the `src/processors` directory
2. Implement the required methods for your processor
3. Update the `DocumentProcessor` class to use your new processor

### Extending the UI

The UI follows a modular architecture in the `src/ui` directory:

```
src/ui/
├── __init__.py           # Main UI module with the run_app function
├── styles.py             # CSS styles for the UI
├── components/           # UI components
│   ├── __init__.py
│   ├── pdf_viewer.py     # PDF viewer component
│   ├── docx_viewer.py    # DOCX viewer component
│   └── json_viewer.py    # JSON viewer component
└── utils/                # Utility functions
    ├── __init__.py
    └── processor.py      # Document processing utilities
```

To extend the UI:

1. Add new components in the `src/ui/components` directory
2. Add new utility functions in the `src/ui/utils` directory
3. Update the main UI module in `src/ui/__init__.py`