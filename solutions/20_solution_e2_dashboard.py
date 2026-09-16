# Databricks notebook source
# MAGIC %md
# MAGIC # E2 — Build a dashboard from Genie's SQL (solution)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** natural-language exploration (lab E1) becomes a durable,
# MAGIC shareable **AI/BI dashboard**. You ask Genie a question, take the SQL it generated,
# MAGIC and drop it into a dashboard as a tile.
# MAGIC
# MAGIC ### Build it (in the UI)
# MAGIC 1. Left sidebar → **Dashboards** → **Create dashboard**.
# MAGIC 2. On the **Data** tab, add a dataset and paste one of the queries below (these are
# MAGIC    the kind of SQL Genie produces — in E1 you can copy your own from **Show generated
# MAGIC    code**).
# MAGIC 3. On the **Canvas** tab, add widgets bound to the datasets: a **counter** for the
# MAGIC    KPI, a **bar** for premium by tenant, a **line** for the monthly trend.
# MAGIC 4. **Publish** and share.
# MAGIC
# MAGIC The cells below run the same SQL so you can confirm the numbers before you build.

# COMMAND ----------

# MAGIC %run ../notebooks/00_config

# COMMAND ----------

# MAGIC %md **KPI tile** — total gross written premium and overall claim frequency

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT round(sum(gwp)) AS total_gwp,
# MAGIC        round(sum(claims) / sum(policies), 4) AS claim_frequency
# MAGIC FROM 3_gold_portfolio_summary;

# COMMAND ----------

# MAGIC %md **Bar tile** — premium and claims by tenant

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT tenant, round(sum(gwp)) AS gwp, sum(claims) AS claims
# MAGIC FROM 3_gold_portfolio_summary
# MAGIC GROUP BY tenant
# MAGIC ORDER BY gwp DESC;

# COMMAND ----------

# MAGIC %md **Line tile** — monthly incurred trend by tenant

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT tenant, month, round(sum(incurred)) AS incurred
# MAGIC FROM 3_gold_loss_ratio_monthly
# MAGIC GROUP BY tenant, month
# MAGIC ORDER BY month;

# COMMAND ----------

# MAGIC %md
# MAGIC > 💡 **Genie Code:** you can also prompt Genie Code to generate a starter dashboard
# MAGIC > definition, then tweak it.
# MAGIC
# MAGIC ✅ **Done** once your dashboard shows the KPI, the by-tenant bar, and the trend line.
# MAGIC Next: `F1` — share a table with another attendee.
