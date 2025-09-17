"""
Skill taxonomy loading and simple extraction utilities.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Cache for taxonomy
_TAXONOMY: Dict[str, Dict[str, List[str]]] | None = None

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TAXONOMY_PATH = DATA_DIR / "skills_taxonomy.json"


def get_taxonomy() -> Dict[str, Dict[str, List[str]]]:
    global _TAXONOMY
    if _TAXONOMY is None:
        with TAXONOMY_PATH.open("r", encoding="utf-8") as f:
            _TAXONOMY = json.load(f)
    return _TAXONOMY


def extract_skills_from_text(text: str) -> List[Tuple[str, str, str]]:
    """
    Return list of (skill_name, category, subcategory) found in text.
    Case-insensitive exact phrase matching for a curated taxonomy.
    """
    if not text:
        return []
    tokens = text.lower()
    results: List[Tuple[str, str, str]] = []
    seen = set()
    tax = get_taxonomy()

    for category, subs in tax.items():
        for subcategory, names in subs.items():
            for name in names:
                key = name.strip()
                if not key:
                    continue
                lname = key.lower()
                # Basic containment check; could be improved with word boundaries
                if lname in tokens and key.lower() not in seen:
                    seen.add(lname)
                    results.append((key, category, subcategory))
    return results
