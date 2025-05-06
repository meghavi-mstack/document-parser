# Document Parser UI

This directory contains the Streamlit UI for the Document Parser application. The UI is designed to be modular, maintainable, and user-friendly.

## Directory Structure

```
src/ui/
├── __init__.py           # Main UI module with the run_app function
├── styles.py             # CSS styles for the UI
├── components/           # UI components
│   ├── __init__.py
│   ├── pdf_viewer.py     # PDF viewer component
│   └── json_viewer.py    # JSON viewer component
└── utils/                # Utility functions
    ├── __init__.py
    └── processor.py      # Document processing utilities
```

## Module Descriptions

### `__init__.py`

The main UI module that orchestrates the application flow. It contains the `run_app()` function which is the entry point for the UI.

Key functions:
- `setup_page()`: Sets up the Streamlit page configuration
- `render_header()`: Renders the application header
- `render_upload_section()`: Renders the upload section for new documents
- `process_document()`: Processes the uploaded document
- `render_existing_documents_section()`: Renders the section for viewing existing documents
- `render_results()`: Renders the results section with PDF and JSON viewers
- `render_footer()`: Renders the application footer
- `run_app()`: Main function that runs the Streamlit application

### `styles.py`

Contains the CSS styles for the UI. The `load_styles()` function applies these styles to the Streamlit application.

### `components/pdf_viewer.py`

Provides components for viewing PDF documents:
- `render_pdf_viewer()`: Renders a PDF viewer for a given PDF path
- `render_pdf_placeholder()`: Renders a placeholder when the PDF is not available

### `components/json_viewer.py`

Provides components for viewing JSON data:
- `render_json_viewer()`: Renders a JSON viewer for the given JSON data
- `render_json_section()`: Recursively renders a JSON section with expandable/collapsible sections
- `render_json_value()`: Renders a JSON key-value pair with appropriate styling
- `format_json_value()`: Formats a JSON value with appropriate styling

### `utils/processor.py`

Provides utilities for processing documents:
- `create_document_processor()`: Creates and returns a document processor instance
- `process_uploaded_file()`: Processes an uploaded PDF file and returns the results
- `load_existing_json()`: Loads an existing JSON file

## Usage

The UI is used by importing the `run_app()` function from the `src.ui` module and calling it:

```python
from src.ui import run_app

if __name__ == "__main__":
    run_app()
```

## Features

- **PDF Upload**: Easily upload PDF documents for processing
- **PDF Viewer**: View the original PDF with page navigation
- **JSON Viewer**: Explore the parsed JSON with expandable/collapsible sections
- **Search**: Search for specific fields or values in the JSON data
- **Previously Processed Documents**: View previously processed documents
- **Download JSON**: Download the parsed JSON data as a file
