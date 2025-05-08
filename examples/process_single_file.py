#!/usr/bin/env python3
"""
Example script for processing a single PDF or DOCX file
"""

import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.document_processor import DocumentProcessor


def main():
    """Process a single PDF or DOCX file"""
    # Load environment variables from .env file
    load_dotenv()

    # Path to the file
    file_path = "path/to/your/file.pdf"  # or "path/to/your/file.docx"

    # Create document processor
    processor = DocumentProcessor(output_dir="example_output")

    # Process the file based on its extension
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == '.pdf':
        processor.process_pdf(file_path)
    elif file_extension == '.docx':
        processor.process_docx(file_path)
    else:
        print(f"Error: Unsupported file type: {file_extension}")


if __name__ == "__main__":
    main()
