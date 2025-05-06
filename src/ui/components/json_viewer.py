"""
JSON Viewer component for the Document Parser UI.

This module provides a component for viewing JSON data.
"""

import json
import streamlit as st
from typing import Dict, Any


def render_json_viewer(json_data: Dict):
    """
    Render a simple JSON viewer for the given JSON data.

    Args:
        json_data: The JSON data to display
    """
    st.markdown('<div class="section-title">Structured Data Output</div>', unsafe_allow_html=True)

    # Format the JSON with proper indentation for better readability
    formatted_json = json.dumps(json_data, indent=2, ensure_ascii=False)

    # Display the formatted JSON
    st.code(formatted_json, language="json")

    # Add a download button for the JSON data
    st.download_button(
        label="Download JSON",
        data=formatted_json,
        file_name="parsed_document.json",
        mime="application/json",
        help="Download the JSON data as a file"
    )


# The interactive JSON viewer functions have been removed to simplify the UI
