# Databricks notebook source
# MAGIC %md
# MAGIC # C5 — Zero-copy clones for dev and test
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** you constantly need safe copies of production data to experiment
# MAGIC on. Delta `CLONE` gives you two kinds: a **shallow** clone (points at the same files —
# MAGIC near-instant, cheap, great for a throwaway test) and a **deep** clone (an independent,
# MAGIC self-contained copy).

# COMMAND ----------

# MAGIC %run ../notebooks/00_config

# COMMAND ----------

# MAGIC %md ## Deep clone — an independent copy

# COMMAND ----------

spark.sql(f"CREATE OR REPLACE TABLE {FQ}.c5_deep DEEP CLONE {FQ}.`2_silver_policies`")
print("deep clone rows:", spark.table(f"{FQ}.c5_deep").count())

# COMMAND ----------

# MAGIC %md ## Shallow clone — near-instant, shares the source's files

# COMMAND ----------

shallow_ok = True
try:
    spark.sql(f"CREATE OR REPLACE TABLE {FQ}.c5_shallow SHALLOW CLONE {FQ}.`2_silver_policies`")
    print("shallow clone rows:", spark.table(f"{FQ}.c5_shallow").count())
except Exception as e:
    shallow_ok = False
    print("shallow clone not available here:", str(e)[:300])

# COMMAND ----------

# MAGIC %md ## Change a clone — the source is untouched

# COMMAND ----------

target = "c5_shallow" if shallow_ok else "c5_deep"
spark.sql(f"DELETE FROM {FQ}.{target} WHERE tenant = 'helios_re'")
src = spark.table(f"{FQ}.`2_silver_policies`").count()
clone = spark.table(f"{FQ}.{target}").count()
print(f"after deleting Helios from the clone: source={src:,}, clone={clone:,} (source unchanged)")
assert src > clone, "the source should be untouched by edits to the clone"

# COMMAND ----------

# MAGIC %md
# MAGIC **Use it for:** spinning up a dev/test copy of a tenant's data in seconds without
# MAGIC duplicating storage (shallow), or a fully independent snapshot (deep). Clean up with
# MAGIC `DROP TABLE` on the clones.

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C6 — keeping tables fast and tidy`.
