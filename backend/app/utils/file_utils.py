from pathlib import Path

UPLOADS_DIR = Path("uploads")
STATIC_DIR = Path("static")

# Ensure directories exist at runtime
UPLOADS_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
