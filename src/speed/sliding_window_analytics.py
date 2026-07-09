"""Local speed-layer prototype for sliding-window Wikimedia trends."""

import argparse
import json
import time
from collections import Counter, deque
from dataclasses import dataclass
from typing import Deque


@dataclass
class WindowEvent:
    observed_at: float
    wiki: str
    title: str


def expire_old_events(events: Deque[WindowEvent], window_seconds: int, now: float) -> None:
    while events and now - events[0].observed_at > window_seconds:
        events.popleft()


def top_titles(events: Deque[WindowEvent], limit: int) -> list[tuple[str, int]]:
    counts = Counter(f"{event.wiki}:{event.title}" for event in events)
    return counts.most_common(limit)


def process_json_lines(input_path: str, window_seconds: int, top_n: int) -> None:
    window: Deque[WindowEvent] = deque()

    with open(input_path, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            record = json.loads(line)
            now = time.time()
            title = record.get("title")
            wiki = record.get("wiki")
            if not title or not wiki:
                continue

            window.append(WindowEvent(now, wiki, title))
            expire_old_events(window, window_seconds, now)

            if line_number % 25 == 0:
                print(
                    json.dumps(
                        {
                            "line": line_number,
                            "window_seconds": window_seconds,
                            "events_in_window": len(window),
                            "top_titles": top_titles(window, top_n),
                        }
                    )
                )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Local JSON-lines file for replay testing")
    parser.add_argument("--window-seconds", type=int, default=300)
    parser.add_argument("--top-n", type=int, default=5)
    args = parser.parse_args()
    process_json_lines(args.input, args.window_seconds, args.top_n)


if __name__ == "__main__":
    main()

