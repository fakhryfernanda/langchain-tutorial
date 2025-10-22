import os
import random
from pathlib import Path
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()


def _get_all_dates():
    """Helper function to get all available dates from the vault."""
    vault = Path(os.getenv("OBSIDIAN_VAULT"))
    if not vault.is_dir():
        return []
    
    dates = []
    
    # Find all date directories with YYYY/MM/DD structure
    for day_dir in vault.glob("????/??/??"):
        if day_dir.is_dir():
            day = day_dir.name
            month = day_dir.parent.name
            year = day_dir.parent.parent.name
            
            # Verify numeric date format and skip hidden directories
            if (len(year) == 4 and year.isdigit() and 
                len(month) == 2 and month.isdigit() and 
                len(day) == 2 and day.isdigit() and
                not year.startswith('.') and not month.startswith('.') and not day.startswith('.')):
                
                # Basic validation of date ranges
                month_int = int(month)
                day_int = int(day)
                
                if 1 <= month_int <= 12 and 1 <= day_int <= 31:
                    date_str = f"{year}-{month}-{day}"
                    dates.append(date_str)
    
    return sorted(dates, reverse=True)  # Return newest dates first


def _get_categories_for_date_path(date_path, allowed_categories):
    """Helper function to get all valid categories for a given date path."""
    categories = []
    if date_path.is_dir():
        for item in date_path.iterdir():
            if item.is_dir() and not item.name.startswith(".") and item.name in allowed_categories:
                categories.append(item.name)
    
    return sorted(categories)


@tool
def get_dates_and_categories(limit: int = 10, after_date: str = None):
    """
    Get a mapping of dates to their available categories, with pagination support.
    Results are returned in descending order (newest dates first).
    
    Args:
        limit (int, optional): Maximum number of dates to return. Defaults to 10.
        after_date (str, optional): If provided, only dates older than this date will be returned.
        
    Returns:
        dict: Mapping of dates (YYYY-MM-DD) to list of available categories for that date.
    """
    allowed_categories = ["arsip", "digital", "ekonomi", "gaya-hidup", "hiburan", "hukum", "info-tempo", "lingkungan", "internasional", "olahraga", "politik", "sains", "sepakbola", "teroka"]
    
    vault = Path(os.getenv("OBSIDIAN_VAULT"))
    if not vault.is_dir():
        return {}
    
    # Get all dates in descending order (newest first)
    all_dates = _get_all_dates()
    
    # Filter dates if after_date is specified
    if after_date:
        try:
            # Validate date format
            after_year, after_month, after_day = after_date.split("-")
            # Convert to comparable string format
            filtered_dates = []
            for date_str in all_dates:
                year, month, day = date_str.split("-")
                if (year, month, day) < (after_year, after_month, after_day):
                    filtered_dates.append(date_str)
            all_dates = filtered_dates
        except ValueError:
            return f"Invalid date format for after_date. Expected YYYY-MM-DD, got: {after_date}"
    
    result = {}
    count = 0
    
    for date_str in all_dates:
        if count >= limit:
            break
            
        try:
            year, month, day = date_str.split("-")
            date_path = vault / year / month / day
            
            categories = _get_categories_for_date_path(date_path, allowed_categories)
            
            if categories:  # Only add to result if there are categories
                result[date_str] = categories
                count += 1
                
        except Exception:
            continue  # Skip invalid date formats
    
    return result


@tool
def get_available_categories(date: str):
    """
    Get a list of available categories for a given date.
    
    Args:
        date (str): Date string in YYYY-MM-DD format
        
    Returns:
        list: List of available categories for the given date.
    """
    # List of allowed categories
    allowed_categories = ["arsip", "digital", "ekonomi", "gaya-hidup", "hiburan", "hukum", "info-tempo", "lingkungan", "internasional", "olahraga", "politik", "sains", "sepakbola", "teroka"]
    
    vault = Path(os.getenv("OBSIDIAN_VAULT"))
    if not vault.is_dir():
        return []
    
    try:
        year, month, day = date.split("-")
    except ValueError:
        return f"Invalid date format. Expected YYYY-MM-DD, got: {date}"

    date_path = vault / year / month / day
    if not date_path.is_dir():
        return []

    # Get all directories that are allowed categories and not hidden
    categories = []
    for item in date_path.iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name in allowed_categories:
            categories.append(item.name)
    
    return sorted(categories)


@tool
def list_articles(date: str, category: str):
    """
    List all articles for a given date (YYYY-MM-DD) and category with their metadata.
    
    Args:
        date (str): Date string in YYYY-MM-DD format
        category (str): Category name. Allowed categories: 
                       "arsip", "digital", "ekonomi", "gaya-hidup", "hiburan", 
                       "hukum", "info-tempo", "lingkungan", "internasional", 
                       "olahraga", "politik", "sains", "sepakbola", "teroka"
        
    Returns:
        list: List of dictionaries containing article metadata (title, date, category) for the given date-category combination.
    """
    # List of allowed categories
    allowed_categories = ["arsip", "digital", "ekonomi", "gaya-hidup", "hiburan", "hukum", "info-tempo", "lingkungan", "internasional", "olahraga", "politik", "sains", "sepakbola", "teroka"]
    
    vault = Path(os.getenv("OBSIDIAN_VAULT"))
    if not vault.is_dir():
        return []

    # Validate category first
    if category not in allowed_categories:
        return f"Category '{category}' is not in the allowed categories. Allowed categories: {allowed_categories}"
    
    # Validate date format
    try:
        year, month, day = date.split("-")
    except ValueError:
        return f"Invalid date format. Expected YYYY-MM-DD, got: {date}"

    date_path = vault / year / month / day
    if not date_path.is_dir():
        return []

    category_path = date_path / category
    if not category_path.is_dir():
        return []

    # Get all markdown files
    md_files = [f for f in category_path.iterdir() if f.is_file() and f.suffix.lower() == ".md"]
    
    articles = []
    for file_path in md_files:
        # Extract title from filename (remove extension)
        title = file_path.stem
        # Check content for "content not available" to skip such files
        try:
            content = file_path.read_text()
            if "content not available" not in content.lower():
                articles.append({
                    "title": title,
                    "date": date,
                    "category": category
                })
        except Exception:
            # Skip files that can't be read
            continue

    return articles


@tool
def read_article(date: str, category: str, max_retries=10):
    """
    Read a random article for a given date (YYYY-MM-DD) and category.
    Skips files containing 'Content not available' (case-insensitive).
    
    Args:
        date (str): Date string in YYYY-MM-DD format
        category (str): Category name. Allowed categories: 
                       "arsip", "digital", "ekonomi", "gaya-hidup", "hiburan", 
                       "hukum", "info-tempo", "lingkungan", "internasional", 
                       "olahraga", "politik", "sains", "sepakbola", "teroka"
        max_retries (int): Number of attempts to find a valid article
    """
    # List of allowed categories
    allowed_categories = ["arsip", "digital", "ekonomi", "gaya-hidup", "hiburan", "hukum", "info-tempo", "lingkungan", "internasional", "olahraga", "politik", "sains", "sepakbola", "teroka"]
    
    vault = Path(os.getenv("OBSIDIAN_VAULT"))
    if not vault.is_dir():
        return f"Vault not found: {vault}"

    # Validate category first
    if category not in allowed_categories:
        return f"Category '{category}' is not in the allowed categories. Allowed categories: {allowed_categories}"
    
    # Validate date format
    try:
        year, month, day = date.split("-")
    except ValueError:
        return f"Invalid date format. Expected YYYY-MM-DD, got: {date}"

    date_path = vault / year / month / day
    if not date_path.is_dir():
        return f"Date path does not exist: {date_path}"

    category_path = date_path / category
    if not category_path.is_dir():
        return f"Category '{category}' not found in: {date_path}"

    # Prefer markdown files; fall back to any files if none
    md_files = [f for f in category_path.iterdir() if f.is_file() and f.suffix.lower() == ".md"]
    files = md_files or [f for f in category_path.iterdir() if f.is_file()]
    if not files:
        return f"No files found in category: {category_path}"

    for _ in range(max_retries):
        article = random.choice(files)
        try:
            content = article.read_text()
        except Exception:
            # If we fail to read, try another file
            files = [f for f in category_path.iterdir() if f.is_file() and f.suffix.lower() == ".md"] if md_files else [f for f in category_path.iterdir() if f.is_file()]
            if not files:
                return f"No readable files found in category: {category_path}"
            article = random.choice(files)
            try:
                content = article.read_text()
            except Exception:
                continue

        if "content not available" not in content.lower():
            return content

    return f"No valid article found on {date} with category {category}."


if __name__ == "__main__":
    print(read_article())