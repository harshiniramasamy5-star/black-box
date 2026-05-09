# 🖤 Personal Black Box

> *"Most people overestimate what they can do in a day and underestimate what they can do in a year."*  
> This tool helps you find out — with data.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-22C55E?style=flat-square)]()
[![pytest](https://img.shields.io/badge/Tested%20with-pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://pytest.org/)
[![CLI](https://img.shields.io/badge/Interface-CLI-6B7280?style=flat-square)]()

---

## What Is This?

**Personal Black Box** is a command-line decision journal. Before an important event — an exam, a pitch, a tough conversation — you record what you believe will happen and how confident you are. Afterward, you come back, score your accuracy, and write a short lesson.

Over time, the tool shows you something most people never see clearly: **how well your confidence actually predicts your accuracy**.

When you run `calibration`, you might discover:

```
Confidence 80–89% | Predictions: 5 | Average accuracy: 61% | Gap: -24%
```

That gap is where growth begins.

---

## Motivation

Professionals who get feedback loops right — investors, doctors, meteorologists — tend to improve faster than those who don't. This project applies that same principle to everyday decision-making. The goal is not journaling for its own sake. It is building a personal dataset that reveals patterns in how you think.

This project was built as a practical exploration of Python CLI development, data persistence, and software testing — skills directly applicable to backend and tools engineering roles.

---

## Features

| Feature | Description |
|---|---|
| **Record predictions** | Capture event, statement, confidence score, and category before outcomes are known |
| **Review entries** | Add actual outcome, accuracy score, and lesson after the fact |
| **Calibration analysis** | Group predictions by confidence range and compare against actual accuracy |
| **Statistics dashboard** | Average confidence, average accuracy, best/worst predictions, pending count |
| **Search and filter** | Query entries by keyword, event name, category, or status |
| **Export to Markdown** | Generate a formatted report of reviewed entries |
| **Pending reminders** | Flag entries older than 30 days that have not been reviewed |
| **Edit and delete** | Modify or remove entries with confirmation prompts |
| **Colored terminal output** | Visual cues for pending, reviewed, high-confidence, and low-accuracy entries |
| **JSON persistence** | All data saved locally in human-readable format |
| **Input validation** | Confidence and accuracy scores validated as integers from 0 to 100 |
| **Helpful error messages** | Clear feedback for invalid commands, missing IDs, and malformed input |

---

## Project Structure

```text
black_box/
│
├── black_box.py          # Main CLI application — argument parsing, commands, logic
├── test_black_box.py     # pytest test suite — validation, calibration, stats
├── requirements.txt      # Project dependencies
├── data.json             # JSON-based persistent prediction storage
├── README.md             # Project documentation
├── LICENSE               # MIT License
└── .gitignore            # Files excluded from version control
```

---

## Installation

**Clone the repository:**

```bash
git clone https://github.com/harshiniramasamy5-star/black-box.git
cd black-box
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Verify setup:**

```bash
python black_box.py --help
```

---

## Usage

### Record a Prediction

Capture what you believe before you know the outcome.

```bash
python black_box.py record \
  --event "Final exam" \
  --prediction "I will score above 85" \
  --confidence 70 \
  --category study
```

```bash
python black_box.py record \
  --event "Startup pitch" \
  --assumption "Investors care most about traction" \
  --confidence 80 \
  --category business
```

---

### List Predictions

View entries filtered by status.

```bash
# Show all pending predictions
python black_box.py list --status pending

# Show all reviewed predictions
python black_box.py list --status reviewed

# Show everything
python black_box.py list --status all
```

---

### Review a Prediction

Come back after the event and record what actually happened.

```bash
python black_box.py review 1 \
  --outcome "Scored 78" \
  --accuracy 60 \
  --lesson "I underestimated time pressure."
```

---

### View Statistics

See your overall performance at a glance.

```bash
python black_box.py stats
```

**Example output:**

```
Total predictions   : 14
Pending reviews     : 3
Average confidence  : 74%
Average accuracy    : 58%
Best prediction     : "I will finish the project on time" (accuracy: 95%)
Worst prediction    : "The client will love the first draft" (accuracy: 20%)
Most overconfident  : business (avg gap: -28%)
```

---

### Calibration Report

The most powerful feature. Reveals how well your subjective confidence matches real outcomes.

```bash
python black_box.py calibration
```

**Example output:**

```
Confidence 60–69% | Predictions: 3 | Average accuracy: 58% | Gap: -7%
Confidence 70–79% | Predictions: 8 | Average accuracy: 52% | Gap: -22%
Confidence 80–89% | Predictions: 5 | Average accuracy: 61% | Gap: -24%
```

A negative gap means you are overconfident in that range. A near-zero gap means you are well-calibrated.

---

### Search Predictions

Find entries by keyword, event name, or category.

```bash
python black_box.py search --keyword "exam"
python black_box.py search --category "business"
```

---

### Export to Markdown

Generate a readable report file of all reviewed predictions.

```bash
python black_box.py export
```

---

### Edit and Delete

Modify or remove entries with a confirmation prompt before changes are saved.

```bash
python black_box.py edit 3 --confidence 85
python black_box.py delete 3
```

---

## Data Model

Each prediction is stored as a JSON object with the following fields:

| Field | Type | Example | Purpose |
|---|---|---|---|
| `id` | integer | `1` | Unique identifier for review and edit commands |
| `event` | string | `"Final exam"` | The real-world event being predicted |
| `statement` | string | `"I will score above 85"` | The prediction or assumption |
| `confidence` | integer | `70` | Subjective probability, 0–100 |
| `category` | string | `"study"` | Tag for grouping and filtering |
| `created_date` | string | `"2025-07-10"` | Date the entry was recorded |
| `status` | string | `"pending"` | Either `pending` or `reviewed` |
| `outcome` | string | `"Scored 78"` | Actual result, added at review |
| `accuracy` | integer | `60` | How accurate the prediction was, 0–100 |
| `lesson` | string | `"Underestimated time pressure"` | Reflection written during review |
| `review_date` | string | `"2025-07-15"` | Date the review was completed |

---

## Testing

Run the full test suite:

```bash
pytest
```

Generate an HTML report:

```bash
pytest --html=report.html
```

The test suite covers:

- Confidence and accuracy input validation (0–100 bounds)
- Calibration bucket grouping and gap calculation
- Stats computation across mixed pending and reviewed entries
- Edge cases for empty datasets and single-entry collections
- Search and filter logic

---

## Technologies

| Tool | Role |
|---|---|
| Python 3.10+ | Core language |
| `argparse` | CLI argument parsing and subcommand routing |
| `json` | Data persistence and storage |
| `datetime` | Timestamping entries and detecting stale predictions |
| `statistics` | Mean calculations for stats and calibration |
| `pathlib` | Cross-platform file path handling |
| `colorama` | Colored terminal output for entry status and accuracy |
| `pytest` | Automated unit and integration testing |
| `pytest-html` | HTML test report generation |

---



## Future Improvements

- SQLite backend for querying across large datasets
- CSV export for spreadsheet analysis
- Interactive terminal UI using `rich` or `textual`
- Prediction categories and tagging system
- Machine learning confidence trend analysis
- Web dashboard with calibration charts
- User authentication for multi-user environments

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

**Harshini Ramasamy**  
First-year Computer Science and Engineering student  

Interested in backend development, developer tooling, and building software that solves real problems.

[![GitHub](https://img.shields.io/badge/GitHub-harshiniramasamy5--star-181717?style=flat-square&logo=github)](https://github.com/harshiniramasamy5-star)
