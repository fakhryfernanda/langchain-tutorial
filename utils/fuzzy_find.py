import os
from pathlib import Path
from dotenv import load_dotenv
from rapidfuzz import process, fuzz

def _build_file_index(directory="."):
    base = Path(directory).resolve()
    files = []
    for p in base.rglob("*"):
        if (
            p.is_file()
            and p.suffix == ".md"
            and not any(part.startswith('.') for part in p.relative_to(base).parts)
        ):
            files.append(p.name)

    return files

def fuzzy_find_files(query, limit=5, cutoff=0.7):
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

def main():
    result = fuzzy_find_files("Purbaya Yudhi Sadewa")

    print(result)

if __name__ == "__main__":
    main()