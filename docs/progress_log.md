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
- Added a small local benchmark script for replaying Wikimedia sample events through the speed-layer logic.
- Recorded simple benchmark outputs such as replay time, events per second, and average milliseconds per event.
- Updated the local test notes so the benchmark step can be repeated before AWS resources are available.

## 2026-07-16

- Added a small unittest-based replay check for the speed-layer logic.
- Verified that valid events are counted, incomplete records are ignored, and top pages are returned correctly.
- Updated the local test notes with the replay-check command so the local validation step is easy to repeat.

## 2026-07-19

- Extended the local speed-layer replay summary to report top wiki/project counts in the active window.
- Updated the local benchmark output so each run now includes the final wiki-count snapshot.
- Expanded the replay test to check the new wiki-count summary for valid and empty inputs.
- Updated the local test notes to explain how this small step supports the later speed-layer language/project metric.

## 2026-07-20

- Improved the serving-layer merge so each merged result now keeps the wiki, page title, batch count, speed count, and combined count.
- Added a small unittest file for the serving-layer merge to check overlapping pages and the result limit.
- Updated the local test notes so the lightweight unittest command now also covers the serving view logic.
- Extended the PySpark batch layer to also write an `hourly_volume` view grouped by hour and wiki/project.
- Updated the README, architecture notes, and local test notes to show the new hourly batch output and a simple local Spark smoke-test command.

## 2026-07-22

- Extended the local speed-layer replay so each active window now keeps a simple bot vs human event split.
- Updated the local benchmark output so each run also reports the final bot and human counts beside the top wiki counts.
- Expanded the replay unittest to check the new bot-count summary for both valid and empty sample inputs.
- Updated the README, architecture notes, and local test notes so this small speed-layer metric is documented for the demo and report.
- Created the first AWS resources in Learner Lab using the console: one Kinesis data stream and one S3 bucket.
- Confirmed the Kinesis stream reached Active status and kept S3 public access blocked.
- Updated the AWS notes with the actual resource names for the next live ingestion test.
