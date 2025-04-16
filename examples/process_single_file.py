#!/usr/bin/env python3
"""
Example script for processing a single PDF file
"""

import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.document_processor import DocumentProcessor


def main():
    """Process a single PDF file"""
    # Load environment variables from .env file
    load_dotenv()
    
    # Path to the PDF file
    pdf_path = "path/to/your/file.pdf"
    
    # Create document processor
    processor = DocumentProcessor(output_dir="example_output")
    
    # Process the PDF file
    processor.process_pdf(pdf_path)


if __name__ == "__main__":
    main()
