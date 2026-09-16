# Databricks notebook source
# MAGIC %md
# MAGIC # A1 — Meet the platform
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** the first thing you do on any new platform is *look at the data*.
# MAGIC This lab is the query layer of the Keystone product — the same Delta table read from
# MAGIC SQL and from Python, a quick chart, and a note on letting the AI write your query.

# COMMAND ----------

# MAGIC %run ../notebooks/00_config

# COMMAND ----------

# MAGIC %md ## 1. A Delta table is just a table — query it

# COMMAND ----------

df = spark.table("2_silver_policies")
print(f"{df.count():,} policies across tenants: {[r['tenant'] for r in df.select('tenant').distinct().collect()]}")
display(df.limit(10))

# COMMAND ----------

# MAGIC %md ## 2. The same table, from SQL — `%sql` and Python are interchangeable

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT tenant, count(*) AS policies, round(avg(annual_premium)) AS avg_premium
# MAGIC FROM 2_silver_policies
# MAGIC GROUP BY tenant
# MAGIC ORDER BY tenant

# COMMAND ----------

# The identical question in Python — pick whichever language fits the task.
from pyspark.sql import functions as F
by_tenant = (
    spark.table("2_silver_policies")
    .groupBy("tenant")
    .agg(F.count("*").alias("policies"), F.round(F.avg("annual_premium")).alias("avg_premium"))
    .orderBy("tenant")
)
display(by_tenant)

# COMMAND ----------

# MAGIC %md ## 3. A quick chart — `display()` turns any result into a visual
# MAGIC In the notebook UI, click the **+ → Visualization** on the result below to plot
# MAGIC average premium by driver age. Here we shape the data; the chart is one click away.

# COMMAND ----------

by_age = (
    spark.table("2_silver_policies")
    .withColumn("age_band", F.expr("CASE WHEN driver_age<25 THEN '18-24' WHEN driver_age<40 THEN '25-39' "
                                   "WHEN driver_age<60 THEN '40-59' ELSE '60+' END"))
    .groupBy("age_band").agg(F.round(F.avg("annual_premium")).alias("avg_premium"))
    .orderBy("age_band")
)
display(by_age)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Let the AI write the query
# MAGIC You don't have to remember syntax. Open the **Databricks Assistant** (the ✨ icon in
# MAGIC the cell toolbar) and ask, in English: *"which region has the highest average premium?"*
# MAGIC
# MAGIC > 💡 **Genie Code:** the same idea, scaled up — prompt Genie Code (side panel in the
# MAGIC > notebook and SQL editor) to generate whole cells or notebooks, not just one query.

# COMMAND ----------

# MAGIC %md ✅ **Done.** You can read and shape data three ways. Next: **A2 — Databricks SQL**.
