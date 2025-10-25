import os
import re
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from rapidfuzz import process, fuzz

from globals import OBSIDIAN_VAULT

def _is_valid_date_format(date_str: str) -> bool:
    """
    Validates date format to be either:
    - YYYY (4 digits)
    - YYYY/MM (4 digits, slash, 2 digits)
    - YYYY/MM/DD (4 digits, slash, 2 digits, slash, 2 digits)
    
    Args:
        date_str: The date string to validate
        
    Returns:
        True if the date format is valid, False otherwise
    """
    pattern = r"^\d{4}(/(0[1-9]|1[0-2])(/(0[1-9]|[12]\d|3[01]))?)?$"
    return bool(re.match(pattern, date_str))

def _build_file_index(directory: str = ".") -> list[str]:
    base = Path(directory).resolve()
    return [str(p) for p in base.rglob("*.md")]

def fuzzy_search(query: str, date: Optional[str]=None, category: Optional[str]=None, limit: Optional[int] = 5, cutoff: float = 75) -> list[str]:

    load_dotenv()
    
    path = OBSIDIAN_VAULT
        
    if date and _is_valid_date_format(date):
        path = os.path.join(OBSIDIAN_VAULT, date)

    if category:
        query = f"{category} {query}".strip()

    index = _build_file_index(path)

    if query:    
        matches = process.extract(
            query.lower().strip(),
            index,
            scorer=fuzz.partial_ratio,
            score_cutoff=cutoff,
            limit=limit
        )

        return [m[0] for m in matches]
    else:
        if limit:
            return index[:limit]
        else:
            return index

    

if __name__ == "__main__":
    result = fuzzy_search(query="", date="2025/10", category="politik")

    print(result)