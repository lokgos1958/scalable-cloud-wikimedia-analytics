"""Small local batch preview for Wikimedia JSON-lines samples.

This is a no-Java fallback for demo work. The main batch job is still the
PySpark script, but this creates the same style of output folders locally.
"""

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def read_events(input_path):
    events = []
    with open(input_path, "r", encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if record.get("title") and record.get("wiki") and record.get("timestamp"):
                events.append(record)
    return events


def event_time_parts(timestamp):
    event_time = datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
    return event_time.date().isoformat(), event_time.strftime("%Y-%m-%d %H:00:00")


def write_json_lines(folder, rows):
    folder.mkdir(parents=True, exist_ok=True)
    output_file = folder / "part-00000.jsonl"
    with output_file.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def build_preview_views(input_path, output_path):
    events = read_events(input_path)
    output_root = Path(output_path)

    page_counts = Counter((event["wiki"], event["title"]) for event in events)
    daily_counts = Counter()
    hourly_counts = Counter()
    bot_counts = Counter(bool(event.get("bot")) for event in events)

    for event in events:
        event_date, event_hour = event_time_parts(event["timestamp"])
        daily_counts[(event_date, event["wiki"])] += 1
        hourly_counts[(event_hour, event["wiki"])] += 1

    top_pages = [
        {"wiki": wiki, "title": title, "edit_count": count}
        for (wiki, title), count in page_counts.most_common(100)
    ]
    language_volume = [
        {"event_date": event_date, "wiki": wiki, "edit_count": count}
        for (event_date, wiki), count in sorted(daily_counts.items())
    ]
    hourly_volume = [
        {"event_hour": event_hour, "wiki": wiki, "edit_count": count}
        for (event_hour, wiki), count in sorted(hourly_counts.items())
    ]
    bot_summary = [
        {"bot": bot, "edit_count": count}
        for bot, count in bot_counts.most_common()
    ]

    write_json_lines(output_root / "top_pages", top_pages)
    write_json_lines(output_root / "language_volume", language_volume)
    write_json_lines(output_root / "hourly_volume", hourly_volume)
    write_json_lines(output_root / "bot_summary", bot_summary)

    print(f"events_read={len(events)}")
    print(f"output_path={output_root}")
    print("views_written=top_pages,language_volume,hourly_volume,bot_summary")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    build_preview_views(args.input, args.output)


if __name__ == "__main__":
    main()
