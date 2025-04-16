"""
PyMuPDF parser module for extracting text from PDF documents
"""

import pymupdf4llm


class PyMuPDFParser:
    """
    Parser that uses PyMuPDF to extract text from PDF documents
    """
    
    def parse(self, pdf_path: str) -> str:
        """
        Parse a PDF document using PyMuPDF
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text in markdown format
        """
        print(f"Parsing with PyMuPDF: {pdf_path}")
        
        try:
            md_text = pymupdf4llm.to_markdown(pdf_path)
            return md_text
        except Exception as e:
            print(f"Error parsing with PyMuPDF: {e}")
            return "Error parsing with PyMuPDF"
