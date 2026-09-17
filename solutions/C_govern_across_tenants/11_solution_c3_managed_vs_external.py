# Databricks notebook source
# MAGIC %md
# MAGIC # C3 — Managed vs external tables (and why managed wins)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** people bring an old instinct — *"we must use external tables,
# MAGIC otherwise dropping the table deletes the files."* On Databricks with Unity Catalog that
# MAGIC habit is out of date. **Managed tables are the recommended default**: the platform owns
# MAGIC the storage layout and lifecycle and gives you automatic optimisation plus safety nets
# MAGIC like `UNDROP` and time travel. Let's prove the myth wrong.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

# COMMAND ----------

# MAGIC %md ## 1. Create a managed table and check it is MANAGED

# COMMAND ----------

spark.sql(f"""
    CREATE OR REPLACE TABLE {FQ}.c3_demo AS
    SELECT * FROM {FQ}.`2_silver_policies` WHERE tenant = 'helios_re'
""")
before = spark.table(f"{FQ}.c3_demo").count()
print(f"c3_demo has {before:,} rows")
display(spark.sql(f"DESCRIBE EXTENDED {FQ}.c3_demo").filter("col_name = 'Type'"))

# COMMAND ----------

# MAGIC %md ## 2. Drop it — the "scary" step

# COMMAND ----------

spark.sql(f"DROP TABLE {FQ}.c3_demo")
print("dropped. Is the data gone forever? No —")

# COMMAND ----------

# MAGIC %md ## 3. UNDROP — the data was never lost

# COMMAND ----------

spark.sql(f"UNDROP TABLE {FQ}.c3_demo")
after = spark.table(f"{FQ}.c3_demo").count()
print(f"recovered c3_demo: {after:,} rows (was {before:,})")
assert after == before, "row counts should match after UNDROP"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Time travel is the other safety net
# MAGIC Even after edits, you can read an earlier version.

# COMMAND ----------

spark.sql(f"DELETE FROM {FQ}.c3_demo WHERE penalty_points > 3")
now = spark.table(f"{FQ}.c3_demo").count()
v0 = spark.sql(f"SELECT count(*) c FROM {FQ}.c3_demo VERSION AS OF 0").first()["c"]
print(f"after delete: {now:,} rows | version 0: {v0:,} rows")
display(spark.sql(f"DESCRIBE HISTORY {FQ}.c3_demo").select("version", "operation"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## The takeaway
# MAGIC - **Use managed tables by default.** Unity Catalog owns the storage and lifecycle.
# MAGIC - Dropping a managed table is recoverable (`UNDROP`) within the retention window, and
# MAGIC   time travel lets you read prior versions — the safety the "external for safety" habit
# MAGIC   was really reaching for, without giving up automatic optimisation and performance.
# MAGIC - External tables still have their place (data you must keep in a specific bucket you
# MAGIC   own), but that is not available on Free Edition and is the exception, not the default.

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C4 — time travel and SCD2`.
