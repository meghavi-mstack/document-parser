"""
Mistral OCR parser module for extracting text from PDF documents
"""

import os
from typing import Tuple
from mistralai import Mistral


class MistralParser:
    """
    Parser that uses Mistral OCR to extract text from PDF documents
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Mistral parser
        
        Args:
            api_key: Mistral API key (defaults to MISTRAL_API_KEY environment variable)
        """
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("Mistral API key is required. Set MISTRAL_API_KEY environment variable or pass it directly.")
        
        self.client = Mistral(api_key=self.api_key)
    
    def parse(self, pdf_path: str) -> Tuple[str, str]:
        """
        Parse a PDF document using Mistral OCR
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple containing:
                - Extracted text in markdown format
                - Signed URL for the document
        """
        print(f"Parsing with Mistral OCR: {pdf_path}")
        
        # Upload the file to Mistral for OCR processing
        with open(pdf_path, "rb") as file:
            uploaded_pdf = self.client.files.upload(
                file={"file_name": os.path.basename(pdf_path), "content": file},
                purpose="ocr"
            )

        # Get the signed URL to allow secure processing
        signed_url = self.client.files.get_signed_url(file_id=uploaded_pdf.id)

        # Process OCR on the document using the signed URL
        ocr_response = self.client.ocr.process(
            model="mistral-ocr-latest",
            document={"type": "document_url", "document_url": signed_url.url},
        )

        # Combine all pages into a single markdown string
        mistral_md = ""
        for page in ocr_response.pages:
            mistral_md += page.markdown + "\n\n"
        
        return mistral_md, signed_url.url
