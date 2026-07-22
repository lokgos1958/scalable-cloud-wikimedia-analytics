# Local Test Notes

Before using AWS, the stream can be tested locally. This is useful because it proves that the dataset is live and that the project code can read real Wikimedia events.

## Save A Small Sample

```powershell
python src/producer/save_sample_events.py --max-records 100
```

This creates:

```text
data/raw/wikimedia_sample.jsonl
```

The file is ignored by Git because it is generated data.

## Test The Speed Layer

```powershell
python src/speed/sliding_window_analytics.py --input data/raw/wikimedia_sample.jsonl --window-seconds 300 --top-n 5
```

Expected output is a few JSON lines showing the current window size and the top edited pages in that sample.

It now also shows the busiest wiki projects in the same active window. This is a simple local version of the language/project count that will later be useful in the speed layer.

The replay output also includes the busiest event types in the same active window, such as normal edits versus new-page events. This is a small but useful speed-layer check because it shows whether short windows are dominated by one kind of change.

The replay output now also includes a small bot vs human split for the active window. That makes it easier to compare short-term automation activity against normal editor activity before the same idea is moved into the cloud pipeline.

## Run A Small Local Benchmark

```powershell
python -m benchmarks.local_speed_benchmark --input data/raw/wikimedia_sample.jsonl --runs 3
```

This replays the same sample file a few times and prints:

- processed events
- total replay time
- events per second
- average milliseconds per event
- final top wiki counts in the active window
- final top event-type counts in the active window
- final bot vs human counts in the active window

These numbers are only local baseline measurements, but they are useful later when comparing local replay against AWS-based runs.

## Run The Batch Layer Locally

If PySpark is installed, the same sample file can also be used to test the batch layer on a very small dataset:

```powershell
python src/batch/spark_batch_views.py --input data/raw/wikimedia_sample.jsonl --output data/batch_views
```

This should create small output folders for:

- top page counts
- daily wiki/project totals
- hourly wiki/project totals
- bot vs non-bot counts

This is still only a local smoke test, but it helps confirm that the batch script now produces both daily and hourly views before moving the same job to S3 input in AWS.

## Run A Simple Replay Check

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

This checks that the replay logic:

- counts valid events
- ignores incomplete records
- returns the expected top pages from a small JSON-lines sample

It is a lightweight local check, but it helps show that the speed-layer replay code still behaves as expected after small edits.

The same test command now also checks that the serving-layer merge keeps batch counts, speed counts, and combined counts aligned for the same page.
It also checks that the speed-layer replay keeps both the event-type counts and the bot vs human counts correct for a small sample window.

## Why This Step Matters

This local test is not the final cloud pipeline. It is only a first check before connecting the same stream to Kinesis and S3 in AWS Academy Learner Lab.
