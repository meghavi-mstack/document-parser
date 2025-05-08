"""
DOCX Viewer component for the Document Parser UI.

This module provides a component for viewing DOCX documents.
"""

import os
import streamlit as st
import mammoth


def render_docx_viewer(docx_path: str):
    """
    Render a DOCX viewer for the given DOCX path.

    Args:
        docx_path: Path to the DOCX file
    """
    try:
        # Convert DOCX to HTML using mammoth
        with open(docx_path, 'rb') as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value
        
        # Create a container for the DOCX viewer
        docx_container = st.container()
        
        with docx_container:
            st.markdown('<div class="section-title">Original Document</div>', unsafe_allow_html=True)
            
            # Display the HTML content
            st.markdown(f"""
            <div class="docx-container" style="border: 1px solid #e0e0e0; padding: 1rem; border-radius: 0.5rem; max-height: 800px; overflow-y: auto;">
                {html}
            </div>
            """, unsafe_allow_html=True)
            
            # Add a download button for the original DOCX
            with open(docx_path, "rb") as file:
                docx_bytes = file.read()
                
            st.download_button(
                label="Download Original DOCX",
                data=docx_bytes,
                file_name=os.path.basename(docx_path),
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                help="Download the original DOCX file"
            )
    
    except Exception as e:
        st.error(f"Error displaying DOCX: {str(e)}")


def render_docx_placeholder():
    """
    Render a placeholder when the DOCX is not available.
    """
    st.info("DOCX file not available for viewing. Only JSON data will be displayed.")
    st.markdown('<p style="color: #4B5563; text-align: center; margin-top: 20px;">The original DOCX may not be available if you\'re viewing a previously processed document.</p>', unsafe_allow_html=True)
