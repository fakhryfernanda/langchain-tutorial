import random
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

def get_random_date():
    """
    Traverse the vault structure to find and return a random date in YYYY-MM-DD format.
    
    Assumes structure: vault / YYYY / MM / DD
    
    Returns:
        str: Random date in YYYY-MM-DD format, or None if any level is missing.
    """
    vault = Path(os.getenv("OBSIDIAN_VAULT"))

    def get_random_subdir(path):
        subdirs = [d for d in path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        return random.choice(subdirs) if subdirs else None

    year = get_random_subdir(vault)
    month = get_random_subdir(year) if year else None
    day = get_random_subdir(month) if month else None

    if not all([year, month, day]):
        return None

    return f"{year.name}-{month.name}-{day.name}"


def get_random_category(date_path):
    """
    Select a random category from the given date path.
    
    Args:
        date_path (Path): Path to the date directory containing categories
        
    Returns:
        Path: Path to the randomly selected category directory, or None if no categories found
    """
    # Non-hidden categories
    categories = [p for p in date_path.iterdir() if p.is_dir() and not p.name.startswith(".")]
    if not categories:
        return None

    return random.choice(categories)


def read_article(date=None, category=None, max_retries=50):
    """
    Read a random article for a given date (YYYY-MM-DD). If no date is given,
    picks a random date from the vault. If category is provided, uses that specific category,
    otherwise picks a random category. Skips files containing 'Content not available' (case-insensitive).
    
    Args:
        date (str, optional): Date string in YYYY-MM-DD format
        category (str, optional): Specific category name to use
        max_retries (int): Number of attempts to find a valid article
    """
    vault = Path(os.getenv("OBSIDIAN_VAULT"))
    if not vault.is_dir():
        return f"Vault not found: {vault}"

    # Resolve date
    if not date:
        date = get_random_date()
        if not date:
            return "No dates found in the vault."

    try:
        year, month, day = date.split("-")
    except ValueError:
        return f"Invalid date format. Expected YYYY-MM-DD, got: {date}"

    date_path = vault / year / month / day
    if not date_path.is_dir():
        return f"Date path does not exist: {date_path}"

    # Select category based on whether it was provided
    if category:
        category_path = date_path / category
        if not category_path.is_dir():
            return f"Category '{category}' not found in: {date_path}"
        cat = category_path
    else:
        # Use the separate function to get a random category
        cat = get_random_category(date_path)
        if not cat:
            return f"No categories found in: {date_path}"

    # Prefer markdown files; fall back to any files if none
    md_files = [f for f in cat.iterdir() if f.is_file() and f.suffix.lower() == ".md"]
    files = md_files or [f for f in cat.iterdir() if f.is_file()]
    if not files:
        return f"No files found in category: {cat}"

    for _ in range(max_retries):
        article = random.choice(files)
        try:
            content = article.read_text()
        except Exception:
            # If we fail to read, try another file
            files = [f for f in cat.iterdir() if f.is_file() and f.suffix.lower() == ".md"] if md_files else [f for f in cat.iterdir() if f.is_file()]
            if not files:
                return f"No readable files found in category: {cat}"
            article = random.choice(files)
            try:
                content = article.read_text()
            except Exception:
                continue

        if "content not available" not in content.lower():
            return content

    return "No valid article found after multiple attempts."


# Example usage:
# print(read_article(date="2024-01-15"))   # Read random article from specific date
print(read_article())  # Falls back to random
