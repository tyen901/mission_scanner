import re

def clean_mission_file(content: str) -> str:
    """Clean mission file content while preserving strings"""
    # Preserve strings
    preserved = {}
    def store_string(match):
        token = f"__STR_{len(preserved)}__"
        preserved[token] = match.group(0)
        return token
        
    cleaned = re.sub(r'"[^"]*"', store_string, content)
    
    # Remove comments
    cleaned = re.sub(r'//.*?(?:\n|$)', '', cleaned)
    cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
    
    # Normalize whitespace around keywords
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = re.sub(r'(\b(?:class)\b)\s+', r'\1 ', cleaned) 
    cleaned = re.sub(r'\s*([{}=;])\s*', r'\1', cleaned)
    
    # Restore strings
    for token, string in preserved.items():
        cleaned = cleaned.replace(token, string)
        
    return cleaned.strip()
