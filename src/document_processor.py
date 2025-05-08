"""
Main document processor module
"""

import os
from typing import Dict, List, Optional, Tuple

from .parsers.mistral_parser import MistralParser
from .parsers.docling_parser import DoclingParser
from .parsers.pymupdf_parser import PyMuPDFParser
from .parsers.docx_parser import DocxParser
from .processors.gemini_processor import GeminiProcessor
from .utils.file_utils import ensure_directory


class DocumentProcessor:
    """
    Main document processor that orchestrates the parsing and processing of documents
    """

    def __init__(self,
                 mistral_api_key: Optional[str] = None,
                 gemini_api_key: Optional[str] = None,
                 output_dir: str = "parsed_outputs"):
        """
        Initialize the document processor

        Args:
            mistral_api_key: Mistral API key (defaults to MISTRAL_API_KEY environment variable)
            gemini_api_key: Gemini API key (defaults to GEMINI_API_KEY environment variable)
            output_dir: Directory to save output files
        """
        self.mistral_parser = MistralParser(api_key=mistral_api_key)
        self.docling_parser = DoclingParser()
        self.pymupdf_parser = PyMuPDFParser()
        self.docx_parser = DocxParser()
        self.gemini_processor = GeminiProcessor(api_key=gemini_api_key)
        self.output_dir = output_dir

        # Create output directories
        self._create_output_directories()

    def _create_output_directories(self) -> None:
        """Create output directories"""
        ensure_directory(self.output_dir)
        ensure_directory(os.path.join(self.output_dir, "raw_outputs"))
        ensure_directory(os.path.join(self.output_dir, "json_outputs"))
        ensure_directory(os.path.join(self.output_dir, "confidence_scores"))
        ensure_directory(os.path.join(self.output_dir, "docx_copies"))
        ensure_directory(os.path.join(self.output_dir, "pdf_copies"))

    def process_pdf(self, pdf_path: str) -> bool:
        """
        Process a single PDF file

        Args:
            pdf_path: Path to the PDF file

        Returns:
            True if processing was successful, False otherwise
        """
        # Check if file exists
        if not os.path.exists(pdf_path):
            print(f"Error: File {pdf_path} does not exist")
            return False

        # Get base filename without extension
        base_filename = os.path.splitext(os.path.basename(pdf_path))[0]

        # Define output directories
        raw_dir = os.path.join(self.output_dir, "raw_outputs")
        json_dir = os.path.join(self.output_dir, "json_outputs")
        confidence_dir = os.path.join(self.output_dir, "confidence_scores")

        # Parse PDF using multiple methods
        print(f"\nProcessing file: {pdf_path}")

        try:
            # Parse with Mistral OCR
            mistral_output, _ = self.mistral_parser.parse(pdf_path)

            # Parse with Docling
            docling_output = self.docling_parser.parse(pdf_path)

            # Parse with PyMuPDF
            pymupdf_output = self.pymupdf_parser.parse(pdf_path)

            # Save raw parsed outputs
            with open(f"{raw_dir}/{base_filename}_mistral_ocr.md", "w", encoding="utf-8") as f:
                f.write(mistral_output)

            with open(f"{raw_dir}/{base_filename}_docling.md", "w", encoding="utf-8") as f:
                f.write(docling_output)

            with open(f"{raw_dir}/{base_filename}_pymupdf.md", "w", encoding="utf-8") as f:
                f.write(pymupdf_output)

            # Combine parsed outputs
            parsed_outputs = {
                "mistral_ocr": mistral_output,
                "docling": docling_output,
                "pymupdf": pymupdf_output
            }

            # Step 1: Generate JSON schema and confidence scores
            print(f"Step 1: Generating JSON schema and confidence scores for {base_filename}...")
            schema_json, confidence_json = self.gemini_processor.generate_schema_and_confidence(parsed_outputs)

            # Save confidence scores
            with open(f"{confidence_dir}/{base_filename}_confidence.json", "w", encoding="utf-8") as f:
                f.write(confidence_json)

            # Step 2: Generate final structured JSON
            print(f"Step 2: Generating final structured JSON for {base_filename}...")
            final_json = self.gemini_processor.generate_final_json(schema_json, parsed_outputs)

            # Save final JSON output
            with open(f"{json_dir}/{base_filename}.json", "w", encoding="utf-8") as f:
                f.write(final_json)

            print(f"✓ Successfully processed: {base_filename}")
            print(f"  - Raw outputs saved to {raw_dir}/{base_filename}_*.md")
            print(f"  - Confidence scores saved to {confidence_dir}/{base_filename}_confidence.json")
            print(f"  - Final JSON output saved to {json_dir}/{base_filename}.json")
            return True

        except Exception as e:
            print(f"✗ Error processing {pdf_path}: {str(e)}")
            return False

    def process_docx(self, docx_path: str) -> bool:
        """
        Process a single DOCX file

        Args:
            docx_path: Path to the DOCX file

        Returns:
            True if processing was successful, False otherwise
        """
        # Check if file exists
        if not os.path.exists(docx_path):
            print(f"Error: File {docx_path} does not exist")
            return False

        # Get base filename without extension
        base_filename = os.path.splitext(os.path.basename(docx_path))[0]

        # Define output directories
        raw_dir = os.path.join(self.output_dir, "raw_outputs")
        json_dir = os.path.join(self.output_dir, "json_outputs")
        confidence_dir = os.path.join(self.output_dir, "confidence_scores")
        docx_copy_dir = os.path.join(self.output_dir, "docx_copies")

        # Parse DOCX using mammoth
        print(f"\nProcessing file: {docx_path}")

        try:
            # Save a copy of the DOCX for future reference
            docx_copy_path = os.path.join(docx_copy_dir, f"{base_filename}.docx")
            with open(docx_path, 'rb') as src_file, open(docx_copy_path, 'wb') as dst_file:
                dst_file.write(src_file.read())

            # Parse with Mammoth
            html_output, text_output = self.docx_parser.parse(docx_path)

            # Save raw parsed outputs
            with open(f"{raw_dir}/{base_filename}_html.html", "w", encoding="utf-8") as f:
                f.write(html_output)

            with open(f"{raw_dir}/{base_filename}_text.md", "w", encoding="utf-8") as f:
                f.write(text_output)

            # Combine parsed outputs - for DOCX we only have HTML and text
            parsed_outputs = {
                "html": html_output,
                "text": text_output
            }

            # Step 1: Generate JSON schema and confidence scores using HTML-specific prompt
            print(f"Step 1: Generating JSON schema and confidence scores for {base_filename}...")
            schema_json, confidence_json = self.gemini_processor.generate_schema_and_confidence_for_html(parsed_outputs)

            # Save confidence scores
            with open(f"{confidence_dir}/{base_filename}_confidence.json", "w", encoding="utf-8") as f:
                f.write(confidence_json)

            # Step 2: Generate final structured JSON
            print(f"Step 2: Generating final structured JSON for {base_filename}...")
            final_json = self.gemini_processor.generate_final_json_for_html(schema_json, parsed_outputs)

            # Save final JSON output
            with open(f"{json_dir}/{base_filename}.json", "w", encoding="utf-8") as f:
                f.write(final_json)

            print(f"✓ Successfully processed: {base_filename}")
            print(f"  - Raw outputs saved to {raw_dir}/{base_filename}_*.html/md")
            print(f"  - Confidence scores saved to {confidence_dir}/{base_filename}_confidence.json")
            print(f"  - Final JSON output saved to {json_dir}/{base_filename}.json")
            return True

        except Exception as e:
            print(f"✗ Error processing {docx_path}: {str(e)}")
            return False

    def process_directory(self, directory: str, limit: Optional[int] = None) -> Tuple[int, int]:
        """
        Process all PDF and DOCX files in a directory

        Args:
            directory: Directory containing PDF and DOCX files
            limit: Maximum number of files to process

        Returns:
            Tuple containing (successful_count, failed_count)
        """
        # Get all PDF and DOCX files in the directory
        pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
        docx_files = [f for f in os.listdir(directory) if f.lower().endswith('.docx')]
        all_files = pdf_files + docx_files

        if not all_files:
            print(f"No PDF or DOCX files found in directory: {directory}")
            return 0, 0

        # Apply limit if specified
        if limit and limit > 0:
            all_files = all_files[:limit]
            print(f"Processing {len(all_files)} of {len(pdf_files) + len(docx_files)} files (limit set to {limit})")
        else:
            print(f"Processing {len(all_files)} files from directory: {directory}")

        # Process each file
        successful = 0
        failed = 0

        for i, file in enumerate(all_files):
            file_path = os.path.join(directory, file)
            print(f"\n[{i+1}/{len(all_files)}] Processing: {file}")

            # Process based on file extension
            if file.lower().endswith('.pdf'):
                if self.process_pdf(file_path):
                    successful += 1
                else:
                    failed += 1
            elif file.lower().endswith('.docx'):
                if self.process_docx(file_path):
                    successful += 1
                else:
                    failed += 1

        # Print summary
        print("\n" + "="*50)
        print(f"Processing Summary:")
        print(f"  - Total files: {len(all_files)}")
        print(f"  - Successfully processed: {successful}")
        print(f"  - Failed: {failed}")
        print("\nOutput Directories:")
        print(f"  - Raw parser outputs: {os.path.join(self.output_dir, 'raw_outputs')}")
        print(f"  - Confidence scores: {os.path.join(self.output_dir, 'confidence_scores')}")
        print(f"  - Final JSON outputs: {os.path.join(self.output_dir, 'json_outputs')}")
        print("="*50)

        return successful, failed
