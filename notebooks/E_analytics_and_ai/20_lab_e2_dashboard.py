# Databricks notebook source
# MAGIC %md
# MAGIC # E2 — Build a dashboard from Genie's SQL
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** turn the natural-language exploration from lab E1 into a
# MAGIC durable, shareable **AI/BI dashboard**. You ask Genie a question, copy the SQL it
# MAGIC generated, and drop it into a dashboard tile.
# MAGIC
# MAGIC ### Your task (in the UI)
# MAGIC 1. Left sidebar → **Dashboards** → **Create dashboard**.
# MAGIC 2. **Data** tab → add a dataset. Either paste your own SQL copied from Genie's
# MAGIC    **Show generated code** (lab E1), or use the starter queries below.
# MAGIC 3. **Canvas** tab → add a **counter** (KPI), a **bar** (by tenant) and a **line**
# MAGIC    (monthly trend) bound to the datasets.
# MAGIC 4. **Publish**.
# MAGIC
# MAGIC Run the cells below first to confirm the numbers, then build the dashboard from the
# MAGIC same SQL. Full walkthrough: `solutions/20_solution_e2_dashboard`.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# MAGIC %md **KPI tile** (given)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT round(sum(gwp)) AS total_gwp,
# MAGIC        round(sum(claims) / sum(policies), 4) AS claim_frequency
# MAGIC FROM 3_gold_portfolio_summary;

# COMMAND ----------

# MAGIC %md **Bar tile** — TODO: group premium and claims by `tenant`

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: SELECT tenant, sum(gwp), sum(claims) FROM 3_gold_portfolio_summary GROUP BY tenant
# MAGIC SELECT * FROM 3_gold_portfolio_summary LIMIT 5;

# COMMAND ----------

# MAGIC %md **Line tile** — TODO: monthly incurred trend by tenant from `3_gold_loss_ratio_monthly`

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: SELECT tenant, month, sum(incurred) FROM 3_gold_loss_ratio_monthly GROUP BY tenant, month ORDER BY month
# MAGIC SELECT * FROM 3_gold_loss_ratio_monthly LIMIT 5;

# COMMAND ----------

# MAGIC %md ✅ **Done** once your published dashboard shows the KPI, by-tenant bar and trend line. Next: `F1`.
