# Databricks notebook source
# MAGIC %md
# MAGIC # C4 — Time travel and SCD Type 2 history
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** reproduce what the data said on a given day (time travel) and
# MAGIC keep long-term history (SCD Type 2). Fill in the `# TODO`s; answer in
# MAGIC `solutions/12_solution_c4_time_travel_scd2`.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# MAGIC %md ## 1. Time travel: change a table, then read VERSION AS OF 0

# COMMAND ----------

spark.sql(f"CREATE OR REPLACE TABLE {FQ}.c4_premiums AS SELECT policy_id, tenant, annual_premium FROM {FQ}.`2_silver_policies` WHERE tenant='northwind_mutual'")
# TODO: UPDATE the table (e.g. a 10% rate rise), then compare avg(annual_premium) now vs VERSION AS OF 0
# TODO: DESCRIBE HISTORY the table

# COMMAND ----------

# MAGIC %md ## 2. SCD Type 2: version a small tenant-config dimension with a MERGE

# COMMAND ----------

# Provided: the initial dimension
spark.sql(f"""
    CREATE OR REPLACE TABLE {FQ}.c4_tenant_config (
        tenant STRING, service_tier STRING,
        valid_from TIMESTAMP, valid_to TIMESTAMP, is_current BOOLEAN)
""")
spark.sql(f"""INSERT INTO {FQ}.c4_tenant_config VALUES
      ('bricksurance_se','standard', current_timestamp(), NULL, true),
      ('northwind_mutual','standard', current_timestamp(), NULL, true),
      ('helios_re','premium', current_timestamp(), NULL, true)""")
updates = spark.createDataFrame([("bricksurance_se", "premium")], ["tenant", "service_tier"])
updates.createOrReplaceTempView("c4_updates")

# TODO: MERGE to close the current row where service_tier changed (set is_current=false, valid_to=now)
# TODO: INSERT the new current row for the changed tenant
# TODO: SELECT * ORDER BY tenant, valid_from to see both versions

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C5 — zero-copy clones`.
