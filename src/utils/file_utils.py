"""
File utility functions
"""

import os
from typing import List


def get_pdf_files(directory: str) -> List[str]:
    """
    Get all PDF files in a directory
    
    Args:
        directory: Directory to search for PDF files
        
    Returns:
        List of PDF file paths
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Directory does not exist: {directory}")
    
    return [os.path.join(directory, f) for f in os.listdir(directory) 
            if f.lower().endswith('.pdf') and os.path.isfile(os.path.join(directory, f))]


def ensure_directory(directory: str) -> None:
    """
    Ensure a directory exists, creating it if necessary
    
    Args:
        directory: Directory to ensure exists
    """
    os.makedirs(directory, exist_ok=True)
