import json
from pathlib import Path
from black_box import validate_score, load_data, save_data

# Use a temporary test file so you don't corrupt real data
TEST_FILE = Path("test_black_box_data.json")


# ─────────────────────────────────────────────
# Override DATA_FILE safely for testing
# ─────────────────────────────────────────────
import black_box
black_box.DATA_FILE = TEST_FILE


# ─────────────────────────────────────────────
# Validation Tests
# ─────────────────────────────────────────────
def test_validate_score_valid():
    assert validate_score(50) == 50
    assert validate_score("75") == 75


def test_validate_score_invalid_low():
    try:
        validate_score(-1)
        assert False
    except SystemExit:
        assert True


def test_validate_score_invalid_high():
    try:
        validate_score(150)
        assert False
    except SystemExit:
        assert True


# ─────────────────────────────────────────────
# Data Persistence Tests
# ─────────────────────────────────────────────
def test_save_and_load():
    data = {"entries": [], "next_id": 1}

    save_data(data)
    loaded = load_data()

    assert loaded["next_id"] == 1
    assert isinstance(loaded["entries"], list)


# ─────────────────────────────────────────────
# Entry Creation Logic Test (simulated)
# ─────────────────────────────────────────────
def test_record_structure():
    data = {
        "entries": [{
            "id": 1,
            "event": "Test",
            "statement": "I will pass",
            "confidence": 80,
            "category": "study",
            "status": "pending",
            "accuracy": None
        }],
        "next_id": 2
    }

    save_data(data)
    loaded = load_data()

    entry = loaded["entries"][0]
    assert entry["event"] == "Test"
    assert entry["confidence"] == 80


# ─────────────────────────────────────────────
# Calibration Logic Test
# ─────────────────────────────────────────────
def test_calibration_bucket_logic():
    # simulate reviewed entries
    entries = [
        {"confidence": 75, "accuracy": 60, "status": "reviewed"},
        {"confidence": 78, "accuracy": 65, "status": "reviewed"},
        {"confidence": 85, "accuracy": 70, "status": "reviewed"},
    ]

    bucket = [e for e in entries if 70 <= e["confidence"] <= 79]

    assert len(bucket) == 2
    assert sum(e["accuracy"] for e in bucket) / len(bucket) == 62.5


# ─────────────────────────────────────────────
# Cleanup after tests
# ─────────────────────────────────────────────
def teardown_module(module):
    if TEST_FILE.exists():
        TEST_FILE.unlink()