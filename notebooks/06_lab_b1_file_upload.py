# Databricks notebook source
# MAGIC %md
# MAGIC # B1 — File upload to a Delta table
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** onboarding a new client's extract. A messy CSV arrives; land it
# MAGIC as-is (**bronze**), then clean and type it (**silver**).
# MAGIC
# MAGIC Fill in each `# TODO`. The complete version is in `solutions/`.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# MAGIC %md
# MAGIC ## The file is already in your `raw` volume
# MAGIC In real life you'd click **Catalog → your volume → Upload**. The generator placed a
# MAGIC deliberately messy `policies.csv` there — duplicate rows, a corrupted date
# MAGIC (`31/02/2025`), and some negative premiums.

# COMMAND ----------

print([f.name for f in dbutils.fs.ls(RAW_VOLUME)])

# COMMAND ----------

# MAGIC %md ## 1. Bronze — land the file as-is, plus lineage metadata

# COMMAND ----------

from pyspark.sql import functions as F

# TODO: read raw/policies.csv (header=True, all strings), add _ingest_file (from
# _metadata.file_path) and _ingest_ts, and save as table "1_bronze_policies".
# bronze = spark.read.option("header", True).csv(f"{RAW_VOLUME}/policies.csv") ...
# bronze.write.mode("overwrite").saveAsTable("1_bronze_policies")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Silver — types fixed, duplicates dropped, bad rows quarantined
# MAGIC - `try_cast(start_date AS date)` turns the corrupted date into NULL instead of failing
# MAGIC - drop duplicate `policy_id`
# MAGIC - drop rows with a NULL date or a non-positive premium

# COMMAND ----------

# TODO: build the clean silver DataFrame from 1_bronze_policies and save as
# "2_silver_policies". Cast the numeric columns, fix start_date, dropDuplicates(["policy_id"]),
# filter start_date IS NOT NULL AND annual_premium > 0.

# COMMAND ----------

# MAGIC %md
# MAGIC > 💡 **Genie Code:** prompt it — *"read raw/policies.csv, drop duplicates, fix the date,
# MAGIC > drop negative premiums, save as 2_silver_policies"*.

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: **B2 — Auto Loader**.
