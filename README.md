# Real-Time Wikipedia Edit Analytics

Scalable Cloud Programming CA project using Wikimedia Event Streams, Python, Apache Spark, and AWS Academy Learner Lab.

## Use Case

The system answers this real-time question:

> Which Wikipedia pages and languages are trending in the last few minutes?

Wikimedia recent-change events are continuously ingested into AWS, stored for historical analysis, processed through a batch layer and a speed layer, and exposed through a serving layer.

## Dataset

- Source: Wikimedia Event Streams
- Stream: `https://stream.wikimedia.org/v2/stream/recentchange`
- Type: true real-time Server-Sent Events stream
- Authentication: no API key required

## Target Architecture

- Ingestion: Python producer sends events to Amazon Kinesis Data Streams.
- Storage: Raw events are archived in Amazon S3.
- Batch layer: PySpark computes complete historical views from S3.
- Speed layer: Python/Spark windowed processing computes low-latency top-N trends.
- Serving layer: batch and speed views are merged for dashboard/reporting.
- Scaling: EC2 Auto Scaling Group or EMR managed scaling is benchmarked under different ingestion rates.

## Current Status

Day 1 project setup is complete:

- Project scope selected.
- Public streaming dataset selected.
- Lambda architecture documented.
- Starter producer, batch, and speed-layer scripts added.
- Progress log started for daily professor-visible updates.

## Planned Outputs

- IEEE double-column project report, maximum 10 pages.
- GitHub repository with source code and daily progress commits.
- Demo video showing live ingestion, batch layer, speed layer, serving view, and benchmark results.
- Benchmark graphs for throughput, latency, and speedup.

## Current Batch Outputs

The batch script currently writes four small JSON output folders:

- `top_pages` for overall page edit counts
- `language_volume` for daily wiki/project totals
- `hourly_volume` for hourly wiki/project totals
- `bot_summary` for bot vs non-bot counts
