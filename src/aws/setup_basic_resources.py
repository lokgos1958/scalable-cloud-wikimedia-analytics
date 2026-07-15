"""Create the basic AWS resources for the project."""

import os
import time

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv


load_dotenv()


REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
STREAM_NAME = os.getenv("KINESIS_STREAM_NAME", "wikimedia-recentchange-stream")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "wikimedia-analytics-lokesh")


def create_stream():
    kinesis = boto3.client("kinesis", region_name=REGION)

    try:
        kinesis.create_stream(StreamName=STREAM_NAME, ShardCount=1)
        print(f"creating stream: {STREAM_NAME}")
    except ClientError as error:
        if error.response["Error"]["Code"] == "ResourceInUseException":
            print(f"stream already exists: {STREAM_NAME}")
        else:
            raise

    while True:
        details = kinesis.describe_stream_summary(StreamName=STREAM_NAME)
        status = details["StreamDescriptionSummary"]["StreamStatus"]
        print(f"stream status: {status}")
        if status == "ACTIVE":
            break
        time.sleep(10)


def create_bucket():
    s3 = boto3.client("s3", region_name=REGION)

    try:
        if REGION == "us-east-1":
            s3.create_bucket(Bucket=BUCKET_NAME)
        else:
            s3.create_bucket(
                Bucket=BUCKET_NAME,
                CreateBucketConfiguration={"LocationConstraint": REGION},
            )
        print(f"created bucket: {BUCKET_NAME}")
    except ClientError as error:
        code = error.response["Error"]["Code"]
        if code in ["BucketAlreadyOwnedByYou", "BucketAlreadyExists"]:
            print(f"bucket already exists or name is taken: {BUCKET_NAME}")
        else:
            raise


def main():
    print("setting up basic AWS resources")
    create_stream()
    create_bucket()
    print("basic AWS setup complete")


if __name__ == "__main__":
    main()

