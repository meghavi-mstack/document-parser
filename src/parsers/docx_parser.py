"""
DOCX parser module for extracting text from DOCX documents
"""

import mammoth
import os
from typing import Tuple


class DocxParser:
    """
    Parser that uses mammoth to extract HTML from DOCX documents
    """
    
    def parse(self, docx_path: str) -> Tuple[str, str]:
        """
        Parse a DOCX document using mammoth
        
        Args:
            docx_path: Path to the DOCX file
            
        Returns:
            Tuple containing:
                - Extracted HTML content
                - Plain text content (as a fallback)
        """
        print(f"Parsing with Mammoth: {docx_path}")
        
        try:
            # Check if file exists
            if not os.path.exists(docx_path):
                raise FileNotFoundError(f"File not found: {docx_path}")
            
            # Convert DOCX to HTML
            with open(docx_path, 'rb') as docx_file:
                result = mammoth.convert_to_html(docx_file)
                html = result.value
                
                # Also extract plain text as a fallback
                text_result = mammoth.extract_raw_text(docx_file)
                text = text_result.value
                
                return html, text
                
        except Exception as e:
            print(f"Error parsing with Mammoth: {e}")
            return f"<p>Error parsing with Mammoth: {str(e)}</p>", f"Error parsing with Mammoth: {str(e)}"
