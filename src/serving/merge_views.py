"""Merge batch and speed views into a simple serving result."""

from collections import Counter
from typing import Iterable


def merge_top_counts(batch_rows: Iterable[dict], speed_rows: Iterable[dict], limit: int = 10) -> list[dict]:
    batch_counts = Counter()
    speed_counts = Counter()

    for row in batch_rows:
        key = f"{row['wiki']}:{row['title']}"
        batch_counts[key] += int(row["edit_count"])

    for row in speed_rows:
        key = f"{row['wiki']}:{row['title']}"
        speed_counts[key] += int(row["edit_count"])

    merged = batch_counts + speed_counts

    return [
        {
            "wiki": page.split(":", 1)[0],
            "title": page.split(":", 1)[1],
            "batch_edit_count": batch_counts.get(page, 0),
            "speed_edit_count": speed_counts.get(page, 0),
            "combined_edit_count": count,
        }
        for page, count in merged.most_common(limit)
    ]
