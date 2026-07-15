# Progress Log

This log is maintained as daily evidence of steady project progress.

## 2026-07-09

- Selected final project topic: real-time Wikimedia edit analytics.
- Confirmed dataset source: Wikimedia Event Streams recent-change feed.
- Defined the main question: top trending pages and languages in recent windows.
- Created initial repository structure for ingestion, batch processing, speed processing, serving, and benchmarks.
- Added starter architecture and implementation files.

## 2026-07-13

- Added a small local script to save sample Wikimedia events as JSON-lines.
- Added local test notes for checking the live stream before using AWS.
- The local sample will help test the speed layer and batch layer without spending AWS lab time.

## 2026-07-15

- Added AWS setup notes for Learner Lab.
- Added `.env.example` to show which temporary AWS values are needed locally.
- Added a simple setup script for creating the first Kinesis stream and S3 bucket.
- Kept the setup small so it can be tested safely before moving to Spark and benchmarking.
