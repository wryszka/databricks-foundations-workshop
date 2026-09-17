# Databricks notebook source
# MAGIC %md
# MAGIC # D1 — A Spark Declarative Pipeline (Lakeflow / DLT)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** declare your bronze → silver → gold tables and their quality
# MAGIC rules; the pipeline handles order, incrementality and bad rows. This notebook **is** the
# MAGIC pipeline definition — attach it to a pipeline (instructions at the bottom), don't just
# MAGIC "Run" it. Fill in the `# TODO`s; answer in `solutions/17_solution_d1_pipeline`.

# COMMAND ----------

import dlt
from pyspark.sql import functions as F

RAW = spark.conf.get("keystone.raw", "/Volumes/main/keystone/raw")

# COMMAND ----------

# MAGIC %md ## Bronze — raw as-is

# COMMAND ----------

@dlt.table(comment="Raw motor policies exactly as received.")
def bronze_policies():
    # TODO: read {RAW}/policies.csv with header, add an _ingested_at timestamp
    return spark.read.option("header", True).csv(f"{RAW}/policies.csv")

# TODO: add a bronze_claims table reading {RAW}/claims.csv

# COMMAND ----------

# MAGIC %md ## Silver — typed, deduped, bad rows dropped via expectations

# COMMAND ----------

@dlt.table(comment="Cleaned policies.")
# TODO: @dlt.expect_or_drop("premium_positive", "annual_premium > 0")
# TODO: @dlt.expect_or_drop("valid_start_date", "start_date IS NOT NULL")
def silver_policies():
    # TODO: cast numeric cols, to_date(start_date) (bad strings -> NULL -> dropped), dropDuplicates(policy_id)
    return dlt.read("bronze_policies")

# TODO: add silver_claims (cast incurred_amount, drop where incurred_amount < 0)

# COMMAND ----------

# MAGIC %md ## Gold — per-tenant portfolio summary

# COMMAND ----------

# TODO: gold_portfolio_summary joining silver_policies + silver_claims, aggregated by
#       tenant/region/cover_type (policies, gwp, claims, incurred, claim_frequency)

# COMMAND ----------

# MAGIC %md
# MAGIC **Run it:** Workflows → Pipelines → Create, source = this notebook, serverless, set
# MAGIC target catalog/schema, add config `keystone.raw = /Volumes/<catalog>/<schema>/raw`,
# MAGIC then Start.
# MAGIC
# MAGIC ✅ **Done.** Next: `D2 — schedule it as a job`.
