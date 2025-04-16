"""
Docling parser module for extracting text from PDF documents
"""

import ssl
from docling.document_converter import DocumentConverter


class DoclingParser:
    """
    Parser that uses Docling to extract text from PDF documents
    """
    
    def __init__(self):
        """
        Initialize the Docling parser
        """
        # Ensure SSL context is properly set for Docling
        ssl._create_default_https_context = ssl._create_unverified_context
    
    def parse(self, pdf_path: str) -> str:
        """
        Parse a PDF document using Docling
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text in markdown format
        """
        print(f"Parsing with Docling: {pdf_path}")
        
        try:
            converter = DocumentConverter()
            result = converter.convert(pdf_path)
            docling_md = result.document.export_to_markdown()
            return docling_md
        except Exception as e:
            print(f"Error parsing with Docling: {e}")
            return "Error parsing with Docling"
