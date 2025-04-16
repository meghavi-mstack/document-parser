#!/usr/bin/env python3
"""
Example script for processing a directory of PDF files
"""

import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.document_processor import DocumentProcessor


def main():
    """Process a directory of PDF files"""
    # Load environment variables from .env file
    load_dotenv()
    
    # Path to the directory containing PDF files
    pdf_dir = "path/to/your/pdf/directory"
    
    # Create document processor
    processor = DocumentProcessor(output_dir="example_output")
    
    # Process all PDF files in the directory (limit to 5 files for this example)
    processor.process_directory(pdf_dir, limit=5)


if __name__ == "__main__":
    main()
