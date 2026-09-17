# Databricks notebook source
# MAGIC %md
# MAGIC # B3 — Upserts with MERGE (and reading the changes)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** a source keeps changing — some claims are updated, some are new.
# MAGIC `MERGE` applies both in one statement (the standard change-data-capture pattern), and
# MAGIC **Change Data Feed** lets a downstream step read exactly which rows changed.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

# COMMAND ----------

# MAGIC %md ## 1. A target table with Change Data Feed switched on

# COMMAND ----------

from pyspark.sql import functions as F

spark.sql("DROP TABLE IF EXISTS 2_silver_claims_cdf")
(spark.table("2_silver_claims").limit(800)
    .write.mode("overwrite")
    .option("delta.enableChangeDataFeed", "true")
    .saveAsTable("2_silver_claims_cdf"))
# ensure the property is set (also settable via ALTER TABLE ... SET TBLPROPERTIES)
spark.sql("ALTER TABLE 2_silver_claims_cdf SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")
print(f"target rows: {spark.table('2_silver_claims_cdf').count():,}")

# COMMAND ----------

# MAGIC %md ## 2. A batch of changes — some updates to existing claims, some brand-new ones

# COMMAND ----------

existing = spark.table("2_silver_claims_cdf").limit(100)
updates = (existing
    .withColumn("status", F.lit("settled"))
    .withColumn("incurred_amount", F.round(F.col("incurred_amount") * 1.10, 2)))   # revised reserve

new_claims = (spark.range(50)
    .withColumn("claim_id", F.format_string("CLM-NEW-%04d", F.col("id")))
    .withColumn("policy_id", F.lit("POL-0000001"))
    .withColumn("tenant", F.lit("bricksurance_se"))
    .withColumn("claim_type", F.lit("damage"))
    .withColumn("claim_date", F.current_date())
    .withColumn("incurred_amount", F.round(500 + F.rand(1) * 4000, 2))
    .withColumn("status", F.lit("open"))
    .select("claim_id", "policy_id", "tenant", "claim_type", "claim_date", "incurred_amount", "status"))

updates.unionByName(new_claims).createOrReplaceTempView("claim_updates")
print("changes to apply:", spark.table("claim_updates").count(), "(100 updates + 50 inserts)")

# COMMAND ----------

# MAGIC %md ## 3. One MERGE applies inserts and updates together

# COMMAND ----------

start_v = spark.sql("DESCRIBE HISTORY 2_silver_claims_cdf LIMIT 1").select("version").first()[0]

spark.sql("""
    MERGE INTO 2_silver_claims_cdf t
    USING claim_updates s
    ON t.claim_id = s.claim_id
    WHEN MATCHED THEN UPDATE SET t.status = s.status, t.incurred_amount = s.incurred_amount
    WHEN NOT MATCHED THEN INSERT *
""")
print(f"rows after merge: {spark.table('2_silver_claims_cdf').count():,}  (was 800, +50 inserts)")

# COMMAND ----------

# MAGIC %md ## 4. Read exactly what changed — Change Data Feed

# COMMAND ----------

changes = spark.sql(f"""
    SELECT _change_type, count(*) AS rows
    FROM table_changes('2_silver_claims_cdf', {start_v + 1})
    GROUP BY _change_type
    ORDER BY _change_type
""")
display(changes)
# update_preimage + update_postimage for the 100 updates, insert for the 50 new rows.

# COMMAND ----------

# MAGIC %md
# MAGIC A downstream job can consume just these deltas instead of rescanning the whole table.
# MAGIC
# MAGIC > 💡 **Genie Code:** ask it to "merge claim_updates into the claims table on claim_id"
# MAGIC > and it writes the MERGE for you.

# COMMAND ----------

# MAGIC %md ✅ **Done.** You can keep a table in sync and read its changes. Next: **C1 — Tenant isolation**.
