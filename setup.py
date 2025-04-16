"""
Setup script for the document-parser package
"""

from setuptools import setup, find_packages

setup(
    name="document-parser",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "mistralai",
        "docling",
        "pymupdf4llm",
        "google-generativeai",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "document-parser=src.cli:main",
        ],
    },
    python_requires=">=3.8",
    author="Document Parser Team",
    author_email="info@example.com",
    description="A tool for parsing and structuring document data",
    keywords="pdf, parsing, ocr, json, document",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
