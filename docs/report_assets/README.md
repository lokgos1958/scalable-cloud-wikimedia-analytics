# Report Graphs And Batch Proof Images

Use these files in the final IEEE report.

## Graphs

- `graph_speed_throughput.png` - speed-layer throughput for three replay runs.
- `graph_speed_latency.png` - average milliseconds per event for the same replay runs.
- `graph_event_type_mix.png` - final event-type mix from the 100-event sample window.
- `graph_autoscaling_capacity.png` - configured EC2 Auto Scaling boundary.

## Batch Proof Images

- `spark_batch_preview_output.png` - local batch preview output showing four batch-view folders.
- `spark_java_requirement_output.png` - PySpark local run limitation showing Java/JAVA_HOME requirement.

## Note For Report

The PySpark implementation is included in `src/batch/spark_batch_views.py`. The local Windows demo machine could not start Spark because Java/JAVA_HOME was missing, so `simple_batch_preview.py` was used to show the same output structure on the 100-record Wikimedia sample.
