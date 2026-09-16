# Databricks notebook source
# MAGIC %md
# MAGIC # C8 — System tables: access, lineage, cost
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** the platform records its own operations as queryable tables under
# MAGIC the `system` catalog — the answer to "who queried this?", "where did it come from?" and
# MAGIC "what is this costing?". Great for the cost/audit questions builders always ask.
# MAGIC
# MAGIC > **Free Edition note:** some system schemas (especially `system.billing`) may be empty
# MAGIC > or unavailable without a paid account. We probe each and report what's there.

# COMMAND ----------

# MAGIC %run ../notebooks/00_config

# COMMAND ----------

def probe(label, sql):
    try:
        df = spark.sql(sql)
        n = df.count()
        print(f"[OK]   {label}: {n} rows")
        if n:
            display(df)
    except Exception as e:
        print(f"[N/A]  {label}: {str(e)[:200]}")

# COMMAND ----------

# MAGIC %md ## Catalog of available system tables

# COMMAND ----------

probe("system schemas", "SELECT schema_name FROM system.information_schema.schemata ORDER BY schema_name")

# COMMAND ----------

# MAGIC %md ## Audit — recent activity (who did what)

# COMMAND ----------

probe("system.access.audit (recent)",
      "SELECT event_time, action_name, user_identity.email AS who "
      "FROM system.access.audit ORDER BY event_time DESC LIMIT 20")

# COMMAND ----------

# MAGIC %md ## Cost — usage in DBUs (may be empty on Free Edition)

# COMMAND ----------

probe("system.billing.usage (last 7 days)",
      "SELECT usage_date, sku_name, sum(usage_quantity) AS dbus "
      "FROM system.billing.usage WHERE usage_date >= current_date() - INTERVAL 7 DAYS "
      "GROUP BY usage_date, sku_name ORDER BY usage_date DESC LIMIT 20")

# COMMAND ----------

# MAGIC %md
# MAGIC **Takeaway:** everything the platform does is itself data you can query and govern.
# MAGIC Which of these are populated depends on your workspace tier — note which worked above.

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `D1 — a declarative pipeline`.
