# AWS Screenshots For Report

Use these screenshots in the final IEEE report and demo slides/video.

## Recommended Images

1. `01_aws_console_home.png` - AWS Console in `us-east-1`.
2. `02_kinesis_stream_details.png` - Kinesis stream `wikimedia-recentchange-stream`, Active, on-demand.
3. `03_s3_bucket_objects.png` - S3 bucket object view.
4. `04_s3_live_demo_raw_object.png` - S3 `raw/live-demo/` object from the live Wikimedia run.
5. `05_cloudshell_kinesis_s3_output.png` - CloudShell proof for Kinesis stream and S3 live object.
6. `07_cloudshell_autoscaling_policy_success.png` - CloudShell proof for Auto Scaling Group and CPU target policy.
7. `08_ec2_auto_scaling_group_console.png` - EC2 Auto Scaling Group console view.
8. `09_ec2_auto_scaling_policy_tab.png` - Automatic scaling tab showing dynamic scaling policy area.

## Auto Scaling Configuration

The demo Auto Scaling Group is:

```text
Name: wikimedia-analytics-asg
Launch template: wikimedia-analytics-lt
Minimum capacity: 0
Maximum capacity: 2
Desired capacity during screenshot: 0
Policy: wikimedia-cpu-target-60
Policy type: TargetTrackingScaling
Metric: ASGAverageCPUUtilization
Target value: 60
```

The desired capacity was kept at `0` to avoid running unnecessary EC2 instances in AWS Academy Learner Lab while still showing the scaling boundary and policy configuration.
