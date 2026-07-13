"""Save a small Wikimedia stream sample to a local JSON-lines file."""

import argparse
import json
from pathlib import Path

import requests


STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"


def clean_event(event):
    return {
        "id": event.get("id"),
        "timestamp": event.get("timestamp"),
        "wiki": event.get("wiki"),
        "title": event.get("title"),
        "type": event.get("type"),
        "bot": event.get("bot"),
        "user": event.get("user"),
        "server_name": event.get("server_name"),
    }


def save_events(output_file, max_records):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    saved = 0
    with requests.get(STREAM_URL, stream=True, timeout=30) as response:
        response.raise_for_status()

        with output_path.open("w", encoding="utf-8") as file:
            for line in response.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue

                event_text = line.replace("data: ", "", 1)
                event = json.loads(event_text)
                file.write(json.dumps(clean_event(event)) + "\n")

                saved += 1
                if saved % 25 == 0:
                    print(f"saved {saved} records")
                if saved >= max_records:
                    break

    print(f"sample saved to {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/raw/wikimedia_sample.jsonl")
    parser.add_argument("--max-records", type=int, default=100)
    args = parser.parse_args()

    save_events(args.output, args.max_records)


if __name__ == "__main__":
    main()

