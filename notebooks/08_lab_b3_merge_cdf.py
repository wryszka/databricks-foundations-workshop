# Databricks notebook source
# MAGIC %md
# MAGIC # B3 — Upserts with MERGE (and reading the changes)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** a source keeps changing. `MERGE` applies updates and inserts in
# MAGIC one statement, and **Change Data Feed** lets you read exactly which rows changed.
# MAGIC
# MAGIC Fill in each `# TODO`. The complete version is in `solutions/`.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# MAGIC %md ## 1. A target table with Change Data Feed switched on

# COMMAND ----------

from pyspark.sql import functions as F

spark.sql("DROP TABLE IF EXISTS 2_silver_claims_cdf")
# TODO: create 2_silver_claims_cdf from 800 rows of 2_silver_claims WITH Change Data Feed on.
# Hint: .option("delta.enableChangeDataFeed", "true") on the write, or ALTER TABLE ... SET
#       TBLPROPERTIES (delta.enableChangeDataFeed = true).
print(f"target rows: {spark.table('2_silver_claims_cdf').count():,}")

# COMMAND ----------

# MAGIC %md ## 2. A batch of changes — some updates, some new claims

# COMMAND ----------

existing = spark.table("2_silver_claims_cdf").limit(100)
updates = (existing.withColumn("status", F.lit("settled"))
                   .withColumn("incurred_amount", F.round(F.col("incurred_amount") * 1.10, 2)))
new_claims = (spark.range(50)
    .withColumn("claim_id", F.format_string("CLM-NEW-%04d", F.col("id")))
    .withColumn("policy_id", F.lit("POL-0000001")).withColumn("tenant", F.lit("bricksurance_se"))
    .withColumn("claim_type", F.lit("damage")).withColumn("claim_date", F.current_date())
    .withColumn("incurred_amount", F.round(500 + F.rand(1) * 4000, 2)).withColumn("status", F.lit("open"))
    .select("claim_id", "policy_id", "tenant", "claim_type", "claim_date", "incurred_amount", "status"))
updates.unionByName(new_claims).createOrReplaceTempView("claim_updates")

# COMMAND ----------

# MAGIC %md ## 3. One MERGE applies inserts and updates together

# COMMAND ----------

start_v = spark.sql("DESCRIBE HISTORY 2_silver_claims_cdf LIMIT 1").select("version").first()[0]

# TODO: MERGE INTO 2_silver_claims_cdf USING claim_updates ON claim_id;
# WHEN MATCHED UPDATE SET status/incurred_amount; WHEN NOT MATCHED INSERT *.

print(f"rows after merge: {spark.table('2_silver_claims_cdf').count():,}")

# COMMAND ----------

# MAGIC %md ## 4. Read exactly what changed — Change Data Feed

# COMMAND ----------

# TODO: use table_changes('2_silver_claims_cdf', start_v + 1) and group by _change_type.
# display(spark.sql(f"SELECT _change_type, count(*) rows FROM table_changes(...) GROUP BY _change_type"))

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: **C1 — Tenant isolation**.
