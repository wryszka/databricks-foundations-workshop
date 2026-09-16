# Databricks notebook source
# MAGIC %md
# MAGIC # B1 — File upload to a Delta table
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** onboarding a new client's extract. A messy CSV arrives; you land
# MAGIC it as-is (**bronze**), then clean and type it (**silver**). This is the pattern every
# MAGIC ingest on Keystone follows.

# COMMAND ----------

# MAGIC %run ../notebooks/00_config

# COMMAND ----------

# MAGIC %md
# MAGIC ## The file is already in your `raw` volume
# MAGIC In real life you'd click **Catalog → your volume → Upload** (or drag a file in). The
# MAGIC data generator has placed a deliberately messy `policies.csv` there for you — duplicate
# MAGIC rows, a corrupted date (`31/02/2025`), and some negative premiums.

# COMMAND ----------

files = dbutils.fs.ls(RAW_VOLUME)
print([f.name for f in files])

# COMMAND ----------

# MAGIC %md ## 1. Bronze — land the file exactly as it arrived, plus lineage metadata

# COMMAND ----------

from pyspark.sql import functions as F

bronze = (
    spark.read.option("header", True).csv(f"{RAW_VOLUME}/policies.csv")   # everything as strings
    .withColumn("_ingest_file", F.col("_metadata.file_path"))
    .withColumn("_ingest_ts", F.current_timestamp())
)
bronze.write.mode("overwrite").saveAsTable("1_bronze_policies")
print(f"bronze rows (with duplicates and bad rows): {spark.table('1_bronze_policies').count():,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Silver — types fixed, duplicates dropped, bad rows quarantined
# MAGIC - `try_cast` turns the corrupted date into `NULL` instead of failing the whole load
# MAGIC - drop duplicate `policy_id`s
# MAGIC - drop rows with a broken date or a non-positive premium

# COMMAND ----------

silver = (
    spark.table("1_bronze_policies")
    .withColumn("driver_age", F.col("driver_age").cast("int"))
    .withColumn("ncd_years", F.col("ncd_years").cast("int"))
    .withColumn("penalty_points", F.col("penalty_points").cast("int"))
    .withColumn("engine_cc", F.col("engine_cc").cast("int"))
    .withColumn("annual_premium", F.col("annual_premium").cast("double"))
    .withColumn("start_date", F.expr("try_cast(start_date AS date)"))
    .dropDuplicates(["policy_id"])
    .filter("start_date IS NOT NULL AND annual_premium > 0")
    .select("policy_id", "tenant", "region", "driver_age", "ncd_years", "penalty_points",
            "vehicle_make", "engine_cc", "cover_type", "start_date", "annual_premium")
)
silver.write.mode("overwrite").saveAsTable("2_silver_policies")

n_bronze = spark.table("1_bronze_policies").count()
n_silver = spark.table("2_silver_policies").count()
print(f"bronze {n_bronze:,} -> silver {n_silver:,}  (dropped {n_bronze - n_silver:,} duplicate/bad rows)")
display(spark.table("2_silver_policies").limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC > 💡 **Genie Code:** you could prompt it — *"read raw/policies.csv, drop duplicate
# MAGIC > policy_id, fix the date, drop negative premiums, save as 2_silver_policies"* — and
# MAGIC > it writes this cleaning code for you.

# COMMAND ----------

# MAGIC %md ✅ **Done.** A messy file is now a clean, typed silver table. Next: **B2 — Auto Loader**.
