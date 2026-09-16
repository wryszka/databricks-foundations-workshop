# Databricks notebook source
# MAGIC %md
# MAGIC # C6 — Keeping tables fast and tidy
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** table upkeep — `OPTIMIZE`, liquid clustering, `VACUUM` — most of
# MAGIC which managed tables do for you. Fill in the `# TODO`s; answer in
# MAGIC `solutions/14_solution_c6_maintenance`.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

spark.sql(f"CREATE OR REPLACE TABLE {FQ}.c6_demo AS SELECT * FROM {FQ}.`2_silver_policies`")

# COMMAND ----------

# MAGIC %md ## 1. Set liquid clustering on (tenant, region)

# COMMAND ----------

# TODO: ALTER TABLE {FQ}.c6_demo CLUSTER BY (tenant, region)

# COMMAND ----------

# MAGIC %md ## 2. OPTIMIZE the table

# COMMAND ----------

# TODO: OPTIMIZE {FQ}.c6_demo

# COMMAND ----------

# MAGIC %md ## 3. VACUUM ... DRY RUN (safe — deletes nothing)

# COMMAND ----------

# TODO: VACUUM {FQ}.c6_demo DRY RUN

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C7 — Catalog Explorer and lineage`.
