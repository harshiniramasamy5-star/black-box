import json
from pathlib import Path

FILE_PATH = Path("black_box_data.json")


def load_data():
    if not FILE_PATH.exists():
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)