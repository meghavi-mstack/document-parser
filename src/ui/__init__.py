"""
UI module for the Document Parser.

This module provides the Streamlit UI for the Document Parser.
"""

import os
import streamlit as st

from src.ui.styles import load_styles
from src.ui.components.pdf_viewer import render_pdf_viewer, render_pdf_placeholder
from src.ui.components.json_viewer import render_json_viewer
from src.ui.utils.processor import process_uploaded_file, load_existing_json
from src.ui.utils.sticky_container import sticky_container


def setup_page():
    """
    Set up the Streamlit page configuration.
    """
    st.set_page_config(
        page_title="Document Parser",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Load CSS styles
    load_styles()


def render_header():
    """
    Render the application header.
    """
    st.markdown('<div class="main-header">Document Parser</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Extract structured data from PDF documents</div>', unsafe_allow_html=True)


def render_reset_button():
    """
    Render a reset button to clear the session state.
    This function is kept for reference but not used anymore.
    The reset button is now in the results page.
    """
    pass


def render_upload_section():
    """
    Render the upload section for new documents.
    """
    # Upload section title
    st.markdown('<h2 style="text-align: center; color: #3B82F6; margin-bottom: 1.5rem;">Upload Your Document</h2>', unsafe_allow_html=True)

    # File uploader with improved instructions
    st.markdown('<p style="text-align: center; margin-bottom: 1.5rem;">Select a PDF document to extract structured data</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")

    if uploaded_file:
        # Show file details and process button
        st.markdown(f'<p style="text-align: center; font-weight: 500; margin: 1rem 0;">Selected: <span style="color: #3B82F6;">{uploaded_file.name}</span></p>', unsafe_allow_html=True)

        # Add some space
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

        # Process button in a centered column
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            process_button = st.button("Process Document", type="primary", use_container_width=True)
    else:
        # Show instructions when no file is uploaded
        st.markdown('Drag and drop a PDF file here or click to browse files', unsafe_allow_html=True)
        process_button = False
        uploaded_file = None

    # Option to view existing documents
    st.markdown('<div style="text-align: center; margin-top: 1.5rem;">', unsafe_allow_html=True)
    if st.button("View Previously Processed Documents"):
        st.session_state.show_existing = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    return uploaded_file, process_button


def process_document(uploaded_file):
    """
    Process the uploaded document and update the session state.

    Args:
        uploaded_file: The uploaded file from Streamlit

    Returns:
        Success flag (bool)
    """
    with st.spinner("Processing document... This may take a minute."):
        # Show a progress message
        progress_placeholder = st.empty()
        progress_placeholder.markdown('<div class="info-box" style="text-align: center;">Extracting text and generating structured data...</div>', unsafe_allow_html=True)

        # Process the file
        success, file_path, json_data = process_uploaded_file(uploaded_file)

        # Clear the progress message
        progress_placeholder.empty()

    if success and json_data:
        # Update session state
        st.session_state.pdf_path = file_path
        st.session_state.json_data = json_data
        st.session_state.processing_complete = True
        st.session_state.show_upload = False

        # Show success message and rerun to update the UI
        st.success("Document processed successfully!")
        st.rerun()
        return True
    else:
        st.markdown(f'<div class="error-box">Error: {file_path}</div>', unsafe_allow_html=True)

        # Add a debug expander for troubleshooting
        with st.expander("Debug Information"):
            st.write("### Processing Details")
            st.write(f"Uploaded file: {uploaded_file.name}")
            st.write(f"Temporary file path: {file_path}")

            # Check if the output directories exist
            output_dir = "parsed_outputs"
            json_dir = os.path.join(output_dir, "json_outputs")

            if os.path.exists(json_dir):
                st.write(f"Files in {json_dir}:")
                files = os.listdir(json_dir)
                if files:
                    for file in files:
                        st.write(f"- {file}")
                else:
                    st.write("No files found in the output directory.")
            else:
                st.write(f"Output directory does not exist: {json_dir}")

        return False


def render_existing_documents_section():
    """
    Render the section for viewing existing documents.
    """
    st.markdown('<h2 style="text-align: center; color: #3B82F6; margin-bottom: 1.5rem;">Previously Processed Documents</h2>', unsafe_allow_html=True)

    # Check if the output directory exists
    output_dir = "parsed_outputs"
    json_dir = os.path.join(output_dir, "json_outputs")

    if os.path.exists(json_dir):
        # Get list of JSON files
        json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

        if json_files:
            # Create a dropdown to select a JSON file
            selected_json = st.selectbox(
                "Select a document to view",
                json_files,
                index=None,
                placeholder="Choose a file..."
            )

            if selected_json:
                # Load the selected JSON file
                json_path = os.path.join(json_dir, selected_json)
                json_data = load_existing_json(json_path)

                if json_data:
                    # Store in session state
                    st.session_state.json_data = json_data
                    st.session_state.processing_complete = True
                    st.session_state.show_upload = False

                    # Try to find the corresponding PDF if it exists
                    base_filename = os.path.splitext(selected_json)[0]
                    pdf_dir = os.path.join(output_dir, "pdf_copies")

                    if os.path.exists(pdf_dir):
                        pdf_path = os.path.join(pdf_dir, f"{base_filename}.pdf")
                        if os.path.exists(pdf_path):
                            st.session_state.pdf_path = pdf_path

                    # Show success message and rerun to update the UI
                    st.success("Document loaded successfully!")
                    st.rerun()
        else:
            st.info("No processed documents found. Process a document first.")

            # Button to go back to upload
            if st.button("Upload a Document"):
                st.session_state.show_existing = False
                st.rerun()
    else:
        st.info(f"Output directory not found: {json_dir}")

        # Button to go back to upload
        if st.button("Upload a Document"):
            st.session_state.show_existing = False
            st.rerun()


def render_results():
    """
    Render the results section with PDF and JSON viewers.
    """
    # Header with logo and reset button
    header_col1, header_col2 = st.columns([6, 2])

    with header_col1:
        # Logo/title on the left
        st.markdown('<h3 style="color: #3B82F6; margin: 0;">Document Parser</h3>', unsafe_allow_html=True)

    with header_col2:
        # Reset button on the right
        if st.button("Start Over", use_container_width=True):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.show_upload = True
            st.session_state.processing_complete = False
            st.rerun()

    # Add custom CSS to remove column dividers
    st.markdown("""
    <style>
    /* Remove column dividers */
    div[data-testid="column"] {
        border-right: none !important;
        box-shadow: none !important;
        outline: none !important;
    }
    .st-emotion-cache-17lr0tt {
        border: none !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create two columns for the PDF viewer and JSON viewer
    col1, col2 = st.columns(2)

    with col1:
        # Use the sticky container for the PDF viewer with custom configuration
        with sticky_container(mode="top", border=True, margin="5rem"):
            # Add a container with some padding to ensure the PDF is fully visible
            pdf_container = st.container()
            with pdf_container:
                if 'pdf_path' in st.session_state and os.path.exists(st.session_state.pdf_path):
                    render_pdf_viewer(st.session_state.pdf_path)
                else:
                    render_pdf_placeholder()

    with col2:
        render_json_viewer(st.session_state.json_data)


def render_footer():
    """
    Render the application footer.
    """
    st.markdown('<div class="footer">Document Parser - A tool for parsing and structuring document data</div>', unsafe_allow_html=True)


def run_app():
    """
    Run the Streamlit application.
    """
    # Initialize session state variables if they don't exist
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    if 'show_upload' not in st.session_state:
        st.session_state.show_upload = True

    # Set up the page
    setup_page()

    # Render the header
    render_header()

    # Main content area
    if not st.session_state.processing_complete:
        # Show the existing documents view if requested
        if 'show_existing' in st.session_state and st.session_state.show_existing:
            render_existing_documents_section()
        else:
            # Show the upload interface
            uploaded_file, process_button = render_upload_section()

            # Process the uploaded file when the button is clicked
            if uploaded_file and process_button:
                process_document(uploaded_file)

    # Display the results if processing is complete
    if st.session_state.processing_complete and 'json_data' in st.session_state:
        render_results()

    # Render the footer
    render_footer()
