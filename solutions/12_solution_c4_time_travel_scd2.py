# Databricks notebook source
# MAGIC %md
# MAGIC # C4 — Time travel and SCD Type 2 history
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** regulated tenants need to reproduce *what the data said on a
# MAGIC given day* and keep long-term history. **Time travel** covers the short term; a
# MAGIC **Slowly Changing Dimension Type 2 (SCD2)** table keeps full history for the long term.

# COMMAND ----------

# MAGIC %run ../notebooks/00_config

# COMMAND ----------

# MAGIC %md ## 1. Time travel — read a table as it was

# COMMAND ----------

spark.sql(f"CREATE OR REPLACE TABLE {FQ}.c4_premiums AS SELECT policy_id, tenant, annual_premium FROM {FQ}.`2_silver_policies` WHERE tenant='northwind_mutual'")
spark.sql(f"UPDATE {FQ}.c4_premiums SET annual_premium = annual_premium * 1.10")  # a 10% rate change
v_now = spark.sql(f"SELECT round(avg(annual_premium),2) a FROM {FQ}.c4_premiums").first()["a"]
v_0 = spark.sql(f"SELECT round(avg(annual_premium),2) a FROM {FQ}.c4_premiums VERSION AS OF 0").first()["a"]
print(f"avg premium now: {v_now} | before the rate change (version 0): {v_0}")
display(spark.sql(f"DESCRIBE HISTORY {FQ}.c4_premiums").select("version", "operation", "operationMetrics"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. SCD Type 2 — keep every version of a row
# MAGIC We build a small tenant-configuration dimension and version it with `valid_from`,
# MAGIC `valid_to`, `is_current`. A `MERGE` closes the old row and inserts the new one.

# COMMAND ----------

from pyspark.sql import functions as F

# initial state
spark.sql(f"""
    CREATE OR REPLACE TABLE {FQ}.c4_tenant_config (
        tenant STRING, service_tier STRING,
        valid_from TIMESTAMP, valid_to TIMESTAMP, is_current BOOLEAN
    )
""")
spark.sql(f"""
    INSERT INTO {FQ}.c4_tenant_config VALUES
      ('bricksurance_se','standard', current_timestamp(), NULL, true),
      ('northwind_mutual','standard', current_timestamp(), NULL, true),
      ('helios_re','premium',  current_timestamp(), NULL, true)
""")

# a change arrives: bricksurance upgrades to premium
updates = spark.createDataFrame([("bricksurance_se", "premium")], ["tenant", "service_tier"])
updates.createOrReplaceTempView("c4_updates")

# SCD2 merge: close the current row where the value changed...
spark.sql(f"""
    MERGE INTO {FQ}.c4_tenant_config t
    USING c4_updates u
    ON t.tenant = u.tenant AND t.is_current = true AND t.service_tier <> u.service_tier
    WHEN MATCHED THEN UPDATE SET t.is_current = false, t.valid_to = current_timestamp()
""")
# ...then insert the new current row
spark.sql(f"""
    INSERT INTO {FQ}.c4_tenant_config
    SELECT u.tenant, u.service_tier, current_timestamp(), NULL, true
    FROM c4_updates u
    JOIN {FQ}.c4_tenant_config t ON t.tenant = u.tenant AND t.is_current = false
""")

display(spark.sql(f"SELECT * FROM {FQ}.c4_tenant_config ORDER BY tenant, valid_from"))

# COMMAND ----------

# MAGIC %md
# MAGIC You can now answer "what tier was Bricksurance on last month?" from `c4_tenant_config`
# MAGIC (long-term, queryable history), while time travel covers recent, table-wide rollbacks.

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C5 — zero-copy clones`.
