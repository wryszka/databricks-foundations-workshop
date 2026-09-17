# Databricks notebook source
# MAGIC %md
# MAGIC # B2 — Auto Loader: an incremental CSV pipeline
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** files keep arriving. Instead of reprocessing everything each time,
# MAGIC **Auto Loader** watches a folder and picks up **only new files**. You'll load one batch,
# MAGIC then drop a second file in and watch just that one flow through.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

# COMMAND ----------

# Reset so this lab is repeatable: clear the checkpoint/schema state and target table,
# and make sure only batch_01 is in the landing folder to start.
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
    """Read any *new* files in landing/claims and append them to the bronze table."""
    stream = (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.schemaLocation", SCHEMA_LOC)
        .option("header", "true")
        .option("cloudFiles.inferColumnTypes", "true")
        .load(f"{LANDING_VOLUME}/claims")
        .withColumn("_ingest_file", F.col("_metadata.file_path"))
    )
    q = (stream.writeStream
         .trigger(availableNow=True)               # process available files, then stop
         .option("checkpointLocation", CHK)
         .toTable("1_bronze_incoming_claims"))
    q.awaitTermination()

run_autoloader()
print(f"after batch 1: {spark.table('1_bronze_incoming_claims').count():,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. A new file lands — drop `claims_batch_02.csv` into the folder
# MAGIC In a real system a source drops the next file automatically. Here we copy the staged
# MAGIC file from `raw/` into the landing folder.

# COMMAND ----------

dbutils.fs.cp(f"{RAW_VOLUME}/claims_batch_02.csv", f"{LANDING_VOLUME}/claims/claims_batch_02.csv")
print("landing/claims now holds:", [f.name for f in dbutils.fs.ls(f"{LANDING_VOLUME}/claims")])

# COMMAND ----------

# MAGIC %md ## 3. Run again — Auto Loader picks up *only* the new file

# COMMAND ----------

before = spark.table("1_bronze_incoming_claims").count()
run_autoloader()
after = spark.table("1_bronze_incoming_claims").count()
print(f"rows {before:,} -> {after:,}  (only the new file's {after - before:,} rows were added)")

# COMMAND ----------

# MAGIC %md
# MAGIC The checkpoint remembers which files it has seen, so batch 1 was **not** reprocessed.
# MAGIC That is the whole point: incremental, exactly-once file ingestion with no bookkeeping
# MAGIC on your side.
# MAGIC
# MAGIC > 💡 **Genie Code:** prompt it for "an Auto Loader stream from this folder into a bronze
# MAGIC > table" and it scaffolds the `cloudFiles` reader for you.

# COMMAND ----------

# MAGIC %md ✅ **Done.** New files flow in automatically. Next: **B3 — MERGE & Change Data Feed**.
