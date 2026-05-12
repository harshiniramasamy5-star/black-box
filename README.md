# Black Box

A command-line decision journal and calibration analysis tool for tracking predictions and measuring decision-making accuracy over time.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)
[![pytest](https://img.shields.io/badge/Tests-pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://pytest.org/)
[![CLI](https://img.shields.io/badge/Interface-CLI-6B7280?style=flat-square)]()

---

## Overview

Black Box is a Python-based CLI tool that enables systematic recording and analysis of predictions. The application captures predictions with confidence assessments, records actual outcomes, and computes calibration metrics to reveal patterns between subjective confidence and objective accuracy.

**Core Use Cases:**
- Track predictions and their outcomes across professional and personal domains
- Analyze confidence calibration to identify systematic biases
- Generate statistical reports on prediction accuracy
- Export decision journals for review and reflection

---

## Features

| Feature | Description |
|---------|-------------|
| **Record Predictions** | Capture prediction statement, confidence score, event details, and category |
| **Review Entries** | Log actual outcome, accuracy score, and lessons learned |
| **Calibration Analysis** | Group predictions by confidence range; compare stated vs. actual accuracy |
| **Statistics Dashboard** | Summary metrics: average confidence, accuracy, pending entries, extremes |
| **Search & Filter** | Query entries by keyword, event, category, or review status |
| **Export Reports** | Generate formatted Markdown reports of reviewed predictions |
| **Data Validation** | Input validation for confidence and accuracy scores (0–100) |
| **Persistent Storage** | All data stored locally in JSON format |
| **Status Tracking** | Distinguish between pending reviews and completed entries |
| **Terminal UI** | Colored output for visual status indication |

---

## Installation

### Requirements
- Python 3.10 or higher
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/harshiniramasamy5-star/black-box.git
cd black-box

# Install dependencies
pip install -r requirements.txt

# Verify installation
python black_box.py --help
```

---

## Quick Start

### Record a Prediction

```bash
python black_box.py record \
  --event "Q2 earnings announcement" \
  --prediction "Revenue will exceed 15% YoY growth" \
  --confidence 75 \
  --category business
```

### List Predictions

```bash
# View pending predictions
python black_box.py list --status pending

# View all completed reviews
python black_box.py list --status reviewed
```

### Review a Prediction

After the event, record the outcome:

```bash
python black_box.py review 1 \
  --outcome "Revenue grew 18% YoY" \
  --accuracy 85 \
  --lesson "Underestimated market momentum in emerging regions"
```

### View Calibration

The core analytical feature—shows how well confidence predicts accuracy:

```bash
python black_box.py calibration
```

**Sample Output:**
```
Confidence 60–69% | Count: 3 | Avg Accuracy: 58% | Gap: -7%
Confidence 70–79% | Count: 8 | Avg Accuracy: 52% | Gap: -22%
Confidence 80–89% | Count: 5 | Avg Accuracy: 61% | Gap: -24%
```

A **negative gap** indicates overconfidence; a **near-zero gap** indicates well-calibrated predictions.

### View Statistics

```bash
python black_box.py stats
```

**Sample Output:**
```
Total Predictions       : 16
Pending Reviews         : 2
Average Confidence      : 74%
Average Accuracy        : 59%
Best Prediction         : (accuracy: 95%)
Worst Prediction        : (accuracy: 20%)
Overconfident Category  : business (avg gap: -28%)
```

### Search Predictions

```bash
python black_box.py search --keyword "earnings"
python black_box.py search --category "business"
```

### Export Report

```bash
python black_box.py export
```

Generates a `report.md` file with all reviewed predictions.

---

## Command Reference

```bash
# Record a new prediction
python black_box.py record --event TEXT --prediction TEXT --confidence INT --category TEXT

# List predictions
python black_box.py list --status [pending|reviewed|all]

# Review a prediction
python black_box.py review ID --outcome TEXT --accuracy INT --lesson TEXT

# View calibration analysis
python black_box.py calibration

# View statistics
python black_box.py stats

# Search entries
python black_box.py search [--keyword TEXT] [--category TEXT]

# Export to Markdown
python black_box.py export [--output FILE]

# Edit an entry
python black_box.py edit ID [--confidence INT]

# Delete an entry
python black_box.py delete ID
```

---

## Data Model

Predictions are stored as JSON objects with the following schema:

```json
{
  "id": 1,
  "event": "Q2 earnings announcement",
  "prediction": "Revenue will exceed 15% YoY growth",
  "confidence": 75,
  "category": "business",
  "created_date": "2026-05-12",
  "status": "reviewed",
  "outcome": "Revenue grew 18% YoY",
  "accuracy": 85,
  "lesson": "Underestimated market momentum",
  "review_date": "2026-05-15"
}
```

---

## Project Structure

```
black-box/
├── black_box/
│   ├── __init__.py          # Main CLI logic and argument parsing
│   └── storage.py           # Data persistence layer
├── tests/
│   └── test_black_box.py    # pytest test suite
├── examples/
│   └── usage.md             # Usage examples
├── README.md                # This file
├── DOCUMENTATION.md         # Detailed documentation
├── TESTS.md                 # Testing guide
├── LICENSE                  # MIT License
├── requirements.txt         # Python dependencies
└── .gitignore              # Git exclusions
```

---

## Testing

Run the test suite:

```bash
# Run all tests with verbose output
pytest tests/ -v

# Generate coverage report
pytest tests/ --cov=black_box --cov-report=html

# Run specific test
pytest tests/test_black_box.py::test_record_prediction -v
```

**Test Coverage:**
- Input validation (confidence/accuracy bounds)
- Calibration computation and bucketing
- Statistics aggregation
- Data persistence
- Search and filter logic
- Edge cases (empty datasets, single entries)

---

## Technologies

| Component | Tool/Library |
|-----------|-------------|
| Language | Python 3.10+ |
| CLI Framework | argparse |
| Data Storage | JSON |
| Testing | pytest |
| Utilities | datetime, statistics, pathlib, colorama |

---

## API Usage (Programmatic)

```python
from black_box import BlackBox

# Initialize
bb = BlackBox()

# Record a prediction
bb.record(
    event="Market event",
    prediction="Stock will rise",
    confidence=80,
    category="finance"
)

# List predictions
predictions = bb.list(status="pending")

# Review a prediction
bb.review(
    entry_id=1,
    outcome="Stock rose 5%",
    accuracy=90,
    lesson="Market conditions favorable"
)

# Get calibration metrics
calibration = bb.calibration()

# Get statistics
stats = bb.stats()
```

---

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes with clear messages
4. Add tests for new functionality
5. Ensure all tests pass (`pytest tests/`)
6. Submit a pull request

---

## License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Author

**Harshini Ramasamy**

GitHub: [@harshiniramasamy5-star](https://github.com/harshiniramasamy5-star)
