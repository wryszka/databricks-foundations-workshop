# Databricks notebook source
# MAGIC %md
# MAGIC # A2 — Databricks SQL and the SQL warehouse
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** a data product serves results through governed SQL. Here you build
# MAGIC a reusable **view** and get a first taste that **AI is a SQL function** on Keystone.
# MAGIC
# MAGIC Fill in each `# TODO`. The complete version is in `solutions/`.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# MAGIC %md ## 1. A view — a saved, reusable query

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: create a view v_tenant_kpis with, per tenant: policies, gross_written_premium
# MAGIC -- (sum of annual_premium), claims, and claim_frequency (claims / policies).
# MAGIC -- Hint: LEFT JOIN 2_silver_policies to 2_silver_claims ON policy_id.
# MAGIC CREATE OR REPLACE VIEW v_tenant_kpis AS
# MAGIC SELECT tenant, count(*) AS policies /* , ... */
# MAGIC FROM 2_silver_policies
# MAGIC GROUP BY tenant;
# MAGIC
# MAGIC SELECT * FROM v_tenant_kpis ORDER BY tenant;

# COMMAND ----------

# MAGIC %md ## 2. AI is just a SQL function — `ai_classify`

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: classify each complaint note as 'angry','neutral','happy' with ai_classify.
# MAGIC -- Hint: ai_classify(note, ARRAY('angry','neutral','happy'))
# MAGIC SELECT tenant, note /* , ai_classify(...) AS tone */
# MAGIC FROM 2_silver_complaints
# MAGIC LIMIT 8;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Where this runs in real life
# MAGIC In the **SQL Editor** the same SQL runs on a **SQL warehouse**; you can save and
# MAGIC schedule a query, and views become the building blocks for dashboards (Track E).
# MAGIC
# MAGIC > 💡 **Genie Code:** ask it in the SQL editor for "average premium by region per tenant".

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: **B1 — File upload**.
