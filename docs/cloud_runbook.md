# Cloud Runbook

This is the step-by-step AWS runbook for the final demo.

## 1. Start Learner Lab

1. Open AWS Academy Learner Lab.
2. Start the lab.
3. Copy the temporary CLI credentials into `.env`.
4. Keep the region as `us-east-1`.

## 2. Check AWS Resources

```powershell
.venv\Scripts\python.exe src/aws/check_resources.py
```

Expected result:

```text
aws_check: ok
```

## 3. Send Wikimedia Events To Kinesis

In one terminal:

```powershell
$env:MAX_RECORDS="200"
.venv\Scripts\python.exe src/producer/wikimedia_kinesis_producer.py
```

This sends a small live batch of Wikimedia recent-change events.

## 4. Save Kinesis Records To S3

After the producer sends records:

```powershell
.venv\Scripts\python.exe src/aws/kinesis_to_s3_consumer.py --max-records 100 --wait-seconds 120
```

Expected result:

```text
uploaded 100 records to s3://wikimedia-analytics-lokesh-24238856/raw/...
```

## 5. Run Batch Layer

The batch layer can read the raw S3 path and write processed views:

```powershell
spark-submit src/batch/spark_batch_views.py --input s3://wikimedia-analytics-lokesh-24238856/raw/ --output s3://wikimedia-analytics-lokesh-24238856/processed/batch/
```

For the report, record:

- input size
- processing time
- output folders created
- screenshots of S3 raw and processed folders

## 6. Run Speed Layer Locally

If AWS time is limited, use a small downloaded JSON-lines sample:

```powershell
.venv\Scripts\python.exe src/speed/sliding_window_analytics.py --input data/raw/wikimedia_sample.jsonl --window-seconds 300 --top-n 5
```

This demonstrates the same window logic used for the speed layer.

