# Performance Results

Date: 2026-07-28

## Local Speed-Layer Replay

Input file:

```text
data/raw/wikimedia_sample.jsonl
```

Sample size: 100 live Wikimedia recent-change records.

Command:

```powershell
$env:PYTHONPATH='.'
.venv\Scripts\python.exe benchmarks\local_speed_benchmark.py --input data\raw\wikimedia_sample.jsonl --runs 3
```

| Run | Events | Duration seconds | Events per second | Avg ms per event |
| --- | ---: | ---: | ---: | ---: |
| 1 | 100 | 0.0457 | 2187.21 | 0.4572 |
| 2 | 100 | 0.0020 | 50027.52 | 0.0200 |
| 3 | 100 | 0.0019 | 53766.34 | 0.0186 |

Final sample summary:

- top wikis: `commonswiki` 31, `wikidatawiki` 18, `enwiki` 16, `cewiki` 8, `eswiktionary` 7
- top namespaces: `0` 40, `14` 36, `6` 17, `4` 2, `10` 1
- event types: `edit` 62, `categorize` 33, `new` 3, `log` 2
- bot events: 36
- human events: 64
- anonymous events: 0
- logged-in events: 100
- minor events: 19
- non-minor events: 81

## Cloud Ingestion Proof

AWS CloudShell sent 25 live Wikimedia records to Kinesis and saved the same records to S3.

```text
Kinesis stream: wikimedia-recentchange-stream
S3 bucket: wikimedia-analytics-lokesh-24238856
S3 object: raw/live-demo/wikimedia-live-20260727-233528.jsonl
```

## Local Batch Preview

PySpark is included in `src/batch/spark_batch_views.py`, but the local Windows machine could not start Spark because Java/JAVA_HOME was missing.

For demo proof on the same dataset, the local preview command was run:

```powershell
.venv\Scripts\python.exe src\batch\simple_batch_preview.py --input data\raw\wikimedia_sample.jsonl --output data\processed\batch_preview
```

Output:

```text
events_read=100
views_written=top_pages,language_volume,hourly_volume,bot_summary
```
