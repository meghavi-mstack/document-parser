"""
Document processor utilities for the Document Parser UI.

This module provides utilities for processing documents.
"""

import os
import json
import tempfile
from pathlib import Path
from typing import Dict, Optional, Tuple

from src.document_processor import DocumentProcessor


def create_document_processor() -> DocumentProcessor:
    """
    Create and return a document processor instance.

    Returns:
        DocumentProcessor: An instance of the document processor
    """
    processor = DocumentProcessor(
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        output_dir="parsed_outputs"
    )

    # Create a directory for PDF copies if it doesn't exist
    pdf_dir = os.path.join(processor.output_dir, "pdf_copies")
    os.makedirs(pdf_dir, exist_ok=True)

    return processor


def process_uploaded_file(uploaded_file) -> Tuple[bool, str, Optional[Dict]]:
    """
    Process an uploaded file (PDF or DOCX) and return the results.

    Args:
        uploaded_file: The uploaded file from Streamlit

    Returns:
        Tuple containing:
            - Success flag (bool)
            - File path or error message (str)
            - Parsed JSON data (Dict or None if failed)
    """
    # Determine file type from the uploaded file's name
    file_extension = Path(uploaded_file.name).suffix.lower()

    # Create a temporary file to save the uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    try:
        # Create document processor
        processor = create_document_processor()

        # Get base filename without extension
        base_filename = Path(tmp_path).stem

        # Process based on file type
        if file_extension == '.pdf':
            # Save a copy of the PDF for future reference
            pdf_copy_dir = os.path.join(processor.output_dir, "pdf_copies")
            pdf_copy_path = os.path.join(pdf_copy_dir, f"{base_filename}.pdf")

            with open(tmp_path, 'rb') as src_file, open(pdf_copy_path, 'wb') as dst_file:
                dst_file.write(src_file.read())

            # Process the PDF file
            success = processor.process_pdf(tmp_path)
        elif file_extension == '.docx':
            # Save a copy of the DOCX for future reference
            docx_copy_dir = os.path.join(processor.output_dir, "docx_copies")
            docx_copy_path = os.path.join(docx_copy_dir, f"{base_filename}.docx")

            with open(tmp_path, 'rb') as src_file, open(docx_copy_path, 'wb') as dst_file:
                dst_file.write(src_file.read())

            # Process the DOCX file
            success = processor.process_docx(tmp_path)
        else:
            return False, f"Unsupported file type: {file_extension}", None

        if success:
            # Path to the generated JSON file
            json_path = os.path.join(processor.output_dir, "json_outputs", f"{base_filename}.json")

            # Add debug information
            print(f"Looking for JSON file at: {json_path}")
            print(f"Original uploaded filename: {uploaded_file.name}")
            print(f"Temporary file path: {tmp_path}")

            # Check if the JSON file exists
            if os.path.exists(json_path):
                # Load the JSON data
                with open(json_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)

                return True, tmp_path, json_data
            else:
                # List files in the output directory to help debug
                json_dir = os.path.join(processor.output_dir, "json_outputs")
                if os.path.exists(json_dir):
                    print(f"Files in {json_dir}:")
                    for file in os.listdir(json_dir):
                        print(f"  - {file}")

                return False, f"JSON file not found: {json_path}", None
        else:
            return False, f"Failed to process the {file_extension} file", None

    except Exception as e:
        return False, f"Error processing file: {str(e)}", None


def load_existing_json(json_path: str) -> Dict:
    """
    Load an existing JSON file.

    Args:
        json_path: Path to the JSON file

    Returns:
        The loaded JSON data
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {str(e)}")
        return None
