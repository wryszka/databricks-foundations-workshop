# Databricks notebook source
# MAGIC %md
# MAGIC # G2 — A simple app powered by Genie + Lakebase (solution)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** everything you built today — governed tables, a Genie space, an
# MAGIC operational database — comes together behind one small **Databricks App**. The app lets
# MAGIC a user ask Genie a question and look up the portfolio table. The code lives in the
# MAGIC [`app/`](../app) folder; this notebook checks the data is ready and walks the deploy.
# MAGIC
# MAGIC > 💡 **Genie Code:** the app's data query was the kind of SQL Genie Code can scaffold.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

# COMMAND ----------

# MAGIC %md ### 1. Confirm the app's data source exists and is queryable

# COMMAND ----------

assert spark.catalog.tableExists(f"{FQ}.3_gold_portfolio_summary"), \
    "Run 01_data_generator with build_all=yes (or Track D) first."
display(spark.sql(f"""
    SELECT tenant, region, cover_type, policies, gwp
    FROM {FQ}.`3_gold_portfolio_summary`
    ORDER BY gwp DESC LIMIT 10
"""))
print("This is exactly what the app's /api/portfolio endpoint returns.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Configure the app
# MAGIC In [`app/app.yaml`](../app/app.yaml) set:
# MAGIC - `KEYSTONE_CATALOG` / `KEYSTONE_SCHEMA` → this schema
# MAGIC - `DATABRICKS_WAREHOUSE_ID` → a SQL warehouse
# MAGIC - `GENIE_SPACE_ID` → the space from lab E1
# MAGIC - `LAKEBASE_*` → only if you want the operational (Postgres) path from lab G1
# MAGIC
# MAGIC The app reads the portfolio from **Lakebase** when `LAKEBASE_HOST` is set, otherwise
# MAGIC from the **warehouse** — so it works even before you finish G1.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3. Deploy
# MAGIC ```
# MAGIC databricks apps create keystone-mini-app
# MAGIC databricks sync ./app /Workspace/Users/<you>/keystone-mini-app
# MAGIC databricks apps deploy keystone-mini-app \
# MAGIC   --source-code-path /Workspace/Users/<you>/keystone-mini-app
# MAGIC ```
# MAGIC Then grant the app's service principal `CAN USE` on the warehouse, `CAN RUN` on the
# MAGIC Genie space, and read access to the catalog/schema.

# COMMAND ----------

# MAGIC %md
# MAGIC ✅ **Done.** You have a working product front end over the day's work. This completes
# MAGIC the "put an app in front of it" track.
