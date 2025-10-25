import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.tools import tool
from rapidfuzz import process, fuzz

def _build_file_index(directory="."):
    base = Path(directory).resolve()
    return [str(p) for p in base.rglob("*.md")]

@tool
def fuzzy_search_articles(query: str, limit: int = 5, cutoff: float = 0.7) -> list[str]:
    """
        Search for news articles by name using fuzzy matching.
        
        Args:
            query: The name or partial name of the article you're looking for
            limit: Maximum number of results to return (default: 5)
            cutoff: Minimum similarity score (0-1) for results (default: 0.7)
        
        Returns:
            A list of file paths matching the query
    """

    load_dotenv()
    
    vault = os.getenv("OBSIDIAN_VAULT")
    if not vault:
        raise ValueError("OBSIDIAN_VAULT environment variable is not set.")

    index = _build_file_index(vault)
    
    matches = process.extract(
        query.lower().strip(),
        index,
        scorer=fuzz.WRatio,
        score_cutoff=cutoff,
        limit=limit
    )

    return [m[0] for m in matches]
    

if __name__ == "__main__":
    result = fuzzy_search_articles("Purbaya Yudhi Sadewa")

    print(result)