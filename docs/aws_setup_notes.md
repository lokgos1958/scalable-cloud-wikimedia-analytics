# AWS Setup Notes

These are the simple AWS services needed for the project.

## Services Used

- Amazon Kinesis Data Streams: receives live Wikimedia events.
- Amazon S3: stores raw event files and processed outputs.
- EC2 or EMR: runs Python and Spark processing.
- Athena or downloaded CSV files: used later for checking results.

## Learner Lab Steps

1. Open AWS Academy Learner Lab.
2. Start the lab session.
3. Copy the temporary AWS CLI credentials.
4. Put the credentials in a local `.env` file.
5. Do not commit `.env` to GitHub.

## First Cloud Test

The first cloud test will be small:

- create one Kinesis stream
- create one S3 bucket
- send a few Wikimedia records to Kinesis
- confirm the records are visible in AWS

This keeps the test simple before moving to Spark and scaling.

## Resource Names

Planned names:

```text
Kinesis stream: wikimedia-recentchange-stream
S3 bucket: wikimedia-analytics-lokesh
Region: us-east-1
```

If a bucket name is already taken, add a short suffix such as student ID or date.

