"""Compute historical Wikimedia edit aggregates with PySpark."""

import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc, from_unixtime, to_date


def build_batch_views(input_path: str, output_path: str) -> None:
    spark = (
        SparkSession.builder.appName("wikimedia-batch-views")
        .getOrCreate()
    )

    events = spark.read.json(input_path)
    clean = events.where(col("title").isNotNull()).where(col("wiki").isNotNull())

    top_pages = (
        clean.groupBy("wiki", "title")
        .agg(count("*").alias("edit_count"))
        .orderBy(desc("edit_count"))
        .limit(100)
    )

    language_volume = (
        clean.withColumn("event_date", to_date(from_unixtime(col("timestamp"))))
        .groupBy("event_date", "wiki")
        .agg(count("*").alias("edit_count"))
        .orderBy("event_date", desc("edit_count"))
    )

    bot_summary = (
        clean.groupBy("bot")
        .agg(count("*").alias("edit_count"))
        .orderBy(desc("edit_count"))
    )

    top_pages.write.mode("overwrite").json(f"{output_path}/top_pages")
    language_volume.write.mode("overwrite").json(f"{output_path}/language_volume")
    bot_summary.write.mode("overwrite").json(f"{output_path}/bot_summary")

    spark.stop()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="S3 or local path containing raw JSON events")
    parser.add_argument("--output", required=True, help="S3 or local path for batch views")
    args = parser.parse_args()
    build_batch_views(args.input, args.output)


if __name__ == "__main__":
    main()

