"""Small local benchmark for replaying Wikimedia sample events."""

import argparse
import json
import time

from src.speed.sliding_window_analytics import run_window_replay


def benchmark_speed_layer(input_path: str, window_seconds: int, top_n: int, runs: int) -> None:
    results = []

    for run_number in range(1, runs + 1):
        started_at = time.perf_counter()
        summary = run_window_replay(
            input_path=input_path,
            window_seconds=window_seconds,
            top_n=top_n,
            emit_progress=False,
        )
        duration_seconds = time.perf_counter() - started_at
        processed_events = summary["processed_events"]
        events_per_second = processed_events / duration_seconds if duration_seconds else 0.0
        average_ms_per_event = (duration_seconds * 1000 / processed_events) if processed_events else 0.0

        results.append(
            {
                "run": run_number,
                "processed_events": processed_events,
                "duration_seconds": round(duration_seconds, 4),
                "events_per_second": round(events_per_second, 2),
                "average_ms_per_event": round(average_ms_per_event, 4),
                "final_window_size": summary["final_window_size"],
            }
        )

    print(json.dumps({"benchmark_runs": results}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Local JSON-lines file for replay testing")
    parser.add_argument("--window-seconds", type=int, default=300)
    parser.add_argument("--top-n", type=int, default=5)
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()
    benchmark_speed_layer(args.input, args.window_seconds, args.top_n, args.runs)


if __name__ == "__main__":
    main()
