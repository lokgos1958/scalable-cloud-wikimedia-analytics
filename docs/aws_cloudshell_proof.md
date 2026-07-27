# AWS CloudShell Proof

Date: 2026-07-28

This check was done in AWS Academy Learner Lab using AWS Console CloudShell.

## Resource Check

Kinesis stream checked:

```text
wikimedia-recentchange-stream
```

S3 bucket checked:

```text
wikimedia-analytics-lokesh-24238856
```

The S3 bucket check returned the bucket ARN and region:

```text
arn:aws:s3:::wikimedia-analytics-lokesh-24238856
us-east-1
```

## Kinesis Demo Record

One small demo edit record was sent to the Kinesis stream from CloudShell.

The command returned a Kinesis sequence number. This confirms that the stream accepted the record.

## S3 Demo File

One JSON-lines demo file was uploaded to S3:

```text
s3://wikimedia-analytics-lokesh-24238856/raw/manual-demo/wikimedia-demo.jsonl
```

The S3 listing showed:

```text
2026-07-27 23:26:39 105 wikimedia-demo.jsonl
```

## Live Wikimedia CloudShell Run

A stronger live run was also completed from AWS CloudShell.

The script connected to the Wikimedia recent-change event stream, sent 25 live records into Kinesis, and saved the same 25 records to S3.

Kinesis result:

```text
live_records_sent_to_kinesis 25
```

S3 result:

```text
s3://wikimedia-analytics-lokesh-24238856/raw/live-demo/wikimedia-live-20260727-233528.jsonl
```

The output showed real Wikimedia events from projects such as `eswiktionary`, `commonswiki`, `wikidatawiki`, and `enwiki`.

## Note

The next optional step is to run the repository Kinesis-to-S3 consumer for a larger sample. For the current submission prototype, the live CloudShell run proves the Kinesis and S3 path using real Wikimedia events.
