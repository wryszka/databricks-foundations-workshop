# Databricks notebook source
# MAGIC %md
# MAGIC # D1 — A Spark Declarative Pipeline (Lakeflow / DLT)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** the transform layer that feeds the platform, written as
# MAGIC **declarative configuration** instead of hand-wired orchestration. You declare the
# MAGIC tables and their quality rules; the pipeline works out the order, incrementality and
# MAGIC error handling. This notebook **is** the pipeline definition — you don't "Run" it like
# MAGIC a normal notebook, you attach it to a **pipeline** (see the markdown at the bottom, and
# MAGIC lab D2 to schedule it).

# COMMAND ----------

import dlt
from pyspark.sql import functions as F

# The raw volume path is supplied by the pipeline's `configuration` (set when you create the
# pipeline). Fallback lets you edit/preview the file safely.
RAW = spark.conf.get("keystone.raw", "/Volumes/main/keystone/raw")

# COMMAND ----------

# MAGIC %md ## Bronze — raw as-is, plus ingest metadata

# COMMAND ----------

@dlt.table(comment="Raw motor policies exactly as received.")
def bronze_policies():
    return (
        spark.read.option("header", True).csv(f"{RAW}/policies.csv")
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.lit("policies.csv"))
    )

@dlt.table(comment="Raw motor claims exactly as received.")
def bronze_claims():
    return (
        spark.read.option("header", True).csv(f"{RAW}/claims.csv")
        .withColumn("_ingested_at", F.current_timestamp())
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver — typed, deduplicated, bad rows dropped by expectations
# MAGIC `expect_or_drop` quarantines rows that fail; the pipeline reports how many.

# COMMAND ----------

@dlt.table(comment="Cleaned, typed, deduplicated policies.")
@dlt.expect_or_drop("premium_positive", "annual_premium > 0")
@dlt.expect_or_drop("valid_start_date", "start_date IS NOT NULL")
def silver_policies():
    return (
        dlt.read("bronze_policies")
        .withColumn("annual_premium", F.col("annual_premium").cast("double"))
        .withColumn("driver_age", F.col("driver_age").cast("int"))
        .withColumn("engine_cc", F.col("engine_cc").cast("int"))
        .withColumn("start_date", F.to_date("start_date"))  # bad strings like 31/02/2025 -> NULL -> dropped
        .dropDuplicates(["policy_id"])
    )

@dlt.table(comment="Cleaned claims; the -1 placeholders are dropped.")
@dlt.expect_or_drop("incurred_non_negative", "incurred_amount >= 0")
def silver_claims():
    return (
        dlt.read("bronze_claims")
        .withColumn("incurred_amount", F.col("incurred_amount").cast("double"))
        .withColumn("claim_date", F.to_date("claim_date"))
    )

# COMMAND ----------

# MAGIC %md ## Gold — a per-tenant portfolio summary

# COMMAND ----------

@dlt.table(comment="Policies, GWP, claim frequency and incurred by tenant and region.")
def gold_portfolio_summary():
    p = dlt.read("silver_policies")
    c = dlt.read("silver_claims")
    return (
        p.join(c, "policy_id", "left")
        .groupBy(p.tenant, p.region, p.cover_type)
        .agg(
            F.countDistinct(p.policy_id).alias("policies"),
            F.round(F.sum(p.annual_premium), 2).alias("gwp"),
            F.count(c.claim_id).alias("claims"),
            F.round(F.coalesce(F.sum(c.incurred_amount), F.lit(0)), 2).alias("incurred"),
        )
        .withColumn("claim_frequency", F.round(F.col("claims") / F.col("policies"), 4))
    )

# COMMAND ----------

# MAGIC %md
# MAGIC ## How to run this as a pipeline
# MAGIC 1. **Workflows → Pipelines → Create pipeline** (or the ETL/Lakeflow entry in the sidebar).
# MAGIC 2. Source = this notebook. Set **serverless**, target **catalog** and **schema** to your
# MAGIC    own (e.g. `main` / `keystone_<you>`).
# MAGIC 3. Under **Configuration** add `keystone.raw` = `/Volumes/<catalog>/<schema>/raw`.
# MAGIC 4. **Start** — watch the DAG build bronze → silver → gold, with the dropped-row counts
# MAGIC    shown on each expectation.
# MAGIC
# MAGIC > 💡 **Genie Code:** you could prompt Genie Code to scaffold a pipeline like this from a
# MAGIC > plain-English description of the bronze/silver/gold layers.
# MAGIC
# MAGIC ✅ **Done.** Next: `D2 — schedule it as a job`.
