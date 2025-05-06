"""
Styles module for the Document Parser UI.

This module contains the CSS styles used in the Streamlit UI.
"""

import streamlit as st

def load_styles():
    """
    Load and apply CSS styles for the UI.
    """
    st.markdown("""
    <style>
        /* Typography improvements */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
        }
        p, div, span {
            font-size: 1.05rem;
        }
        .main-header {
            font-size: 2.8rem;
            font-weight: 700;
            color: #3B82F6;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        .sub-header {
            font-size: 1.3rem;
            font-weight: 400;
            color: #4B5563;
            margin-bottom: 2rem;
            text-align: center;
        }
        .json-title {
            font-size: 1.6rem;
            font-weight: 600;
            color: #3B82F6;
            margin-bottom: 1rem;
        }
        .section-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: #3B82F6;
            margin-top: 1rem;
            margin-bottom: 0.8rem;
            padding-bottom: 0.3rem;
            border-bottom: 2px solid #DBEAFE;
        }
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #F3F4F6;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            font-size: 1.1rem;
            font-weight: 500;
        }
        .stTabs [aria-selected="true"] {
            background-color: #DBEAFE;
            font-weight: 600;
        }
        /* JSON styling */
        .json-key {
            color: #3B82F6;
            font-weight: 600;
            font-size: 1.05rem;
        }
        .json-value {
            color: #1F2937;
            font-size: 1.05rem;
        }
        .json-string {
            color: #047857;
            font-size: 1.05rem;
        }
        .json-number {
            color: #7C3AED;
            font-size: 1.05rem;
        }
        .json-boolean {
            color: #B91C1C;
            font-size: 1.05rem;
        }
        .json-null {
            color: #6B7280;
            font-style: italic;
            font-size: 1.05rem;
        }
        /* Container styling */
        .footer {
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #E5E7EB;
            text-align: center;
            color: #6B7280;
            font-size: 0.9rem;
        }
        /* Message boxes */
        .success-box {
            background-color: #ECFDF5;
            border-left: 4px solid #10B981;
            padding: 1.2rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            font-size: 1.05rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        }
        .error-box {
            background-color: #FEF2F2;
            border-left: 4px solid #EF4444;
            padding: 1.2rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            font-size: 1.05rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        }
        /* Button styling */
        .stButton > button {
            font-weight: 500;
            font-size: 1.05rem;
            padding: 0.5rem 1rem;
            border-radius: 8px;
        }

        /* Improved captions */
        .caption-text {
            font-size: 0.95rem;
            color: #4B5563;
            margin-top: 0.5rem;
        }
        /* Improved navigation */
        .nav-button {
            background-color: #EFF6FF;
            border: 1px solid #BFDBFE;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .nav-button:hover {
            background-color: #DBEAFE;
        }
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* PDF Viewer improvements for sticky container */
        .pdf-container {
            padding: 0.5rem;
            margin-bottom: 1rem;
        }
        .pdf-container img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }
        /* Ensure the sticky container doesn't overlap with other elements */
        .stApp > header + div[data-testid="stVerticalBlock"] > div:first-child {
            padding-top: 0.5rem;
        }

        /* Fix for vertical line in PDF viewer */
        .element-container, .st-emotion-cache-17lr0tt, .e1lln2w81 {
            border: none !important;
            box-shadow: none !important;
        }
        div[data-testid="column"] {
            border-right: none !important;
            box-shadow: none !important;
        }
        /* Remove any vertical separators */
        .stVerticalBlock > div {
            border: none !important;
        }
    </style>
    """, unsafe_allow_html=True)
