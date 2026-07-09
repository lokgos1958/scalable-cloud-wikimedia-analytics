"""Merge batch and speed views into a simple serving result."""

from collections import Counter
from typing import Iterable


def merge_top_counts(batch_rows: Iterable[dict], speed_rows: Iterable[dict], limit: int = 10) -> list[dict]:
    merged = Counter()

    for row in batch_rows:
        key = f"{row['wiki']}:{row['title']}"
        merged[key] += int(row["edit_count"])

    for row in speed_rows:
        key = f"{row['wiki']}:{row['title']}"
        merged[key] += int(row["edit_count"])

    return [
        {"page": page, "combined_edit_count": count}
        for page, count in merged.most_common(limit)
    ]

