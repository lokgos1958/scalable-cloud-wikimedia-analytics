# Performance Results Template

Use this page to record the final benchmark numbers.

## Local Speed-Layer Replay

| Run | Events | Duration seconds | Events per second | Avg ms per event |
| --- | ---: | ---: | ---: | ---: |
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |

Command:

```powershell
.venv\Scripts\python.exe benchmarks/local_speed_benchmark.py --input data/raw/wikimedia_sample.jsonl --runs 3
```

## Producer Load Test

| Test | Delay seconds | Max records | Approx records/sec | Notes |
| --- | ---: | ---: | ---: | --- |
| Slow stream | 0.50 | 100 |  |  |
| Medium stream | 0.10 | 200 |  |  |
| Fast stream | 0.00 | 500 |  |  |

Commands:

```powershell
$env:MAX_RECORDS="100"
$env:PRODUCER_DELAY_SECONDS="0.50"
.venv\Scripts\python.exe src/producer/wikimedia_kinesis_producer.py
```

## Batch Layer Timing

| Worker count | Input records | Runtime seconds | Speedup |
| ---: | ---: | ---: | ---: |
| 1 |  |  | 1.00 |
| 2 |  |  |  |
| 3 |  |  |  |

Speedup formula:

```text
speedup = runtime_with_1_worker / runtime_with_n_workers
```

## Graphs To Add To Report

- latency vs ingestion rate
- throughput over time
- speedup vs worker count

Simple graph titles:

- Speed Layer Latency Under Different Loads
- Producer Throughput For Wikimedia Events
- Batch Layer Speedup With More Workers

