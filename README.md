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
- Scaling: EC2 Auto Scaling Group boundary is configured for the cloud demo.

## Current Status

Final prototype work is complete:

- Public Wikimedia live dataset selected and tested.
- Kinesis stream and S3 bucket created in AWS Learner Lab.
- Live Wikimedia records were sent to Kinesis from AWS CloudShell.
- Live sample records were saved to S3.
- Local speed-layer benchmark was run on 100 recent-change events.
- Local batch preview was run on the same 100-event sample.
- Unit tests cover the speed-layer replay and serving merge logic.

## Project Outputs

- IEEE double-column project report, maximum 10 pages.
- GitHub repository with source code and daily progress commits.
- Demo video showing live ingestion, batch layer, speed layer, serving view, and benchmark results.
- Report graphs for throughput, latency, event-type mix, and auto-scaling capacity.

## Main Run Commands

Check AWS resources:

```powershell
.venv\Scripts\python.exe src/aws/check_resources.py
```

Send a small live batch to Kinesis:

```powershell
$env:MAX_RECORDS="200"
.venv\Scripts\python.exe src/producer/wikimedia_kinesis_producer.py
```

Read Kinesis records and save them to S3:

```powershell
.venv\Scripts\python.exe src/aws/kinesis_to_s3_consumer.py --max-records 100 --wait-seconds 120
```

Run local tests:

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests
```

Run the local batch preview without Java:

```powershell
.venv\Scripts\python.exe src/batch/simple_batch_preview.py --input data/raw/wikimedia_sample.jsonl --output data/processed/batch_preview
```

Run the PySpark batch job when Java is available:

```powershell
.venv\Scripts\python.exe src/batch/spark_batch_views.py --input data/raw/wikimedia_sample.jsonl --output data/processed/batch_test
```

## Current Batch Outputs

The batch script currently writes four small JSON output folders:

- `top_pages` for overall page edit counts
- `language_volume` for daily wiki/project totals
- `hourly_volume` for hourly wiki/project totals
- `bot_summary` for bot vs non-bot counts

## Current Speed Outputs

The local speed-layer replay currently reports:

- top edited pages in the active window
- top wiki/project counts in the active window
- top namespace counts in the active window
- top event types in the active window
- bot vs human event counts in the active window
- anonymous vs logged-in edit counts in the active window
- minor vs non-minor edit counts in the active window
- unique editors and repeat-editor counts in the active window
