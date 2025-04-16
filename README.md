# Document Parser

A modular, production-grade tool for parsing PDF documents and converting them to structured JSON with confidence scores.

## Features

- **Multi-Parser Approach**: Uses three different parsing methods (Mistral OCR, Docling, PyMuPDF) to extract text from PDFs
- **Dynamic Schema Generation**: Creates custom JSON schemas tailored to each document's specific structure
- **Confidence Scoring**: Provides confidence scores for each extracted field based on parser agreement
- **Structured JSON Output**: Generates clean, well-structured JSON that accurately represents the document
- **Modular Architecture**: Easily extensible with new parsers or processors
- **Production-Ready**: Includes error handling, retry mechanisms, and comprehensive logging
- **Command-Line Interface**: Simple CLI for processing single files or entire directories
- **Python API**: Can be used as a library in other Python applications

## Installation

### Prerequisites

- Python 3.8 or higher
- Mistral API key
- Gemini API key

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
```

Alternatively, you can set these as environment variables or pass them directly to the API.

## Usage

### Command-Line Interface

Process a single PDF file:

```bash
document-parser path/to/your/file.pdf
```

Process all PDFs in a directory:

```bash
document-parser path/to/your/pdf/directory
```

With custom output directory:

```bash
document-parser path/to/your/pdf/directory --output-dir custom_output
```

Process only the first 5 PDFs in a directory:

```bash
document-parser path/to/your/pdf/directory --limit 5
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

# Process all PDFs in a directory
processor.process_directory("path/to/your/pdf/directory")

# Process with a limit
processor.process_directory("path/to/your/pdf/directory", limit=5)
```

## Output Structure

The tool creates the following directory structure for outputs:

```
output_dir/
├── raw_outputs/         # Raw parser outputs
│   ├── filename_mistral_ocr.md
│   ├── filename_docling.md
│   └── filename_pymupdf.md
├── confidence_scores/   # Confidence score JSONs
│   └── filename_confidence.json
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

1. **Parsers**: Extract text from PDF documents
   - `MistralParser`: Uses Mistral OCR
   - `DoclingParser`: Uses Docling
   - `PyMuPDFParser`: Uses PyMuPDF

2. **Processors**: Process the extracted text
   - `GeminiProcessor`: Uses Gemini to generate JSON schema, confidence scores, and final JSON

3. **Document Processor**: Orchestrates the parsing and processing workflow

4. **Utilities**: Helper functions for file operations, JSON cleaning, etc.

5. **Configuration**: Prompt templates and other configuration

## Extending the Tool

### Adding a New Parser

1. Create a new parser class in the `src/parsers` directory
2. Implement the `parse` method that takes a PDF path and returns extracted text
3. Update the `DocumentProcessor` class to use your new parser

### Adding a New Processor

1. Create a new processor class in the `src/processors` directory
2. Implement the required methods for your processor
3. Update the `DocumentProcessor` class to use your new processor