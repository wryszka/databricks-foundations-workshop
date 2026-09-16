# Databricks notebook source
# MAGIC %md
# MAGIC # D2 — Schedule the pipeline as a Job
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** run the D1 pipeline on a schedule with a **dependent** check task.
# MAGIC Mostly a UI/JSON exercise — answer in `solutions/18_solution_d2_job`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Build the job in the UI
# MAGIC **Workflows → Jobs → Create job**:
# MAGIC - Task 1 (**Pipeline**): your D1 pipeline.
# MAGIC - Task 2 (**Notebook**): a check notebook, **Depends on** Task 1.
# MAGIC - Add a **Schedule**, Save, **Run now**.
# MAGIC
# MAGIC ## 2. Write the quality-check cell (task 2's body)
# MAGIC Fill in the TODO: assert the gold table the pipeline produced has rows across tenants.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# TODO: pick gold_portfolio_summary (or 3_gold_portfolio_summary as fallback),
#       count rows and distinct tenants, and assert it isn't empty.

# COMMAND ----------

# MAGIC %md ✅ **Done.** That's Track D. Next: `E1 — Genie`.
