# Databricks notebook source
# MAGIC %md
# MAGIC # C7 — Catalog Explorer and data lineage
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** finding data and seeing where it came from. **Do this in the UI
# MAGIC first:** open **Catalog** → your schema → a table → the **Lineage** tab. Then reproduce
# MAGIC the browse from SQL below. Answer in `solutions/15_solution_c7_catalog_lineage`.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# MAGIC %md ## 1. List your schema's tables from information_schema

# COMMAND ----------

# TODO: SELECT table_name, table_type FROM {CATALOG}.information_schema.tables
#       WHERE table_schema = '{SCHEMA}'

# COMMAND ----------

# MAGIC %md ## 2. List the columns of 2_silver_policies

# COMMAND ----------

# TODO: query {CATALOG}.information_schema.columns for that table

# COMMAND ----------

# MAGIC %md ## 3. (Optional) Query system.access.table_lineage for this schema (wrap in try/except)

# COMMAND ----------

# TODO: SELECT ... FROM system.access.table_lineage WHERE target_table_schema='{SCHEMA}'

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C8 — system tables`.
