# Architecture

```mermaid
flowchart LR
    A["Wikimedia Event Streams"] --> B["Python Producer"]
    B --> C["Amazon Kinesis Data Streams"]
    C --> D["S3 Raw Event Archive"]
    D --> E["PySpark Batch Layer"]
    C --> F["Speed Layer Window Processor"]
    E --> G["Batch View"]
    F --> H["Recent Window View"]
    G --> I["Serving Layer Merge"]
    H --> I
    I --> J["Athena / Dashboard / Report Outputs"]
    K["EC2 Auto Scaling or EMR Managed Scaling"] --> E
    K --> F
```

## Batch View

The batch layer reads all accumulated events and computes complete historical aggregates:

- top edited pages
- top languages/projects
- bot vs human edit counts
- event volume per time interval

## Speed View

The speed layer updates recent aggregates over sliding windows:

- top pages in the last 1 minute
- top pages in the last 5 minutes
- event count per language in the current window

## Serving Merge

The serving layer combines:

- accurate historical results from the batch view
- fresh recent results from the speed view

This gives both correctness and low latency, which is the purpose of the Lambda architecture.

