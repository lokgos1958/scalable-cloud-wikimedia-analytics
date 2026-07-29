# Real-Time Wikipedia Edit Analytics Using AWS Lambda Architecture

## Abstract

This project builds a small scalable cloud analytics pipeline for Wikimedia recent-change events. The system ingests a live stream, stores raw events, computes full-history batch views, and also produces recent window-based speed views. The aim is to answer which pages and wiki projects are trending in near real time.

## 1. Introduction

Wikimedia projects receive continuous edits from logged-in users, anonymous users, and bots. This makes the recent-change stream a good public dataset for testing real-time analytics. The main question for this project is: which Wikipedia pages and wiki projects are most active in the last few minutes?

## 2. Dataset

The dataset is Wikimedia Event Streams recent-change data. It is a public Server-Sent Events stream and does not need an API key. Each record includes fields such as wiki, title, namespace, event type, bot flag, anonymous flag, minor flag, and timestamp.

## 3. Architecture

The project uses a Lambda architecture:

- ingestion layer: Python producer reads Wikimedia events and writes to Amazon Kinesis
- storage layer: raw event files are stored in Amazon S3
- batch layer: PySpark computes complete historical views
- speed layer: sliding-window logic computes recent top pages and counts
- serving layer: batch and speed results are merged into one view

This design is useful because the batch layer gives complete results over all stored data, while the speed layer gives fresh recent results.

## 4. Implementation

The producer script reads Wikimedia events and sends compact records to Kinesis. A separate consumer reads Kinesis records and uploads them to S3 as JSON-lines files. The batch layer reads JSON data using PySpark and writes four output views: top pages, daily wiki volume, hourly wiki volume, and bot summary.

The speed layer replays JSON-lines events and keeps a sliding window in memory. It reports top pages, top wiki projects, namespaces, event types, bot vs human counts, anonymous vs logged-in counts, and minor vs non-minor counts.

## 5. AWS Resources

The first AWS resources created in Learner Lab were:

- Kinesis stream: `wikimedia-recentchange-stream`
- S3 bucket: `wikimedia-analytics-lokesh-24238856`
- Region: `us-east-1`

The Kinesis stream was configured with on-demand capacity. S3 public access was kept blocked.

A CloudShell check confirmed that the stream and bucket were available. One small demo record was sent into Kinesis, and one JSON-lines file was uploaded to the S3 raw folder as first proof that the storage path works.

A stronger live CloudShell run then connected to the Wikimedia recent-change stream, sent 25 live records to Kinesis, and saved the same records to:

```text
s3://wikimedia-analytics-lokesh-24238856/raw/live-demo/wikimedia-live-20260727-233528.jsonl
```

For the auto-scaling requirement, an EC2 Auto Scaling Group named `wikimedia-analytics-asg` was configured with launch template `wikimedia-analytics-lt`. The group has minimum capacity `0`, maximum capacity `2`, and a target tracking policy named `wikimedia-cpu-target-60` using `ASGAverageCPUUtilization` with a target value of `60`. Desired capacity was kept at `0` during evidence capture to avoid running unnecessary EC2 instances in Learner Lab.

## 6. Performance Plan

The measurements used in the prototype are:

- throughput: records processed per second
- latency: time taken by the speed-layer replay
- output correctness: speed-layer and serving-layer unit tests
- batch output shape: local batch preview folders

For the local benchmark, 100 live Wikimedia sample records were replayed three times. The runs processed the sample at about 2187, 50028, and 53766 events per second. The final sample window had 36 bot events, 64 human events, 19 minor edits, and 81 non-minor edits.

The PySpark batch script is included for the main batch layer. For the local Windows demo setup, a small `simple_batch_preview.py` script was also used so the batch output shape could be verified without requiring a full local Java/Spark installation. It was run on the same 100-record sample and wrote `top_pages`, `language_volume`, `hourly_volume`, and `bot_summary` folders.

## 7. Critical Analysis

The Lambda architecture is appropriate because this stream needs both fresh and complete analytics. A batch-only design would not answer recent trends quickly. A stream-only design would be fast but weaker for full historical accuracy. The main bottlenecks are likely to be Kinesis read/write rate, Spark startup time for small data, and AWS Learner Lab limits.

## 8. Conclusion

The project demonstrates the main parts of a scalable real-time analytics system: live ingestion, cloud storage, batch processing, speed processing, and serving output. The implementation is intentionally small enough for AWS Academy Learner Lab but still follows the same architecture used in larger streaming systems.

## References

- Wikimedia Event Streams recentchange endpoint
- AWS Kinesis Data Streams documentation
- AWS S3 documentation
- Apache Spark documentation
