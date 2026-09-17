# Databricks notebook source
# MAGIC %md
# MAGIC # C5 — Zero-copy clones for dev and test
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** safe copies of production data via Delta `CLONE` — **shallow**
# MAGIC (shares files, near-instant) and **deep** (independent copy). Fill in the `# TODO`s;
# MAGIC answer in `solutions/13_solution_c5_clones`.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# MAGIC %md ## 1. Make a DEEP clone of 2_silver_policies and count it

# COMMAND ----------

# TODO: CREATE OR REPLACE TABLE {FQ}.c5_deep DEEP CLONE {FQ}.`2_silver_policies`

# COMMAND ----------

# MAGIC %md ## 2. Make a SHALLOW clone (wrap in try/except — it may be restricted here)

# COMMAND ----------

# TODO: CREATE OR REPLACE TABLE {FQ}.c5_shallow SHALLOW CLONE {FQ}.`2_silver_policies`

# COMMAND ----------

# MAGIC %md ## 3. Delete rows from a clone and confirm the source is unchanged

# COMMAND ----------

# TODO: DELETE FROM the clone WHERE tenant='helios_re'; compare counts with the source

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C6 — keeping tables fast and tidy`.
