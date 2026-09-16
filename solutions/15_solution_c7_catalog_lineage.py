# Databricks notebook source
# MAGIC %md
# MAGIC # C7 — Catalog Explorer and data lineage
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** finding data and understanding where it came from — without
# MAGIC reading anyone's code. **Catalog Explorer** (in the UI) is the browse tool; **lineage**
# MAGIC shows how tables flow into one another.
# MAGIC
# MAGIC ### Do this in the UI first
# MAGIC Open **Catalog** in the left sidebar, expand your catalog → your schema, click a table
# MAGIC (e.g. `2_silver_policies`), and look at the **Lineage** tab to see upstream/downstream
# MAGIC tables and columns as a graph.

# COMMAND ----------

# MAGIC %run ../notebooks/00_config

# COMMAND ----------

# MAGIC %md
# MAGIC ## Browse the catalog from SQL (`information_schema` — always available)

# COMMAND ----------

display(spark.sql(f"""
    SELECT table_name, table_type, comment
    FROM {CATALOG}.information_schema.tables
    WHERE table_schema = '{SCHEMA}'
    ORDER BY table_name
"""))

# COMMAND ----------

# MAGIC %md ## Column-level detail for one table

# COMMAND ----------

display(spark.sql(f"""
    SELECT column_name, data_type
    FROM {CATALOG}.information_schema.columns
    WHERE table_schema = '{SCHEMA}' AND table_name = '2_silver_policies'
    ORDER BY ordinal_position
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lineage from system tables
# MAGIC Lineage is captured in `system.access.table_lineage` / `column_lineage`. It may take a
# MAGIC few minutes to populate and requires the system schema to be enabled — we handle the
# MAGIC case where it isn't.

# COMMAND ----------

try:
    df = spark.sql(f"""
        SELECT source_table_full_name, target_table_full_name, event_time
        FROM system.access.table_lineage
        WHERE target_table_schema = '{SCHEMA}'
        ORDER BY event_time DESC LIMIT 20
    """)
    n = df.count()
    print(f"table_lineage rows for this schema: {n}")
    display(df)
except Exception as e:
    print("system.access.table_lineage not available/enabled here:", str(e)[:300])

# COMMAND ----------

# MAGIC %md
# MAGIC The lineage **graph** in Catalog Explorer is the friendlier view of the same
# MAGIC information — use the UI for exploration, system tables when you need to query it.

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C8 — system tables`.
