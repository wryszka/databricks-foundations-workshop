# Databricks notebook source
# MAGIC %md
# MAGIC # A2 — Databricks SQL and the SQL warehouse
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** a data product serves results through governed SQL — no separate
# MAGIC database to stand up. Here you build a reusable **view**, and get a first taste that
# MAGIC **AI is a SQL function** on Keystone, ready for Track E.
# MAGIC
# MAGIC > On Databricks the **SQL Editor** runs these against a **SQL warehouse**. Everything
# MAGIC > below is plain SQL, so it runs the same way in this notebook.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

# COMMAND ----------

# MAGIC %md ## 1. A view — a saved, reusable query other tools can read

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW v_tenant_kpis AS
# MAGIC SELECT
# MAGIC   p.tenant,
# MAGIC   count(*)                                   AS policies,
# MAGIC   round(sum(p.annual_premium), 2)            AS gross_written_premium,
# MAGIC   count(c.claim_id)                          AS claims,
# MAGIC   round(count(c.claim_id) / count(*), 4)     AS claim_frequency
# MAGIC FROM 2_silver_policies p
# MAGIC LEFT JOIN 2_silver_claims c ON p.policy_id = c.policy_id
# MAGIC GROUP BY p.tenant;
# MAGIC
# MAGIC SELECT * FROM v_tenant_kpis ORDER BY tenant;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. AI is just a SQL function — `ai_classify`
# MAGIC No model to deploy. Point `ai_classify` at free text and give it the labels you want.
# MAGIC Here we bucket a sample of complaint notes by tone — a teaser for Track E.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   tenant,
# MAGIC   note,
# MAGIC   ai_classify(note, ARRAY('angry', 'neutral', 'happy')) AS tone
# MAGIC FROM 2_silver_complaints
# MAGIC LIMIT 8;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Where this runs in real life
# MAGIC - In the **SQL Editor**, the same query runs on a **SQL warehouse** (serverless
# MAGIC   compute for SQL). You can **Save** a query and schedule it.
# MAGIC - Views like `v_tenant_kpis` become the building blocks of dashboards (Track E) and
# MAGIC   of anything a downstream app reads.
# MAGIC
# MAGIC > 💡 **Genie Code:** ask it in the SQL editor for "average premium by region per tenant"
# MAGIC > and it writes the SQL for you.

# COMMAND ----------

# MAGIC %md ✅ **Done.** You have a reusable view and have called AI from SQL. Next: **B1 — File upload**.
