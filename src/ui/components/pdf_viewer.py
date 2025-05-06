"""
PDF Viewer component for the Document Parser UI.

This module provides a component for viewing PDF documents.
"""

import io
import streamlit as st
import fitz  # PyMuPDF
from PIL import Image


def render_pdf_viewer(pdf_path: str):
    """
    Render a PDF viewer for the given PDF path.

    Args:
        pdf_path: Path to the PDF file
    """
    try:
        # Get the number of pages in the PDF using PyMuPDF (fitz)
        doc = fitz.open(pdf_path)
        num_pages = len(doc)

        # Create a container for the PDF viewer
        pdf_container = st.container()

        with pdf_container:
            st.markdown('<div class="section-title">Original Document</div>', unsafe_allow_html=True)

            # Initialize page number in session state if not present
            if 'pdf_current_page' not in st.session_state:
                st.session_state.pdf_current_page = 1

            # Add page navigation if there are multiple pages
            if num_pages > 1:
                # Create a more visually appealing navigation bar
                st.markdown('<div style="display: flex; align-items: center; margin-bottom: 1rem;">', unsafe_allow_html=True)

                # Create navigation controls
                col1, col2, col3 = st.columns([1, 3, 1])

                # Previous button
                with col1:
                    # Disable the button if we're on the first page
                    prev_disabled = st.session_state.pdf_current_page <= 1
                    if st.button("← Previous", key="prev_button", use_container_width=True,
                                help="Go to previous page", disabled=prev_disabled):
                        # Decrement page number
                        st.session_state.pdf_current_page = max(1, st.session_state.pdf_current_page - 1)
                        st.rerun()

                # Page selector
                with col2:
                    # Create a number input for page selection
                    page_num = st.number_input(
                        "Page",
                        min_value=1,
                        max_value=num_pages,
                        value=st.session_state.pdf_current_page,
                        step=1,
                        key="pdf_page_input"
                    )

                    # Update the current page if changed
                    if page_num != st.session_state.pdf_current_page:
                        st.session_state.pdf_current_page = page_num
                        st.rerun()

                # Next button
                with col3:
                    # Disable the button if we're on the last page
                    next_disabled = st.session_state.pdf_current_page >= num_pages
                    if st.button("Next →", key="next_button", use_container_width=True,
                               help="Go to next page", disabled=next_disabled):
                        # Increment page number
                        st.session_state.pdf_current_page = min(num_pages, st.session_state.pdf_current_page + 1)
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

                # Get the current page number from session state
                page_num = st.session_state.pdf_current_page
            else:
                # If there's only one page, set the page number to 1
                page_num = 1
                st.session_state.pdf_current_page = 1

            # Display the current page with a CSS class for better styling in sticky container
            st.markdown('<div class="pdf-container" style="border: none; box-shadow: none;">', unsafe_allow_html=True)
            # Convert the page to an image and display it
            page = doc.load_page(page_num - 1)  # 0-based page number
            pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5))  # Higher zoom factor for better resolution

            # Convert pixmap to PIL Image
            img_bytes = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_bytes))

            # Display the image (using use_container_width instead of deprecated use_column_width)
            st.image(img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Display page information with better styling
            st.markdown(f'<p class="caption-text" style="text-align: center;">Page {page_num} of {num_pages}</p>', unsafe_allow_html=True)

        # Close the document
        doc.close()

    except Exception as e:
        st.error(f"Error displaying PDF: {str(e)}")


def render_pdf_placeholder():
    """
    Render a placeholder when the PDF is not available.
    """
    st.info("PDF file not available for viewing. Only JSON data will be displayed.")
    st.markdown('<p style="color: #4B5563; text-align: center; margin-top: 20px;">The original PDF may not be available if you\'re viewing a previously processed document.</p>', unsafe_allow_html=True)
