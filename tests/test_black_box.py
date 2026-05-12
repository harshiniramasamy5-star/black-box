import json
from pathlib import Path
from black_box import validate_score, load_data, save_data

TEST_FILE = Path("test_black_box_data.json")



import black_box
black_box.DATA_FILE = TEST_FILE


<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
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


<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
def test_save_and_load():
    data = {"entries": [], "next_id": 1}

    save_data(data)
    loaded = load_data()

    assert loaded["next_id"] == 1
    assert isinstance(loaded["entries"], list)



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



def teardown_module(module):
    if TEST_FILE.exists():
        TEST_FILE.unlink()
