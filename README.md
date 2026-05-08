````markdown
# 🖤 Personal Black Box

A command-line tool to record predictions and assumptions before important events, then review them afterward to measure how well-calibrated your thinking is.

---

# ✨ Features

- Record predictions with confidence levels
- Review outcomes later with accuracy scores
- Measure overconfidence / underconfidence
- View calibration reports
- Analyze category-wise thinking bias
- Search entries quickly
- Edit and delete predictions
- Export reviewed entries to Markdown reports
- Get reminders for overdue pending entries

---

# 📦 Installation

## 1. Clone the project

```bash
git clone <your-repo-url>
cd black_box
````

## 2. Install dependencies

```bash
pip install colorama
```

---

# ▶️ Usage

```bash
python black_box.py <command> [options]
```

---

# 📌 Commands

| Command       | Purpose                      |
| ------------- | ---------------------------- |
| `record`      | Record a new prediction      |
| `list`        | List entries                 |
| `review`      | Review a prediction          |
| `stats`       | Show overall statistics      |
| `calibration` | Show calibration report      |
| `search`      | Search predictions           |
| `export`      | Export reviewed entries      |
| `remind`      | Show overdue pending entries |
| `edit`        | Edit an entry                |
| `delete`      | Delete an entry              |

---

# 🧠 Example Commands

## 1. Record a prediction

```bash
python black_box.py record \
--event "Final Exam" \
--statement "I will score above 90" \
--confidence 80 \
--category study
```

---

## 2. List all entries

```bash
python black_box.py list
```

---

## 3. List pending entries

```bash
python black_box.py list --status pending
```

---

## 4. List reviewed entries

```bash
python black_box.py list --status reviewed
```

---

## 5. Review a prediction

```bash
python black_box.py review 1 \
--outcome "Scored 85" \
--accuracy 75 \
--lesson "Need more revision"
```

---

## 6. View statistics

```bash
python black_box.py stats
```

Example output:

```text
=== Stats ===
Total entries   : 7
Pending reviews : 2
Avg confidence  : 59.3%
Avg accuracy    : 70.0%
```

---

## 7. View calibration report

```bash
python black_box.py calibration
```

Example output:

```text
Confidence 70-79% | Predictions: 2 | Avg accuracy: 68% | Gap: -2%
Confidence 80-89% | Predictions: 2 | Avg accuracy: 88% | Gap: +8%
```

---

## 8. Search entries

### By event

```bash
python black_box.py search --event exam
```

### By category

```bash
python black_box.py search --category study
```

### By keyword

```bash
python black_box.py search --keyword score
```

---

## 9. Edit an entry

```bash
python black_box.py edit 6 \
--statement "Updated prediction"
```

Update confidence:

```bash
python black_box.py edit 6 --confidence 55
```

---

## 10. Delete an entry

```bash
python black_box.py delete 8
```

---

## 11. Export reviewed entries

```bash
python black_box.py export
```

This creates:

```text
black_box_report.md
```

---

## 12. Get overdue reminders

```bash
python black_box.py remind
```

---

# 📊 Calibration Explained

The calibration report groups predictions into confidence buckets and compares expected confidence with actual accuracy.

Example:

| Confidence Bucket | Avg Accuracy | Meaning        |
| ----------------- | ------------ | -------------- |
| 80–89%            | 60%          | Overconfident  |
| 50–59%            | 70%          | Underconfident |

A positive gap means overconfidence.

A negative gap means underconfidence.

---

# 🗂️ Data Storage

All entries are stored in:

```text
black_box_data.json
```

Each entry contains:

| Field         | Description              |
| ------------- | ------------------------ |
| `id`          | Unique prediction ID     |
| `event`       | Event name               |
| `statement`   | Prediction/assumption    |
| `confidence`  | Confidence level (0–100) |
| `accuracy`    | Review accuracy (0–100)  |
| `lesson`      | Reflection after review  |
| `category`    | Prediction category      |
| `status`      | `pending` or `reviewed`  |
| `created_at`  | Creation date            |
| `reviewed_at` | Review date              |

---

# 🛡️ Validation

The CLI validates:

* Confidence must be between 0–100
* Accuracy must be between 0–100
* Invalid IDs are rejected
* Missing required arguments are handled safely

---

# 📁 Example Project Structure

```text
black_box/
│
├── black_box.py
├── storage.py
├── black_box_data.json
├── black_box_report.md
├── README.md
└── tests/
```

---

# 🚀 Future Improvements

Possible future upgrades:

* CSV export
* Graph visualizations
* SQLite database support
* AI-generated insight summaries
* Streak tracking
* Web dashboard
* User authentication

---


