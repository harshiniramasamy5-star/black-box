# Personal Black Box

A professional Python CLI tool for recording predictions, reviewing outcomes, and improving decision-making accuracy over time.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

---

# Features

- Record predictions with confidence levels
- Review outcomes and calculate accuracy
- Search and filter entries
- Export prediction history
- Track calibration and decision-making patterns
- JSON-based persistent storage
- Command-line interface using argparse
- Automated testing with pytest

---

# Project Structure

```text
black_box/
│
├── black_box.py          # Main CLI application
├── test_black_box.py     # Test suite
├── requirements.txt      # Project dependencies
├── LICENSE               # MIT License
├── README.md             # Project documentation
├── .gitignore            # Ignored files/folders
└── data.json             # Prediction storage
```

---

# Requirements

- Python 3.10+

---

# Installation

Clone the repository:

```bash
git clone https://github.com/harshiniramasamy5-star/black-box.git
cd black-box
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Usage

## Record a Prediction

```bash
python black_box.py record \
--event "Math Exam" \
--statement "I will score above 90" \
--confidence 80
```

---

## List Predictions

```bash
python black_box.py list
```

---

## Review a Prediction

```bash
python black_box.py review \
--id 1 \
--outcome correct \
--accuracy 90
```

---

## View Statistics

```bash
python black_box.py stats
```

---

## Search Predictions

```bash
python black_box.py search --keyword "exam"
```

---

# Example Workflow

1. Record a prediction
2. Wait for the outcome
3. Review the prediction
4. Analyze confidence vs accuracy
5. Improve future decision-making

---

# Technologies Used

- Python
- argparse
- JSON
- pytest
- colorama

---

# Testing

Run tests using:

```bash
pytest
```

Generate HTML test report:

```bash
pytest --html=report.html
```

---

# Future Improvements

- SQLite database support
- CSV/Markdown export
- Interactive terminal UI
- Machine learning confidence analysis
- Web dashboard
- User authentication
- Prediction categories and tagging

---

# Learning Outcomes

This project demonstrates:

- CLI application development
- Argument parsing with argparse
- JSON data handling
- File persistence
- Software testing with pytest
- Git and GitHub workflows
- Clean project structuring
- Documentation practices

---

# License

This project is licensed under the MIT License.

See the LICENSE file for details.

---

# Author

Harshini Ramasamy

First-year CSE student passionate about software development, problem-solving, and building practical tools.

---
