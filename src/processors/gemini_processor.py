"""
Gemini processor module for generating structured JSON from parsed document text
"""

import os
import time
import random
from typing import Dict, Tuple

import google.generativeai as genai

from ..utils.json_utils import clean_json_string
from ..config.prompts import schema_generation_prompt, final_json_generation_prompt


class GeminiProcessor:
    """
    Processor that uses Google's Gemini to generate structured JSON from parsed document text
    """
    
    def __init__(self, api_key: str = None, model: str = "gemini-2.0-pro-exp-02-05"):
        """
        Initialize the Gemini processor
        
        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY environment variable)
            model: Gemini model to use
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable or pass it directly.")
        
        self.model_name = model
        genai.configure(api_key=self.api_key)
    
    def generate_schema_and_confidence(self, parsed_outputs: Dict[str, str]) -> Tuple[str, str]:
        """
        Generate JSON schema and confidence scores using Gemini
        
        Args:
            parsed_outputs: Dictionary of parsed outputs from different parsers
            
        Returns:
            Tuple containing:
                - JSON schema with extracted values
                - Confidence scores JSON with identical structure
        """
        print("Generating JSON schema and confidence scores...")
        
        # Combine all parsed outputs into a single message
        combined_text = f"""
# Mistral OCR Output:
{parsed_outputs.get('mistral_ocr', '')}

# Docling Output:
{parsed_outputs.get('docling', '')}

# PyMuPDF Output:
{parsed_outputs.get('pymupdf', '')}
"""

        prompt = schema_generation_prompt + "\n\nHere are the parsed outputs:\n" + combined_text
        
        # Implement retry logic with exponential backoff
        max_retries = 5
        base_delay = 2  # seconds
        
        for attempt in range(1, max_retries + 1):
            try:
                model = genai.GenerativeModel(self.model_name)
                response = model.generate_content(prompt)
                response_text = response.text
                
                # Extract schema and confidence JSONs from the response
                schema_json = ""
                confidence_json = ""
                
                if "SCHEMA_JSON:" in response_text and "CONFIDENCE_JSON:" in response_text:
                    parts = response_text.split("CONFIDENCE_JSON:")
                    schema_part = parts[0].strip()
                    confidence_part = parts[1].strip()
                    
                    # Extract schema JSON
                    if "SCHEMA_JSON:" in schema_part:
                        schema_json = schema_part.split("SCHEMA_JSON:")[1].strip()
                    
                    # Extract confidence JSON
                    confidence_json = confidence_part.strip()
                    
                    # Clean the JSON strings
                    schema_json = clean_json_string(schema_json)
                    confidence_json = clean_json_string(confidence_json)
                    
                    return schema_json, confidence_json
                else:
                    print(f"Response format incorrect (attempt {attempt}/{max_retries})")
                    if attempt == max_retries:
                        return clean_json_string(response_text), "{}"
            
            except Exception as e:
                print(f"Gemini API error (attempt {attempt}/{max_retries}): {str(e)}")
                
                if attempt < max_retries:
                    # Calculate delay with exponential backoff and jitter
                    delay = min(base_delay * (2 ** (attempt - 1)), 60)  # Cap at 60 seconds
                    jitter = random.uniform(-0.2, 0.2)
                    adjusted_delay = delay * (1 + jitter)
                    
                    print(f"Retrying in {adjusted_delay:.2f} seconds...")
                    time.sleep(adjusted_delay)
                else:
                    print("Maximum retries reached. Failed to generate schema and confidence scores.")
                    return "{}", "{}"

    def generate_final_json(self, schema_json: str, parsed_outputs: Dict[str, str]) -> str:
        """
        Generate final JSON using schema and parsed outputs
        
        Args:
            schema_json: JSON schema with extracted values
            parsed_outputs: Dictionary of parsed outputs from different parsers
            
        Returns:
            Final structured JSON
        """
        print("Generating final structured JSON...")
        
        # Combine all parsed outputs into a single message
        combined_text = f"""
# Mistral OCR Output:
{parsed_outputs.get('mistral_ocr', '')}

# Docling Output:
{parsed_outputs.get('docling', '')}

# PyMuPDF Output:
{parsed_outputs.get('pymupdf', '')}
"""

        prompt = final_json_generation_prompt + "\n\nHere is the schema JSON:\n" + schema_json + "\n\nHere are the parsed outputs:\n" + combined_text
        
        # Implement retry logic with exponential backoff
        max_retries = 5
        base_delay = 2  # seconds
        
        for attempt in range(1, max_retries + 1):
            try:
                model = genai.GenerativeModel(self.model_name)
                response = model.generate_content(prompt)
                final_json = clean_json_string(response.text)
                return final_json
            
            except Exception as e:
                print(f"Gemini API error (attempt {attempt}/{max_retries}): {str(e)}")
                
                if attempt < max_retries:
                    # Calculate delay with exponential backoff and jitter
                    delay = min(base_delay * (2 ** (attempt - 1)), 60)  # Cap at 60 seconds
                    jitter = random.uniform(-0.2, 0.2)
                    adjusted_delay = delay * (1 + jitter)
                    
                    print(f"Retrying in {adjusted_delay:.2f} seconds...")
                    time.sleep(adjusted_delay)
                else:
                    print("Maximum retries reached. Failed to generate final JSON.")
                    return "Error: Failed to generate final JSON after multiple attempts."
