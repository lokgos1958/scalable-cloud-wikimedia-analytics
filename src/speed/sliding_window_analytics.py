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
    bot: bool
    anonymous: bool
    event_type: str


def expire_old_events(events: Deque[WindowEvent], window_seconds: int, now: float) -> None:
    while events and now - events[0].observed_at > window_seconds:
        events.popleft()


def top_titles(events: Deque[WindowEvent], limit: int) -> list[tuple[str, int]]:
    counts = Counter(f"{event.wiki}:{event.title}" for event in events)
    return counts.most_common(limit)


def top_wikis(events: Deque[WindowEvent], limit: int) -> list[tuple[str, int]]:
    counts = Counter(event.wiki for event in events)
    return counts.most_common(limit)


def top_event_types(events: Deque[WindowEvent], limit: int) -> list[tuple[str, int]]:
    counts = Counter(event.event_type for event in events)
    return counts.most_common(limit)


def bot_breakdown(events: Deque[WindowEvent]) -> dict[str, int]:
    bot_events = sum(1 for event in events if event.bot)
    return {
        "bot_events": bot_events,
        "human_events": len(events) - bot_events,
    }


def editor_breakdown(events: Deque[WindowEvent]) -> dict[str, int]:
    anonymous_events = sum(1 for event in events if event.anonymous)
    return {
        "anonymous_events": anonymous_events,
        "logged_in_events": len(events) - anonymous_events,
    }


def run_window_replay(
    input_path: str,
    window_seconds: int,
    top_n: int,
    report_every: int = 25,
    emit_progress: bool = True,
) -> dict:
    window: Deque[WindowEvent] = deque()
    processed = 0
    snapshots = 0

    def emit_snapshot(line_number: int) -> None:
        nonlocal snapshots
        snapshots += 1
        snapshot = {
            "line": line_number,
            "window_seconds": window_seconds,
            "events_in_window": len(window),
            "top_titles": top_titles(window, top_n),
            "top_wikis": top_wikis(window, top_n),
            "top_event_types": top_event_types(window, top_n),
            "bot_breakdown": bot_breakdown(window),
            "editor_breakdown": editor_breakdown(window),
        }
        if emit_progress:
            print(json.dumps(snapshot))

    with open(input_path, "r", encoding="utf-8") as handle:
        last_line_number = 0
        for line_number, line in enumerate(handle, 1):
            last_line_number = line_number
            record = json.loads(line)
            now = time.time()
            title = record.get("title")
            wiki = record.get("wiki")
            event_type = record.get("type")
            if not title or not wiki or not event_type:
                continue

            window.append(
                WindowEvent(
                    now,
                    wiki,
                    title,
                    bool(record.get("bot")),
                    bool(record.get("anon")),
                    event_type,
                )
            )
            expire_old_events(window, window_seconds, now)
            processed += 1

            if report_every > 0 and processed % report_every == 0:
                emit_snapshot(line_number)

    if processed > 0 and report_every > 0 and processed % report_every != 0:
        emit_snapshot(last_line_number)

    return {
        "processed_events": processed,
        "snapshots_emitted": snapshots,
        "final_window_size": len(window),
        "final_top_titles": top_titles(window, top_n),
        "final_top_wikis": top_wikis(window, top_n),
        "final_top_event_types": top_event_types(window, top_n),
        "final_bot_breakdown": bot_breakdown(window),
        "final_editor_breakdown": editor_breakdown(window),
    }


def process_json_lines(input_path: str, window_seconds: int, top_n: int) -> None:
    summary = run_window_replay(input_path, window_seconds, top_n)
    if summary["processed_events"] == 0:
        print(
            json.dumps(
                {
                    "processed_events": 0,
                    "message": "no valid events were found in the input file",
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
