"""Stream Wikimedia recent-change events into Amazon Kinesis."""

import json
import os
import time
from typing import Iterable

import boto3
import requests


STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"


def iter_wikimedia_events() -> Iterable[dict]:
    """Yield parsed Wikimedia Server-Sent Events."""
    with requests.get(STREAM_URL, stream=True, timeout=30) as response:
        response.raise_for_status()
        for raw_line in response.iter_lines(decode_unicode=True):
            if not raw_line or not raw_line.startswith("data: "):
                continue
            payload = raw_line.removeprefix("data: ").strip()
            if payload:
                yield json.loads(payload)


def compact_event(event: dict) -> dict:
    """Keep only fields needed by the analytics pipeline."""
    return {
        "id": event.get("id"),
        "timestamp": event.get("timestamp"),
        "wiki": event.get("wiki"),
        "title": event.get("title"),
        "type": event.get("type"),
        "bot": event.get("bot"),
        "minor": event.get("minor"),
        "user": event.get("user"),
        "server_name": event.get("server_name"),
    }


def main() -> None:
    stream_name = os.environ["KINESIS_STREAM_NAME"]
    region = os.getenv("AWS_REGION", "us-east-1")
    max_records = int(os.getenv("MAX_RECORDS", "0"))
    delay_seconds = float(os.getenv("PRODUCER_DELAY_SECONDS", "0"))

    kinesis = boto3.client("kinesis", region_name=region)

    sent = 0
    for event in iter_wikimedia_events():
        record = compact_event(event)
        kinesis.put_record(
            StreamName=stream_name,
            Data=json.dumps(record).encode("utf-8"),
            PartitionKey=record.get("wiki") or "unknown",
        )
        sent += 1
        if sent % 100 == 0:
            print(f"sent_records={sent}")
        if max_records and sent >= max_records:
            break
        if delay_seconds:
            time.sleep(delay_seconds)


if __name__ == "__main__":
    main()

