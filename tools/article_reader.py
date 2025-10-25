import os
from typing import Optional
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from langchain.tools import tool

from globals import OBSIDIAN_VAULT
from utils.fuzzy_find import fuzzy_search

load_dotenv()

def _get_latest_date(base: str = ".") -> str | None:
    """Return the latest date in YYYY/MM/DD format."""
    base = Path(base)
    
    date_paths = [
        "/".join(p.parts[-3:])
        for p in base.glob("????/??/??")
        if p.is_dir()
    ]

    valid_dates = []
    for ds in date_paths:
        try:
            datetime.strptime(ds, "%Y/%m/%d")
            valid_dates.append(ds)
        except ValueError:
            continue

    if not valid_dates:
        return None

    return max(valid_dates)

def _list_articles(date: str):
    path = Path(OBSIDIAN_VAULT) / date
    categories = [item.name for item in path.iterdir() if item.is_dir()]

    articles = {}
    for category in categories:
        articles[category] = fuzzy_search(query="", date=date)

    return articles

@tool
def fuzzy_search_articles(query: str, date: Optional[str]=None, category: Optional[str]=None, limit: int = 5, cutoff: float = 75) -> list[str]:
    return fuzzy_search(query, date, category, limit, cutoff)
    

@tool
def read_article(path: str) -> str:
    """
    Read the content of an article file by its path.
    
    Args:
        path: The file path to the article
    
    Returns:
        The content of the article as a string
    """
    load_dotenv()
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"Error reading file {path}: {str(e)}"

@tool
def get_news_update():
    """
    Get the latest news updates from specific categories.
    Returns the titles of all articles from ekonomi, digital, hukum, lingkungan, internasional, and olahraga categories for the most recent date available.
    
    Returns:
        dict: A dictionary where keys are category names and values are lists of article information.
              Each entry contains the title, date, and category of an article.
    """

    latest_date = _get_latest_date(OBSIDIAN_VAULT)
    return _list_articles(latest_date)