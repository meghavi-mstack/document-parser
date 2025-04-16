"""
JSON utility functions
"""


def clean_json_string(json_str: str) -> str:
    """
    Clean up JSON string by removing markdown code block markers and other non-JSON content
    
    Args:
        json_str: JSON string that may contain markdown code block markers or other non-JSON content
        
    Returns:
        Clean JSON string
    """
    # Remove markdown code block markers if present
    if '```json' in json_str:
        json_str = json_str.replace('```json', '').replace('```', '')
    elif '```' in json_str:
        json_str = json_str.replace('```', '')
    
    # Remove any leading/trailing whitespace
    json_str = json_str.strip()
    
    # If the string starts with a comment or explanation, try to find the start of the JSON
    if not json_str.startswith('{') and not json_str.startswith('['):
        # Look for the first occurrence of { or [
        curly_brace_index = json_str.find('{')
        square_bracket_index = json_str.find('[')
        
        # Find the first valid JSON start character
        if curly_brace_index >= 0 and (square_bracket_index < 0 or curly_brace_index < square_bracket_index):
            json_str = json_str[curly_brace_index:]
        elif square_bracket_index >= 0:
            json_str = json_str[square_bracket_index:]
    
    return json_str
