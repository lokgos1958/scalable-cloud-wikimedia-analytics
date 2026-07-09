# Project Plan

## Assessment Fit

This project follows the Scalable Cloud Programming CA requirement to build a Python-based scalable cloud computing system using AWS Academy Learner Lab.

The implementation uses a Lambda architecture:

- Batch layer for correct full-history analytics.
- Speed layer for recent low-latency trends.
- Serving layer to combine both views.
- Auto-scaling boundary around compute workers.

## Two-Person Work Allocation

Although the implementation is being coordinated together, the report can present the work as two clear contribution streams.

### Student 1: Cloud Ingestion and Infrastructure

- AWS Kinesis Data Stream setup.
- S3 raw event storage.
- Architecture diagram and AWS service configuration.
- Auto-scaling policy setup and screenshots.
- Demo section for records flowing through the ingestion path.

### Student 2: Processing, Serving, and Benchmarking

- PySpark batch layer.
- Speed-layer sliding-window analytics.
- Serving layer merge logic.
- Benchmark scripts and graphs.
- Results and critical analysis sections.

## Daily Build Plan

| Day | Target |
| --- | --- |
| Day 1 | Repository setup, use case, dataset, architecture draft |
| Day 2 | Local stream consumer and sample event capture |
| Day 3 | Kinesis producer and AWS setup notes |
| Day 4 | S3 raw storage path and replayable sample data |
| Day 5 | PySpark batch aggregation |
| Day 6 | Speed-layer sliding-window top-N analytics |
| Day 7 | Serving view merge |
| Day 8 | Benchmark harness for throughput and latency |
| Day 9 | Scaling experiment documentation |
| Day 10 | Report draft and demo script |

