# Databricks notebook source
# MAGIC %md
# MAGIC # C6 — Keeping tables fast and tidy
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** a quick tour of table upkeep — `OPTIMIZE`, liquid clustering, and
# MAGIC `VACUUM`. The good news for builders: on managed tables (C3) Databricks does most of
# MAGIC this for you automatically. Here you see the manual levers so you understand what's
# MAGIC happening under the hood.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

# COMMAND ----------

# MAGIC %md ## A working table

# COMMAND ----------

spark.sql(f"CREATE OR REPLACE TABLE {FQ}.c6_demo AS SELECT * FROM {FQ}.`2_silver_policies`")

# COMMAND ----------

# MAGIC %md ## 1. Liquid clustering — cluster the table by the columns you filter on

# COMMAND ----------

spark.sql(f"ALTER TABLE {FQ}.c6_demo CLUSTER BY (tenant, region)")
print("clustering set on (tenant, region)")

# COMMAND ----------

# MAGIC %md ## 2. OPTIMIZE — compact small files (and apply clustering)

# COMMAND ----------

display(spark.sql(f"OPTIMIZE {FQ}.c6_demo"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. VACUUM — remove files no longer referenced
# MAGIC We use a **DRY RUN** so nothing is deleted in the lab; it lists what *would* be removed
# MAGIC beyond the retention window (default 7 days).

# COMMAND ----------

display(spark.sql(f"VACUUM {FQ}.c6_demo DRY RUN"))

# COMMAND ----------

# MAGIC %md
# MAGIC **Takeaway:** these are the manual controls; managed tables with predictive
# MAGIC optimisation apply most of them automatically, which is another reason to prefer
# MAGIC managed (see C3).

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C7 — Catalog Explorer and lineage`.
