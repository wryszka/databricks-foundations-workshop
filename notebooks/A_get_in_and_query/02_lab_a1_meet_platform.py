# Databricks notebook source
# MAGIC %md
# MAGIC # A1 — Meet the platform
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** the first thing you do on any new platform is *look at the data*.
# MAGIC This is the query layer of the Keystone product — the same Delta table read from SQL
# MAGIC and from Python, a quick chart, and a note on letting the AI write your query.
# MAGIC
# MAGIC Fill in each `# TODO`. Stuck? The complete version is in `solutions/`.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# MAGIC %md ## 1. A Delta table is just a table — query it

# COMMAND ----------

# TODO: load the table "2_silver_policies" into a DataFrame and display 10 rows.
# Hint: spark.table("...")  and  display(df.limit(10))
df = spark.table("2_silver_policies")
print(f"{df.count():,} policies")
# display(...)

# COMMAND ----------

# MAGIC %md ## 2. The same table, from SQL

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: count policies and average annual_premium per tenant, ordered by tenant.
# MAGIC SELECT tenant /* , ... */ FROM 2_silver_policies GROUP BY tenant ORDER BY tenant

# COMMAND ----------

# TODO: write the identical query in Python (groupBy / agg) and display it.
from pyspark.sql import functions as F
# by_tenant = spark.table("2_silver_policies").groupBy(...).agg(...)
# display(by_tenant)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. A quick chart
# MAGIC Shape average premium by an age band, then click **+ → Visualization** on the result.

# COMMAND ----------

# TODO: build a DataFrame of avg premium by age band and display it.
# Hint: F.expr("CASE WHEN driver_age<25 THEN '18-24' ... END") then groupBy/agg.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Let the AI write the query
# MAGIC Open the **Databricks Assistant** (✨ in the cell toolbar) and ask
# MAGIC *"which region has the highest average premium?"*.
# MAGIC
# MAGIC > 💡 **Genie Code:** prompt the side panel to generate whole cells, not just one query.

# COMMAND ----------

# MAGIC %md ✅ **Done** when the cells above run. Next: **A2 — Databricks SQL**.
