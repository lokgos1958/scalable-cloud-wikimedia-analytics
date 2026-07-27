"""Small AWS check used before the demo."""

import os

import boto3
from dotenv import load_dotenv


load_dotenv()


REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
STREAM_NAME = os.getenv("KINESIS_STREAM_NAME", "wikimedia-recentchange-stream")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "wikimedia-analytics-lokesh-24238856")


def main():
    sts = boto3.client("sts", region_name=REGION)
    kinesis = boto3.client("kinesis", region_name=REGION)
    s3 = boto3.client("s3", region_name=REGION)

    account = sts.get_caller_identity()["Account"]
    stream = kinesis.describe_stream_summary(StreamName=STREAM_NAME)
    stream_status = stream["StreamDescriptionSummary"]["StreamStatus"]
    s3.head_bucket(Bucket=BUCKET_NAME)

    print(f"account: {account}")
    print(f"kinesis_stream: {STREAM_NAME}")
    print(f"kinesis_status: {stream_status}")
    print(f"s3_bucket: {BUCKET_NAME}")
    print("aws_check: ok")


if __name__ == "__main__":
    main()

