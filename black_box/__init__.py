#!/usr/bin/env python3
"""Personal Black Box - Prediction & Calibration CLI Tool"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from statistics import mean

DATA_FILE = Path("black_box_data.json")

RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"entries": [], "next_id": 1}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def validate_score(value, name="Score"):
    try:
        v = float(value)
    except (TypeError, ValueError):
        print(f"{RED}Error: {name} must be a number between 0 and 100.{RESET}")
        sys.exit(1)

    if not (0 <= v <= 100):
        print(f"{RED}Error: {name} must be between 0 and 100 (got {v}).{RESET}")
        sys.exit(1)

    return v


def migrate_entry(e):
    """Fill in missing fields for entries created before schema additions."""
    e.setdefault("created", datetime.now().isoformat(timespec="seconds"))
    e.setdefault("status", "pending")
    e.setdefault("category", "general")
    e.setdefault("confidence", 0)
    e.setdefault("outcome", None)
    e.setdefault("accuracy", None)
    e.setdefault("lesson", None)
    e.setdefault("reviewed", None)
    e.setdefault("statement", e.get("prediction") or e.get("assumption") or "")
    return e


def print_entry(e):
    e = migrate_entry(e)  # ensure all fields exist before printing

    colour = GREEN if e["status"] == "reviewed" else YELLOW
    conf_colour = RED if e["confidence"] >= 80 else RESET

    print(
        f"{colour}[#{e['id']}] {e['event']}{RESET}  "
        f"cat={e['category']}  "
        f"conf={conf_colour}{e['confidence']}%{RESET}  "
        f"status={e['status']}  "
        f"created={e['created'][:10]}"
    )

    print(f"     Statement: {e['statement']}")

    if e["status"] == "reviewed":
        acc_colour = RED if (e["accuracy"] or 0) < 50 else GREEN

        print(
            f"     Outcome: {e['outcome']}  "
            f"accuracy={acc_colour}{e['accuracy']}%{RESET}  "
            f"lesson={e['lesson']}"
        )

    print()


def cmd_record(args):
    data = load_data()

    statement = args.prediction or args.assumption or args.statement

    if not statement:
        print(f"{RED}Error: provide --prediction, --assumption, or --statement.{RESET}")
        sys.exit(1)

    confidence = validate_score(args.confidence, "Confidence")

    entry = {
        "id": data["next_id"],
        "event": args.event,
        "statement": statement,
        "confidence": confidence,
        "category": args.category or "general",
        "created": datetime.now().isoformat(timespec="seconds"),
        "status": "pending",
        "outcome": None,
        "accuracy": None,
        "lesson": None,
        "reviewed": None,
    }

    data["entries"].append(entry)
    data["next_id"] += 1

    save_data(data)

    print(f"{GREEN}✓ Recorded entry #{entry['id']}: '{args.event}'{RESET}")


def cmd_list(args):
    data = load_data()
    entries = [migrate_entry(e) for e in data["entries"]]

    status_filter = getattr(args, "status", "all") or "all"
    search = getattr(args, "search", None)
    category = getattr(args, "category", None)

    if status_filter != "all":
        entries = [e for e in entries if e["status"] == status_filter]

    if category:
        entries = [
            e for e in entries
            if e["category"].lower() == category.lower()
        ]

    if search:
        kw = search.lower()

        entries = [
            e for e in entries
            if kw in e["event"].lower()
            or kw in e["statement"].lower()
            or kw in (e["lesson"] or "").lower()
        ]

    if not entries:
        print(f"{YELLOW}No entries found.{RESET}")
        return

    for e in entries:
        print_entry(e)


def cmd_review(args):
    data = load_data()

    entry = next(
        (e for e in data["entries"] if e["id"] == args.id),
        None
    )

    if not entry:
        print(f"{RED}Error: No entry with ID {args.id}.{RESET}")
        sys.exit(1)

    if entry.get("status") == "reviewed":
        print(f"{YELLOW}Warning: Entry #{args.id} is already reviewed. Overwriting.{RESET}")

    accuracy = validate_score(args.accuracy, "Accuracy")

    entry["outcome"] = args.outcome
    entry["accuracy"] = accuracy
    entry["lesson"] = args.lesson or ""
    entry["reviewed"] = datetime.now().isoformat(timespec="seconds")
    entry["status"] = "reviewed"

    save_data(data)

    print(f"{GREEN}✓ Entry #{args.id} reviewed. Accuracy: {accuracy}%{RESET}")


def cmd_stats(args):
    data = load_data()

    all_e = [migrate_entry(e) for e in data["entries"]]
    rev_e = [e for e in all_e if e["status"] == "reviewed"]

    if not all_e:
        print("No entries yet.")
        return

    avg_conf = mean(e["confidence"] for e in all_e)
    pending = sum(1 for e in all_e if e["status"] == "pending")

    print(f"\n{BOLD}=== Stats ==={RESET}")
    print(f"Total entries   : {len(all_e)}")
    print(f"Pending reviews : {YELLOW}{pending}{RESET}")
    print(f"Avg confidence  : {avg_conf:.1f}%")

    if rev_e:
        avg_acc = mean(e["accuracy"] for e in rev_e)

        print(f"Avg accuracy    : {avg_acc:.1f}%")

        best = max(rev_e, key=lambda e: e["accuracy"])
        worst = min(rev_e, key=lambda e: e["accuracy"])

        print(
            f"\n{GREEN}Best prediction : "
            f"#{best['id']} '{best['event']}' — "
            f"{best['accuracy']}% accurate{RESET}"
        )

        print(
            f"{RED}Worst prediction: "
            f"#{worst['id']} '{worst['event']}' — "
            f"{worst['accuracy']}% accurate{RESET}"
        )

        cats = {}

        for e in rev_e:
            cats.setdefault(
                e["category"],
                []
            ).append(e["confidence"] - e["accuracy"])

        overconf = max(cats, key=lambda c: mean(cats[c]))
        gap_val = mean(cats[overconf])
        sign = "+" if gap_val >= 0 else ""

        print(
            f"\n{RED}Most overconfident category: "
            f"'{overconf}' (avg gap {sign}{gap_val:.1f}%){RESET}"
        )

    else:
        print("No reviewed entries yet for accuracy stats.")

    print()


def cmd_calibration(args):
    data = load_data()

    # FIX: migrate all entries once, then filter — avoids double migrate_entry
    # on a throwaway dict copy which could miss nested field updates
    all_entries = [migrate_entry(e) for e in data["entries"]]
    rev_e = [e for e in all_entries if e["status"] == "reviewed"]

    if not rev_e:
        print(f"{YELLOW}No reviewed entries for calibration.{RESET}")
        return

    buckets = {}

    for lo in range(0, 100, 10):
        hi = lo + 9 if lo < 90 else 100
        buckets[(lo, hi)] = {"accs": [], "confs": []}

    for e in rev_e:
        c = e.get("confidence", 0)

        for (lo, hi) in buckets:
            if lo <= c <= hi:
                buckets[(lo, hi)]["accs"].append(e.get("accuracy", 0))
                buckets[(lo, hi)]["confs"].append(c)
                break

    print(f"\n{BOLD}=== Calibration Report ==={RESET}")

    for (lo, hi), bdata in sorted(buckets.items()):
        accs = bdata["accs"]

        if not accs:
            print(
                f"Confidence {lo:2d}-{hi}%  | "
                f"Predictions:  0 | "
                f"Avg accuracy: N/A | "
                f"Gap: N/A"
            )
            continue

        avg_acc = mean(accs)
        avg_conf = mean(bdata["confs"])
        gap = avg_acc - avg_conf
        gap_str = f"{gap:+.0f}%"
        gap_col = GREEN if gap >= 0 else RED

        print(
            f"Confidence {lo:2d}-{hi}%  | "
            f"Predictions: {len(accs):2d} | "
            f"Avg accuracy: {avg_acc:.0f}%  | "
            f"Gap: {gap_col}{gap_str}{RESET}"
        )

    print()


def cmd_search(args):
    if not any([args.keyword, args.event, args.category]):
        print(
            f"{RED}Error: provide at least one of "
            f"--keyword, --event, or --category.{RESET}"
        )
        sys.exit(1)

    data = load_data()
    entries = [migrate_entry(e) for e in data["entries"]]

    if args.event:
        kw = args.event.lower()
        entries = [e for e in entries if kw in e["event"].lower()]

    if args.category:
        entries = [
            e for e in entries
            if e["category"].lower() == args.category.lower()
        ]

    if args.keyword:
        kw = args.keyword.lower()
        entries = [
            e for e in entries
            if kw in e["event"].lower()
            or kw in e["statement"].lower()
            or kw in (e["lesson"] or "").lower()
        ]

    if not entries:
        print(f"{YELLOW}No entries found.{RESET}")
        return

    for e in entries:
        print_entry(e)


def cmd_export(args):
    data = load_data()

    # FIX: migrate all entries once, then filter — avoids double migrate_entry
    # on a throwaway dict copy which could miss nested field updates
    all_entries = [migrate_entry(e) for e in data["entries"]]
    rev_e = [e for e in all_entries if e["status"] == "reviewed"]

    if not rev_e:
        print(f"{YELLOW}No reviewed entries to export.{RESET}")
        return

    out = Path(args.output or "black_box_report.md")

    lines = [
        "# Personal Black Box — Reviewed Predictions\n",
        f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n",
    ]

    for e in rev_e:
        lines.append(f"## #{e['id']} — {e['event']}\n")
        lines.append(f"- **Statement**: {e['statement']}\n")
        lines.append(f"- **Category**: {e['category']}\n")
        lines.append(f"- **Confidence**: {e['confidence']}%\n")
        lines.append(f"- **Outcome**: {e['outcome']}\n")
        lines.append(f"- **Accuracy**: {e['accuracy']}%\n")
        lines.append(f"- **Lesson**: {e['lesson']}\n")
        lines.append(f"- **Reviewed**: {(e['reviewed'] or '')[:10]}\n\n")

    out.write_text("".join(lines))

    print(f"{GREEN}✓ Report written to {out}{RESET}")


def cmd_reminders(args):
    data = load_data()

    cutoff = datetime.now() - timedelta(days=30)

    # FIX: migrate entries once into a list, then filter cleanly
    all_entries = [migrate_entry(e) for e in data["entries"]]
    old = [
        e for e in all_entries
        if e["status"] == "pending"
        and datetime.fromisoformat(e["created"]) < cutoff
    ]

    if not old:
        print(f"{GREEN}No overdue pending entries.{RESET}")
        return

    print(f"{YELLOW}=== Overdue Pending Entries (>30 days) ==={RESET}")

    for e in old:
        days = (
            datetime.now() -
            datetime.fromisoformat(e["created"])
        ).days

        print(f"  #{e['id']} '{e['event']}' — {days} days old")


def cmd_edit(args):
    data = load_data()

    entry = next(
        (e for e in data["entries"] if e["id"] == args.id),
        None
    )

    if not entry:
        print(f"{RED}Error: No entry with ID {args.id}.{RESET}")
        sys.exit(1)

    if not any([
        args.event,
        args.statement,
        args.confidence is not None,
        args.category
    ]):
        print(
            f"{RED}Error: provide at least one of "
            f"--event, --statement, --confidence, "
            f"--category.{RESET}"
        )
        sys.exit(1)

    confirm = input(
        f"Edit entry #{args.id} '{entry['event']}'? [y/N] "
    ).strip().lower()

    if confirm != "y":
        print("Aborted.")
        return

    if args.event:
        entry["event"] = args.event

    if args.statement:
        entry["statement"] = args.statement

    if args.confidence is not None:
        entry["confidence"] = validate_score(args.confidence, "Confidence")

    if args.category:
        entry["category"] = args.category

    save_data(data)

    print(f"{GREEN}✓ Entry #{args.id} updated.{RESET}")


def cmd_delete(args):
    data = load_data()

    entry = next(
        (e for e in data["entries"] if e["id"] == args.id),
        None
    )

    if not entry:
        print(f"{RED}Error: No entry with ID {args.id}.{RESET}")
        sys.exit(1)

    confirm = input(
        f"Delete entry #{args.id} '{entry['event']}'? [y/N] "
    ).strip().lower()

    if confirm != "y":
        print("Aborted.")
        return

    data["entries"] = [
        e for e in data["entries"]
        if e["id"] != args.id
    ]

    save_data(data)

    print(f"{GREEN}✓ Entry #{args.id} deleted.{RESET}")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="black_box.py",
        description="Personal Black Box — track predictions & calibrate your thinking.",
    )

    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    p_rec = sub.add_parser("record", help="Record a new prediction or assumption")
    p_rec.add_argument("--event", required=True, help="Event name")
    p_rec.add_argument("--prediction", default=None, help="Prediction text")
    p_rec.add_argument("--assumption", default=None, help="Assumption text")
    p_rec.add_argument("--statement", default=None, help="Statement alias")
    p_rec.add_argument("--confidence", required=True, help="Confidence 0-100")
    p_rec.add_argument("--category", default="general", help="Category tag")

    p_lst = sub.add_parser("list", help="List entries")
    p_lst.add_argument("--status", default="all", choices=["pending", "reviewed", "all"])
    p_lst.add_argument("--category", default=None, help="Filter by category")
    p_lst.add_argument("--search", default=None, help="Keyword search")

    p_rev = sub.add_parser("review", help="Review a pending entry")
    p_rev.add_argument("id", type=int, help="Entry ID")
    p_rev.add_argument("--outcome", required=True, help="Actual outcome")
    p_rev.add_argument("--accuracy", required=True, help="Accuracy 0-100")
    p_rev.add_argument("--lesson", default="", help="Lesson learned")

    sub.add_parser("stats", help="Show overall statistics")
    sub.add_parser("calibration", help="Show calibration report")

    p_srch = sub.add_parser("search", help="Search entries")
    p_srch.add_argument("--keyword", default=None, help="Keyword search")
    p_srch.add_argument("--event", default=None, help="Search by event")
    p_srch.add_argument("--category", default=None, help="Filter by category")

    p_exp = sub.add_parser("export", help="Export reviewed entries")
    p_exp.add_argument("--output", default="black_box_report.md", help="Output file path")

    sub.add_parser("remind", help="Show overdue pending entries")

    p_edit = sub.add_parser("edit", help="Edit an existing entry")
    p_edit.add_argument("id", type=int)
    p_edit.add_argument("--event", default=None)
    p_edit.add_argument("--statement", default=None)
    p_edit.add_argument("--confidence", default=None)
    p_edit.add_argument("--category", default=None)

    p_del = sub.add_parser("delete", help="Delete an entry")
    p_del.add_argument("id", type=int)

    return parser


COMMAND_MAP = {
    "record": cmd_record,
    "list": cmd_list,
    "review": cmd_review,
    "stats": cmd_stats,
    "calibration": cmd_calibration,
    "search": cmd_search,
    "export": cmd_export,
    "remind": cmd_reminders,
    "edit": cmd_edit,
    "delete": cmd_delete,
}


if __name__ == "__main__":
    parser = build_parser()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    fn = COMMAND_MAP.get(args.command)

    if fn:
        fn(args)
    else:
        parser.print_help()
