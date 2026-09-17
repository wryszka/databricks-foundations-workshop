# Databricks notebook source
# MAGIC %md
# MAGIC # C3 — Managed vs external tables (and why managed wins)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** retire the old instinct that dropping a table deletes your data.
# MAGIC On Databricks with Unity Catalog, **managed tables are the default** and dropping is
# MAGIC recoverable. Prove it. Fill in the `# TODO`s; answer in
# MAGIC `solutions/11_solution_c3_managed_vs_external`.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# MAGIC %md ## 1. Create a managed table (Helios's policies) and confirm it's MANAGED

# COMMAND ----------

spark.sql(f"""
    CREATE OR REPLACE TABLE {FQ}.c3_demo AS
    SELECT * FROM {FQ}.`2_silver_policies` WHERE tenant = 'helios_re'
""")
before = spark.table(f"{FQ}.c3_demo").count()
print(f"c3_demo has {before:,} rows")
# TODO: DESCRIBE EXTENDED the table and confirm its Type is MANAGED

# COMMAND ----------

# MAGIC %md ## 2. DROP it, then 3. UNDROP it and confirm the rows are back

# COMMAND ----------

# TODO: DROP TABLE {FQ}.c3_demo
# TODO: UNDROP TABLE {FQ}.c3_demo
# TODO: recount and assert it equals `before`

# COMMAND ----------

# MAGIC %md ## 4. Show time travel: delete some rows, then read VERSION AS OF 0

# COMMAND ----------

# TODO: DELETE some rows, then SELECT count(*) ... VERSION AS OF 0, and DESCRIBE HISTORY

# COMMAND ----------

# MAGIC %md
# MAGIC **Takeaway:** use managed by default — `UNDROP` + time travel are your safety nets,
# MAGIC and you keep automatic optimisation and performance.

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C4 — time travel and SCD2`.
