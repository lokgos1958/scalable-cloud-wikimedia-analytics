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

These numbers are only local baseline measurements, but they are useful later when comparing local replay against AWS-based runs.

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

## Why This Step Matters

This local test is not the final cloud pipeline. It is only a first check before connecting the same stream to Kinesis and S3 in AWS Academy Learner Lab.
