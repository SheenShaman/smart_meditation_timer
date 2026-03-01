import json
from pathlib import Path

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "app_data.json"
DEFAULT_DATA = {
    "sessions": [],
    "settings": {
        "sound": True,
        "theme": "dark",
        "weekly_goal": 200,
    },
    "stats": {
        "total_minutes": 0,
    },
}


def is_data_file():
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()

    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATA, f, indent=4)


def load_data_file():
    is_data_file()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data_file(data: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
