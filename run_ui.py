#!/usr/bin/env python3
"""
Streamlit UI for the Document Parser

This module provides a beautiful web interface for the document parser,
allowing users to upload PDFs and view the parsed JSON output.
"""

from dotenv import load_dotenv
from src.ui import run_app

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    run_app()
