# 📦 Black Box — Personal Prediction & Calibration Tracker
### Complete Project Documentation

> *"The goal is not just to store notes. The tool should reveal whether you are well-calibrated, overconfident, underconfident, or stronger in some categories than others."*

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [How AI Was Used to Build This Project](#3-how-ai-was-used-to-build-this-project)
4. [Architecture & Design](#4-architecture--design)
5. [Installation & Setup](#5-installation--setup)
6. [How to Use — Command Reference](#6-how-to-use--command-reference)
7. [Flow Diagrams](#7-flow-diagrams)
8. [Data Model](#8-data-model)
9. [Example Outputs](#9-example-outputs)
10. [Analytics & Calibration Explained](#10-analytics--calibration-explained)
11. [Bonus Features](#11-bonus-features)

---

## 1. Project Overview

**Black Box** is a beginner-friendly Python command-line tool that acts as a personal thinking journal with analytics. You record what you *think* will happen before events occur — along with how confident you are — then later review what *actually* happened. Over time, the tool surfaces patterns in your thinking:

- Are you consistently overconfident in business predictions?
- Does your 80% confidence actually correspond to 80% accuracy?
- Which categories of thinking are you best at?

This is the concept of **calibration** — the alignment between stated confidence and actual accuracy — and Black Box makes it measurable and personal.

**Tech Stack:**

| Module | Purpose |
|---|---|
| `argparse` | Command-line interface parsing |
| `json` | Local persistent data storage |
| `datetime` | Timestamps and 30-day reminders |
| `statistics` | Mean calculations for calibration and stats |
| `pathlib` | Cross-platform file path handling |
| `colorama` | Colored terminal output |

---

## 2. Problem Statement

Most people never examine the quality of their own thinking. They make predictions, events happen, and the analysis stops there. There is no feedback loop.

Black Box solves this by:

1. Forcing you to write down predictions *before* you know the outcome (eliminating hindsight bias)
2. Attaching a confidence score (0–100) so your certainty is on record
3. Later reviewing with an accuracy score and a written lesson
4. Running calibration analysis to reveal systematic biases across all your entries

The insight is not "were you right?" but "are you *reliably* right when you *say* you're confident?"

---

## 3. How AI Was Used in This Project

AI was used in the development of this project as a coding and documentation assistant. It helped speed up implementation, suggest improvements, and handle repetitive parts of development, while the overall planning, testing, and final decisions were done manually.

### 3.1 Understanding the Problem

The project idea and requirements came from the given problem statement. Based on that, the system design and feature planning were decided manually.

AI helped by suggesting:
- Better project structure
- Ways to organize commands
- Calibration logic for confidence tracking
- Cleaner CLI flow and validations

These suggestions were reviewed and modified during development wherever needed.

### 3.2 Code Development

A large portion of the code was developed with AI assistance. AI helped generate:
- Command handlers (`record`, `list`, `review`, `stats`, `calibration`, `edit`, `delete`, `export`)
- Input validation functions
- CLI argument parsing using argparse
- Calibration bucket calculations

The generated code was manually tested, edited, and integrated into the final project.

### 3.3 Testing and Debugging

Testing was done manually in a real Python environment. Different edge cases and scenarios were checked to ensure the tool worked correctly.

AI assisted by:
- Suggesting test cases
- Identifying possible edge cases
- Helping improve validation logic

However, all debugging, verification, and final corrections were handled during manual testing.

### 3.4 Overall Contribution

This project was developed using a balanced workflow between manual development and AI assistance.

AI helped reduce development time and improve productivity, while the final logic, validation, and project decisions remained manually controlled.

---

## 4. Architecture & Design

```
black_box.py
├── Data Layer         load_data() / save_data()  →  black_box_data.json
├── Validation         validate_score()  →  exits with clear error on bad input
├── Color Helpers      green/red/yellow/cyan/bold/dim  →  graceful fallback
└── Commands
    ├── record         Creates new entry, appends to JSON
    ├── list           Filters and displays entries in table form
    ├── review         Adds outcome + accuracy + lesson to an existing entry
    ├── stats          Calculates averages, gaps, best/worst, category breakdown
    ├── calibration    Groups reviewed entries into confidence buckets
    ├── edit           Updates any field on an existing entry (with confirmation)
    ├── delete         Removes an entry permanently (with confirmation)
    └── export         Writes a Markdown report of all reviewed entries
```

**Data persistence:** All records are stored in `black_box_data.json` in the working directory. This is a human-readable file you can inspect, backup, or move at any time.

**State transitions:**

```
[record]  →  status: "pending"
[review]  →  status: "reviewed"
[edit]    →  any field, any status
[delete]  →  entry removed
```

---

## 5. Installation & Setup

### Requirements

- Python 3.8 or newer
- No virtual environment needed for core functionality

### Step 1 — Download the file

```bash
# Place black_box.py in any folder
cd ~/projects/black_box
```

### Step 2 — Install optional color support

```bash
pip install colorama
```

Without colorama the tool works fully — output just won't be colored.

### Step 3 — Run your first command

```bash
python black_box.py
```

This prints the full help menu. You're ready.

### Step 4 — Record your first prediction

```bash
python black_box.py record \
  --event "Job Interview at Acme" \
  --prediction "I will get an offer" \
  --confidence 75 \
  --category career
```

---

## 6. How to Use — Command Reference

### `record` — Capture a prediction before an event

```bash
python black_box.py record \
  --event "EVENT NAME" \
  --prediction "YOUR PREDICTION"   # or --assumption / --statement
  --confidence 70 \
  --category study
```

| Flag | Required | Description |
|---|---|---|
| `--event` | Yes | Name of the real-world event |
| `--prediction` | One of these | A forward-looking statement about outcome |
| `--assumption` | One of these | A belief about how something works |
| `--statement` | One of these | Alias for `--prediction` |
| `--confidence` | Yes | Your certainty, 0–100 |
| `--category` | No | Tag for grouping (study, business, health, career, work…) |

---

### `list` — View your entries

```bash
python black_box.py list                        # all entries
python black_box.py list --status pending       # not yet reviewed
python black_box.py list --status reviewed      # already reviewed
python black_box.py list --category business    # filter by tag
python black_box.py list --search "pitch"       # keyword search
```

---

### `review` — Record the actual outcome

```bash
python black_box.py review 3 \
  --outcome "Got the offer at lower salary" \
  --accuracy 70 \
  --lesson "Underestimated negotiation friction"
```

| Argument | Required | Description |
|---|---|---|
| `id` | Yes | The numeric ID shown in `list` |
| `--outcome` | Yes | What actually happened |
| `--accuracy` | Yes | How accurate was your statement, 0–100 |
| `--lesson` | No | Reflection for your future self |

**What accuracy means:** This is a judgment call, not just right/wrong. If you predicted "Score above 85" and scored 78, you might give accuracy 55 — you were in the right direction but off by a meaningful margin.

---

### `stats` — Overview of your performance

```bash
python black_box.py stats
```

Prints:
- Total, reviewed, and pending counts
- Average confidence and average accuracy
- Best and worst predictions by accuracy
- Most overconfident category (avg confidence − avg accuracy)

---

### `calibration` — Your confidence vs. reality

```bash
python black_box.py calibration
```

Groups all reviewed predictions into confidence buckets (0–9%, 10–19%, …, 90–100%) and shows:
- How many predictions fall in that range
- The average actual accuracy of those predictions
- The gap: average accuracy minus average confidence within the bucket
- A positive gap means your accuracy exceeded your confidence (underconfident in that range)
- A negative gap means your accuracy fell short of your confidence (overconfident in that range)

---

### `edit` — Update an entry

```bash
python black_box.py edit 2 --category "startup" --lesson "Updated reflection"
```

Asks for confirmation before saving. Any field can be updated.

---

### `delete` — Remove an entry

```bash
python black_box.py delete 4
```

Asks "Are you sure?" before deleting. This is permanent.

---

### `export` — Markdown report of reviewed entries

```bash
python black_box.py export
python black_box.py export --output my_report.md
```

Creates a readable Markdown file with all reviewed entries, their outcomes, gaps, and lessons.

---

### `remind` — Show overdue pending entries

```bash
python black_box.py remind
```

Lists all pending entries that were created more than 30 days ago, so you remember to review them.

---

## 7. Flow Diagrams

### 7.1 Full Lifecycle of an Entry

```
User has an upcoming event
         │
         ▼
   python black_box.py record
   --event "..."
   --prediction/--assumption/--statement "..."
   --confidence 0-100
   --category "..."
         │
         ▼
   Entry created with status = PENDING
   Saved to black_box_data.json
         │
         │   (time passes, event occurs)
         │
         ▼
   python black_box.py review <id>
   --outcome "what happened"
   --accuracy 0-100
   --lesson "what I learned"
         │
         ▼
   Entry updated: status = REVIEWED
   outcome, accuracy, lesson, reviewed_date saved
         │
         ▼
   python black_box.py calibration
   python black_box.py stats
         │
         ▼
   Patterns discovered in your thinking
```

---

### 7.2 Calibration Bucket Algorithm

```
For each REVIEWED entry:
         │
         ▼
   bucket = int(confidence // 10) * 10
         │
   confidence=75 → bucket 70
   confidence=80 → bucket 80
   confidence=99 → bucket 90
   confidence=100 → bucket 100
         │
         ▼
   Group all accuracies and confidences by bucket
         │
         ▼
   For each bucket:
     avg_accuracy = mean(accuracies in bucket)
     avg_conf     = mean(confidences in bucket)
     gap          = avg_accuracy - avg_conf
         │
         ▼
   Display with verdict:
     gap >= 0  →  green   ← accuracy ≥ confidence (you were better than you thought)
     gap <  0  →  red     ← accuracy < confidence (you were worse than you thought)
```

---

### 7.3 `list` Command Filter Chain

```
All entries in JSON
       │
       ▼
  Filter by --status (pending / reviewed / all)
       │
       ▼
  Filter by --category (if provided)
       │
       ▼
  Filter by --search keyword (event, statement, category)
       │
       ▼
  Render table with color-coded status and accuracy
```

---

### 7.4 Validation Flow

```
User enters --confidence 110
       │
       ▼
  validate_score("110", "confidence")
       │
       ▼
  float("110") = 110.0  ✓ (is a number)
  110.0 > 100           ✗ (out of range)
       │
       ▼
  Print: "✗ Error: confidence must be a number between 0 and 100."
  sys.exit(1)  ← program exits cleanly, JSON not modified
```

---

## 8. Data Model

Each entry stored in `black_box_data.json`:

```json
{
  "id": 1,
  "event": "Final Exam",
  "statement": "I will score above 85",
  "confidence": 70.0,
  "category": "study",
  "created": "2026-05-10T14:32:00.123456",
  "status": "reviewed",
  "outcome": "Scored 78",
  "accuracy": 55.0,
  "lesson": "Underestimated time pressure under exam conditions",
  "reviewed": "2026-05-11T09:15:00.654321"
}
```

| Field | Type | When Set | Description |
|---|---|---|---|
| `id` | int | `record` | Auto-incrementing unique identifier |
| `event` | string | `record` | The real-world event name |
| `statement` | string | `record` | Prediction or assumption text |
| `confidence` | float | `record` | 0–100, user's stated certainty |
| `category` | string | `record` | Grouping tag |
| `created` | ISO datetime | `record` | When the entry was made |
| `status` | string | auto | `"pending"` → `"reviewed"` |
| `outcome` | string \| null | `review` | What actually happened |
| `accuracy` | float \| null | `review` | 0–100, retrospective accuracy score |
| `lesson` | string \| null | `review` | Reflection written during review |
| `reviewed` | ISO datetime \| null | `review` | When the review was done |

The JSON file also has a `next_id` key that auto-increments to ensure IDs are always unique.

---

## 9. Example Outputs

### 9.1 `record`

```
✓ Recorded entry #1: Final Exam
  Statement  : I will score above 85
  Confidence : 70.0%
  Category   : study
```

### 9.2 `list --status all`

```
ID   STATUS      CONF   ACC  EVENT                        CATEGORY       CREATED
──────────────────────────────────────────────────────────────────────────────────────────
1    reviewed   70.0% 55.0%  Final Exam                   study          2026-05-10
2    reviewed   80.0% 40.0%  Startup Pitch                business       2026-05-10
3    reviewed   75.0% 70.0%  Job Interview                career         2026-05-10
4    reviewed   85.0% 25.0%  Product Launch               business       2026-05-10
5    reviewed   90.0% 30.0%  Coding Sprint                work           2026-05-10
6    reviewed   65.0% 75.0%  Sales Call                   business       2026-05-10
7    pending    60.0%     —  Marathon Training            health         2026-05-10
8    pending    78.0%     —  Team Presentation            work           2026-05-10

Total: 8 entries
```

### 9.3 `stats`

```
=== Stats ===
Total entries   : 8
Pending reviews : 2
Avg confidence  : 75.4%
Avg accuracy    : 49.2%

Best prediction : #6 — Sales Call — 75% accurate
Worst prediction: #4 — Product Launch — 25% accurate

Most overconfident category: 'work' (avg gap +60.0%)
```

### 9.4 `calibration`

```
=== Calibration Report ===
Confidence 60-69%  | Predictions:  1 | Avg accuracy: 75%  | Gap: +10%
Confidence 70-79%  | Predictions:  2 | Avg accuracy: 62%  | Gap: -12%
Confidence 80-89%  | Predictions:  2 | Avg accuracy: 32%  | Gap: -52%
Confidence 90-100% | Predictions:  1 | Avg accuracy: 30%  | Gap: -60%
```

**Reading this output:** Gap = average accuracy − average confidence within the bucket. A positive gap means your accuracy *exceeded* your stated confidence (you were better than you thought). A negative gap means your accuracy *fell short* of your confidence (you were overconfident). In this example, at 80–89% confidence your accuracy was only 32% — a gap of −52 points, meaning you were dramatically overconfident in that range.

---

## 10. Analytics & Calibration Explained

### Why calibration matters

Most people think of predictions as binary: right or wrong. Calibration asks a deeper question: **does your confidence track your accuracy?**

A perfectly calibrated person who says "I'm 70% confident" is right about 70% of the time. They say "I'm 90% confident" only about things they're right about 90% of the time. Most people are not like this — they are **overconfident**, especially in domains where they feel expertise.

Black Box surfaces this by:

1. Collecting enough predictions over time across confidence levels
2. Grouping them into buckets (70–79%, 80–89%, etc.)
3. Computing actual accuracy in each bucket
4. Comparing actual accuracy vs. actual average confidence within that bucket

### The gap number

**Gap = average accuracy − average confidence (within the bucket)**

- **Gap near 0:** You're well-calibrated in this range
- **Gap negative (e.g. −20%):** Your accuracy fell short of your confidence — you were overconfident
- **Gap positive (e.g. +20%):** Your accuracy exceeded your confidence — you were underestimating yourself

### Using calibration to improve thinking

Once you see your patterns, you can adjust:

- If you're consistently showing a large negative gap in the 80–89% bucket, start treating your "85% confident" feelings with more skepticism
- If one category (e.g. career) shows a gap near 0 while another (e.g. work estimates) shows a large negative gap, you know where to trust yourself and where to be more careful

---

## 11. Bonus Features

All bonus challenges from the spec have been implemented:

| Feature | Implementation |
|---|---|
| Export to Markdown | `python black_box.py export` |
| 30-day pending reminders | `python black_box.py remind` — lists overdue entries |
| Edit with confirmation | `python black_box.py edit <id> [fields]` |
| Delete with confirmation | `python black_box.py delete <id>` |
| Unit tests | `python test_black_box.py` — 42 tests |
| Colored terminal output | Via `colorama` with graceful fallback |

---

*Black Box v1.0 — Built with Python 3, argparse, json, datetime, statistics, pathlib, colorama*