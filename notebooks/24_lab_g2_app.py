# Databricks notebook source
# MAGIC %md
# MAGIC # G2 — A simple app powered by Genie + Lakebase
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** bring the whole day together behind one small **Databricks App** —
# MAGIC ask Genie a question and look up the portfolio table. The code is in the
# MAGIC [`app/`](../app) folder; here you confirm the data and deploy.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# MAGIC %md ### 1. Confirm the app's data source
# MAGIC TODO 1: assert `{FQ}.3_gold_portfolio_summary` exists, then display its top 10 rows by
# MAGIC `gwp`. This is what the app's `/api/portfolio` returns.

# COMMAND ----------

# your code here

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Configure `app/app.yaml`
# MAGIC Set `KEYSTONE_CATALOG`, `KEYSTONE_SCHEMA`, `DATABRICKS_WAREHOUSE_ID`, `GENIE_SPACE_ID`
# MAGIC (and `LAKEBASE_*` if using the Postgres path from G1).

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3. Deploy
# MAGIC ```
# MAGIC databricks apps create keystone-mini-app
# MAGIC databricks sync ./app /Workspace/Users/<you>/keystone-mini-app
# MAGIC databricks apps deploy keystone-mini-app --source-code-path /Workspace/Users/<you>/keystone-mini-app
# MAGIC ```
# MAGIC Grant the app SP `CAN USE` on the warehouse, `CAN RUN` on the Genie space, read on the schema.

# COMMAND ----------

# MAGIC %md ✅ **Done** when the deployed app answers a question and lists the portfolio.
