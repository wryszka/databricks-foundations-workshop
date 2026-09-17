# Databricks notebook source
# MAGIC %md
# MAGIC # B2 — Auto Loader: an incremental CSV pipeline
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** files keep arriving. **Auto Loader** watches a folder and picks up
# MAGIC **only new files**. Load one batch, drop a second file in, watch just that one flow through.
# MAGIC
# MAGIC Fill in each `# TODO`. The complete version is in `solutions/`.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# Reset so this lab is repeatable.
CHK = f"{LANDING_VOLUME}/_chk/claims"
SCHEMA_LOC = f"{LANDING_VOLUME}/_schema/claims"
for p in (CHK, SCHEMA_LOC):
    try: dbutils.fs.rm(p, True)
    except Exception: pass
spark.sql("DROP TABLE IF EXISTS 1_bronze_incoming_claims")
try: dbutils.fs.rm(f"{LANDING_VOLUME}/claims/claims_batch_02.csv")
except Exception: pass
print("landing/claims now holds:", [f.name for f in dbutils.fs.ls(f"{LANDING_VOLUME}/claims")])

# COMMAND ----------

# MAGIC %md ## 1. Point Auto Loader at the folder and load what's there

# COMMAND ----------

from pyspark.sql import functions as F

def run_autoloader():
    # TODO: complete the cloudFiles reader:
    #   .format("cloudFiles")
    #   .option("cloudFiles.format", "csv")
    #   .option("cloudFiles.schemaLocation", SCHEMA_LOC)
    #   .option("header", "true").option("cloudFiles.inferColumnTypes", "true")
    #   .load(f"{LANDING_VOLUME}/claims")
    stream = spark.readStream  # ... complete this
    # TODO: writeStream with .trigger(availableNow=True), checkpointLocation=CHK,
    #       .toTable("1_bronze_incoming_claims"); then q.awaitTermination()

run_autoloader()
print(f"after batch 1: {spark.table('1_bronze_incoming_claims').count():,} rows")

# COMMAND ----------

# MAGIC %md ## 2. A new file lands — drop `claims_batch_02.csv` in

# COMMAND ----------

dbutils.fs.cp(f"{RAW_VOLUME}/claims_batch_02.csv", f"{LANDING_VOLUME}/claims/claims_batch_02.csv")
print([f.name for f in dbutils.fs.ls(f"{LANDING_VOLUME}/claims")])

# COMMAND ----------

# MAGIC %md ## 3. Run again — only the new file is picked up

# COMMAND ----------

before = spark.table("1_bronze_incoming_claims").count()
run_autoloader()
after = spark.table("1_bronze_incoming_claims").count()
print(f"rows {before:,} -> {after:,}  (only the new file's rows were added)")

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: **B3 — MERGE & Change Data Feed**.
