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

## Why This Step Matters

This local test is not the final cloud pipeline. It is only a first check before connecting the same stream to Kinesis and S3 in AWS Academy Learner Lab.

