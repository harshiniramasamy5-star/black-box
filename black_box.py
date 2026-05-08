# professional_black_box.py


import argparse
import json
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

DATA_FILE = "data.json"


# =========================
# Utility Functions
# =========================


def load_data():
    """Load prediction data from JSON storage."""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []



def save_data(data):
    """Save prediction data into JSON storage."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)



def validate_score(value, name="Score"):
    """Validate that a score is between 0 and 100."""
    try:
        value = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{name} must be a number")

    if not (0 <= value <= 100):
        raise argparse.ArgumentTypeError(f"{name} must be between 0 and 100")

    return value



def print_entry(entry):
    """Display a formatted prediction entry."""
    print(Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + f"ID: {entry['id']}")
    print(f"Event: {entry['event']}")
    print(f"Statement: {entry['statement']}")
    print(f"Confidence: {entry['confidence']}%")
    print(f"Category: {entry.get('category', 'General')}")
    print(f"Status: {entry['status']}")
    print(f"Created: {entry['created_at']}")

    if entry['status'] == 'reviewed':
        print(f"Outcome: {entry.get('outcome', 'N/A')}")
        print(f"Accuracy: {entry.get('accuracy', 'N/A')}%")
        print(f"Lesson: {entry.get('lesson', 'N/A')}")


# =========================
# Command Functions
# =========================


def cmd_record(args):
    """Record a new prediction."""
    data = load_data()

    new_id = max([item["id"] for item in data], default=0) + 1

    entry = {
        "id": new_id,
        "event": args.event,
        "statement": args.statement,
        "confidence": args.confidence,
        "category": args.category,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    data.append(entry)
    save_data(data)

    print(Fore.GREEN + "Prediction recorded successfully!")
    print_entry(entry)



def cmd_list(args):
    """List all predictions with optional filters."""
    data = load_data()

    if args.status:
        data = [item for item in data if item["status"] == args.status]

    if args.category:
        data = [item for item in data if item.get("category", "").lower() == args.category.lower()]

    if not data:
        print(Fore.RED + "No entries found.")
        return

    for entry in data:
        print_entry(entry)



def cmd_review(args):
    """Review a prediction and update outcome."""
    data = load_data()

    for entry in data:
        if entry["id"] == args.id:
            entry["status"] = "reviewed"
            entry["outcome"] = args.outcome
            entry["accuracy"] = args.accuracy
            entry["lesson"] = args.lesson
            entry["reviewed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            save_data(data)

            print(Fore.GREEN + "Prediction reviewed successfully!")
            print_entry(entry)
            return

    print(Fore.RED + "Entry not found.")



def cmd_stats(args):
    """Display prediction statistics."""
    data = load_data()

    total = len(data)
    reviewed = [item for item in data if item["status"] == "reviewed"]
    pending = [item for item in data if item["status"] == "pending"]

    print(Fore.CYAN + "\n=== Prediction Statistics ===")
    print(f"Total Predictions: {total}")
    print(f"Reviewed Predictions: {len(reviewed)}")
    print(f"Pending Predictions: {len(pending)}")

    if reviewed:
        avg_accuracy = sum(item.get("accuracy", 0) for item in reviewed) / len(reviewed)
        print(f"Average Accuracy: {avg_accuracy:.2f}%")



def cmd_search(args):
    """Search predictions by keyword."""
    data = load_data()

    keyword = args.keyword.lower()

    results = [
        item for item in data
        if keyword in item["event"].lower()
        or keyword in item["statement"].lower()
    ]

    if not results:
        print(Fore.RED + "No matching predictions found.")
        return

    for entry in results:
        print_entry(entry)



def cmd_delete(args):
    """Delete a prediction entry."""
    data = load_data()

    updated_data = [item for item in data if item["id"] != args.id]

    if len(updated_data) == len(data):
        print(Fore.RED + "Entry not found.")
        return

    save_data(updated_data)

    print(Fore.GREEN + f"Entry {args.id} deleted successfully.")



def cmd_export(args):
    """Export predictions to a JSON file."""
    data = load_data()

    export_file = args.file

    with open(export_file, "w") as file:
        json.dump(data, file, indent=4)

    print(Fore.GREEN + f"Data exported to {export_file}")



def cmd_reminders(args):
    """Show pending predictions that need review."""
    data = load_data()

    pending = [item for item in data if item["status"] == "pending"]

    if not pending:
        print(Fore.GREEN + "No overdue pending entries.")
        return

    print(Fore.CYAN + "\n=== Pending Predictions ===")

    for entry in pending:
        print_entry(entry)


# =========================
# Main Parser Setup
# =========================


def main():
    """Main CLI entry point."""

    parser = argparse.ArgumentParser(
        description="Personal Black Box - Prediction Calibration CLI Tool"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Record Command
    parser_record = subparsers.add_parser("record", help="Record a prediction")

    parser_record.add_argument("--event", required=True, help="Event name")
    parser_record.add_argument("--statement", required=True, help="Prediction statement")
    parser_record.add_argument(
        "--confidence",
        required=True,
        type=lambda x: validate_score(x, "Confidence"),
        help="Confidence level (0-100)"
    )
    parser_record.add_argument(
        "--category",
        default="General",
        help="Prediction category"
    )

    parser_record.set_defaults(func=cmd_record)

    # List Command
    parser_list = subparsers.add_parser("list", help="List predictions")

    parser_list.add_argument(
        "--status",
        choices=["pending", "reviewed"],
        help="Filter by status"
    )

    parser_list.add_argument(
        "--category",
        help="Filter by category"
    )

    parser_list.set_defaults(func=cmd_list)

    # Review Command
    parser_review = subparsers.add_parser("review", help="Review a prediction")

    parser_review.add_argument("--id", required=True, type=int, help="Prediction ID")
    parser_review.add_argument("--outcome", required=True, help="Outcome")
    parser_review.add_argument(
        "--accuracy",
        required=True,
        type=lambda x: validate_score(x, "Accuracy"),
        help="Accuracy score (0-100)"
    )
    parser_review.add_argument(
        "--lesson",
        default="No lesson provided",
        help="Lesson learned"
    )

    parser_review.set_defaults(func=cmd_review)

    # Stats Command
    parser_stats = subparsers.add_parser("stats", help="Show statistics")
    parser_stats.set_defaults(func=cmd_stats)

    # Search Command
    parser_search = subparsers.add_parser("search", help="Search predictions")
    parser_search.add_argument("--keyword", required=True, help="Search keyword")
    parser_search.set_defaults(func=cmd_search)

    # Delete Command
    parser_delete = subparsers.add_parser("delete", help="Delete prediction")
    parser_delete.add_argument("--id", required=True, type=int, help="Prediction ID")
    parser_delete.set_defaults(func=cmd_delete)

    # Export Command
    parser_export = subparsers.add_parser("export", help="Export predictions")
    parser_export.add_argument(
        "--file",
        default="export.json",
        help="Export filename"
    )
    parser_export.set_defaults(func=cmd_export)

    # Reminders Command
    parser_reminders = subparsers.add_parser(
        "remind",
        help="Show pending reminders"
    )
    parser_reminders.set_defaults(func=cmd_reminders)

    # Parse Arguments
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```
