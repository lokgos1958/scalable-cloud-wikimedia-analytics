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

## Note

The next stronger demo step is to run the full Wikimedia producer with fresh Learner Lab CLI credentials and then run the Kinesis-to-S3 consumer. The project code for that is already included in the repository.

