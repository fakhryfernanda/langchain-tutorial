import os
import re
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from langchain.tools import tool
from rapidfuzz import process, fuzz


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

@tool
def fuzzy_search_articles(query: str, date: Optional[str]=None, category: Optional[str]=None, limit: int = 5, cutoff: float = 75) -> list[str]:
    """
        Search for news articles by name using fuzzy matching.
        
        Args:
            query: The name or partial name of the article you're looking for
            date: Optional date filter in format YYYY, YYYY/MM, or YYYY/MM/DD
            category: Optional category to filter or prioritize in the search
            limit: Maximum number of results to return (default: 5)
            cutoff: Minimum similarity score (0-100) for results (default: 75)
        
        Returns:
            A list of file paths matching the query
    """

    load_dotenv()
    
    path = os.getenv("OBSIDIAN_VAULT")
    if not path:
        raise ValueError("OBSIDIAN_VAULT environment variable is not set.")
    
    if date and _is_valid_date_format(date):
        path = os.path.join(path, date)

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
        return index[:limit]

    

if __name__ == "__main__":
    result = fuzzy_search_articles(query="", date="2025/10", category="politik")

    print(result)