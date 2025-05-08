"""
Command-line interface for the document parser
"""

import os
import sys
import argparse
from typing import List

from dotenv import load_dotenv

from .document_processor import DocumentProcessor


def parse_args(args: List[str]) -> argparse.Namespace:
    """
    Parse command-line arguments

    Args:
        args: Command-line arguments

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Parse PDF and DOCX documents and convert to structured JSON',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        'path',
        help='Path to a PDF/DOCX file or directory containing PDF/DOCX files'
    )

    parser.add_argument(
        '--output-dir', '-o',
        default="parsed_outputs",
        help='Directory to save output files'
    )

    parser.add_argument(
        '--limit', '-l',
        type=int,
        help='Limit the number of files to process (useful for testing)'
    )

    parser.add_argument(
        '--mistral-api-key',
        help='Mistral API key (defaults to MISTRAL_API_KEY environment variable)'
    )

    parser.add_argument(
        '--gemini-api-key',
        help='Gemini API key (defaults to GEMINI_API_KEY environment variable)'
    )

    return parser.parse_args(args)


def main() -> int:
    """
    Main entry point for the command-line interface

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    # Load environment variables from .env file if present
    load_dotenv()

    # Parse command-line arguments
    args = parse_args(sys.argv[1:])

    # Create document processor
    processor = DocumentProcessor(
        mistral_api_key=args.mistral_api_key,
        gemini_api_key=args.gemini_api_key,
        output_dir=args.output_dir
    )

    # Process file or directory
    if os.path.isfile(args.path):
        # Process a single file based on extension
        file_extension = os.path.splitext(args.path)[1].lower()
        if file_extension == '.pdf':
            success = processor.process_pdf(args.path)
        elif file_extension == '.docx':
            success = processor.process_docx(args.path)
        else:
            print(f"Error: Unsupported file type: {file_extension}")
            return 1
        return 0 if success else 1
    elif os.path.isdir(args.path):
        # Process all PDF and DOCX files in the directory
        successful, failed = processor.process_directory(args.path, args.limit)
        return 0 if failed == 0 else 1
    else:
        print(f"Error: Path does not exist: {args.path}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
