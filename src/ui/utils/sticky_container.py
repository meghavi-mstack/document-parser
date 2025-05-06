"""
Sticky Container utility for the Document Parser UI.

This module provides a utility for creating sticky containers in Streamlit.
"""

import streamlit as st
from typing import Literal, Optional

# Default margins for sticky containers
MARGINS = {
    "top": "5rem",  # Increased top margin to ensure PDF is fully visible
    "bottom": "0",
}

# HTML/CSS for creating a sticky container
STICKY_CONTAINER_HTML = """
<style>
div[data-testid="stVerticalBlock"] div:has(div.fixed-header-{i}) {{
    position: sticky;
    {position}: {margin};
    background-color: white;
    z-index: 999;
    max-height: 85vh;  /* Limit height to 85% of viewport height to ensure visibility */
    overflow-y: auto;  /* Add scrolling if content is too tall */
    padding-bottom: 2rem;  /* Add more padding at the bottom */
    border: none !important;
    box-shadow: none !important;
}}

/* Remove any borders or dividers within the sticky container */
div:has(div.fixed-header-{i}) * {{
    border-right: none !important;
    box-shadow: none !important;
}}
</style>
<div class='fixed-header-{i}'/>
""".strip()

# Counter to ensure unique IDs for multiple sticky containers
count = 0


def sticky_container(
    *,
    height: Optional[int] = None,
    border: Optional[bool] = None,
    mode: Literal["top", "bottom"] = "top",
    margin: Optional[str] = None,
):
    """
    Create a sticky container that remains fixed while scrolling.

    Args:
        height: Optional height for the container
        border: Whether to add a border to the container
        mode: Position mode ('top' or 'bottom')
        margin: Custom margin value (defaults to predefined margins if None)

    Returns:
        A Streamlit container that will stick to the specified position
    """
    if margin is None:
        margin = MARGINS[mode]

    global count
    html_code = STICKY_CONTAINER_HTML.format(position=mode, margin=margin, i=count)
    count += 1

    container = st.container(height=height, border=border)
    container.markdown(html_code, unsafe_allow_html=True)
    return container
