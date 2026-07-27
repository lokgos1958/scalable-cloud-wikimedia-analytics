# Demo Video Script

## 1. Introduction

Hello, this is our Scalable Cloud Programming project. We built a real-time analytics pipeline for Wikimedia recent-change events using Python, AWS Kinesis, S3, and Spark.

## 2. Use Case

The question we answer is: which Wikipedia pages and wiki projects are trending in the last few minutes?

## 3. Architecture

Show the architecture diagram in `docs/architecture.md`.

Explain:

- Wikimedia stream is the data source.
- Python producer sends events to Kinesis.
- S3 stores raw event files.
- PySpark creates batch views.
- Speed layer creates recent sliding-window views.
- Serving layer combines batch and speed results.

## 4. AWS Setup

Show AWS console:

- Kinesis stream: `wikimedia-recentchange-stream`
- S3 bucket: `wikimedia-analytics-lokesh-24238856`

Mention that public access is blocked for the bucket.

## 5. Code Walkthrough

Show these files:

- `src/producer/wikimedia_kinesis_producer.py`
- `src/aws/kinesis_to_s3_consumer.py`
- `src/batch/spark_batch_views.py`
- `src/speed/sliding_window_analytics.py`
- `src/serving/merge_views.py`

Keep the explanation simple. Say what each script does in one or two lines.

## 6. Local Test

Run:

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests
```

Explain that the tests check the speed layer and serving layer.

## 7. Benchmark

Show the local speed benchmark command:

```powershell
.venv\Scripts\python.exe benchmarks/local_speed_benchmark.py --input data/raw/wikimedia_sample.jsonl --runs 3
```

Explain throughput and average milliseconds per event.

## 8. Closing

The project shows both correctness and freshness. The batch layer gives complete historical views, while the speed layer gives recent trending results.

