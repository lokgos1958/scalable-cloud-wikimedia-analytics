"""Read a few Kinesis records and save them to S3 as a JSON-lines file."""

import argparse
import datetime as dt
import json
import os
import time

import boto3
from dotenv import load_dotenv


load_dotenv()


REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
STREAM_NAME = os.getenv("KINESIS_STREAM_NAME", "wikimedia-recentchange-stream")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "wikimedia-analytics-lokesh-24238856")


def get_first_shard_id(kinesis):
    response = kinesis.list_shards(StreamName=STREAM_NAME)
    shards = response.get("Shards", [])
    if not shards:
        raise RuntimeError("No shards found for the stream")
    return shards[0]["ShardId"]


def read_records(max_records, wait_seconds):
    kinesis = boto3.client("kinesis", region_name=REGION)
    shard_id = get_first_shard_id(kinesis)

    iterator_response = kinesis.get_shard_iterator(
        StreamName=STREAM_NAME,
        ShardId=shard_id,
        ShardIteratorType="TRIM_HORIZON",
    )
    shard_iterator = iterator_response["ShardIterator"]

    records = []
    deadline = time.time() + wait_seconds

    while len(records) < max_records and time.time() < deadline:
        response = kinesis.get_records(ShardIterator=shard_iterator, Limit=100)
        shard_iterator = response.get("NextShardIterator")

        for item in response.get("Records", []):
            data = item["Data"].decode("utf-8")
            records.append(json.loads(data))
            if len(records) >= max_records:
                break

        if not response.get("Records"):
            time.sleep(2)

    return records


def upload_records_to_s3(records):
    if not records:
        print("No records found to upload")
        return None

    s3 = boto3.client("s3", region_name=REGION)
    today = dt.datetime.utcnow().strftime("%Y-%m-%d")
    timestamp = dt.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    key = f"raw/wikimedia/date={today}/events-{timestamp}.jsonl"

    body = "\n".join(json.dumps(record) for record in records) + "\n"
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=body.encode("utf-8"),
        ContentType="application/json",
    )

    print(f"uploaded {len(records)} records to s3://{BUCKET_NAME}/{key}")
    return key


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-records", type=int, default=50)
    parser.add_argument("--wait-seconds", type=int, default=90)
    args = parser.parse_args()

    records = read_records(args.max_records, args.wait_seconds)
    upload_records_to_s3(records)


if __name__ == "__main__":
    main()

