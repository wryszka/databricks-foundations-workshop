# Databricks notebook source
# MAGIC %md
# MAGIC # D2 — Schedule the pipeline as a Job
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** a pipeline you have to press "start" on by hand isn't production.
# MAGIC A **Job** runs it on a schedule and can chain **dependent tasks**. Here the job runs the
# MAGIC D1 pipeline, then a second task that runs a quick data-quality check after it succeeds.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Do it in the UI
# MAGIC **Workflows → Jobs → Create job**:
# MAGIC 1. Task 1 — type **Pipeline**, select your D1 pipeline.
# MAGIC 2. Task 2 — type **Notebook**, select a check notebook, **Depends on** Task 1.
# MAGIC 3. Add a **Schedule** (e.g. daily) or a trigger. Save and **Run now** to test.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Or as JSON (Jobs API / `databricks jobs create --json`)
# MAGIC Replace `<PIPELINE_ID>` and the notebook path. Two tasks; the check runs only after the
# MAGIC pipeline succeeds. On serverless, notebook tasks need no cluster.
# MAGIC ```json
# MAGIC {
# MAGIC   "name": "keystone-nightly",
# MAGIC   "tasks": [
# MAGIC     {
# MAGIC       "task_key": "run_pipeline",
# MAGIC       "pipeline_task": { "pipeline_id": "<PIPELINE_ID>" }
# MAGIC     },
# MAGIC     {
# MAGIC       "task_key": "quality_check",
# MAGIC       "depends_on": [ { "task_key": "run_pipeline" } ],
# MAGIC       "notebook_task": {
# MAGIC         "notebook_path": "/Workspace/.../databricks-foundations-workshop/solutions/18_solution_d2_job",
# MAGIC         "base_parameters": { "catalog": "main", "schema": "keystone_you" }
# MAGIC       }
# MAGIC     }
# MAGIC   ],
# MAGIC   "schedule": {
# MAGIC     "quartz_cron_expression": "0 0 2 * * ?",
# MAGIC     "timezone_id": "UTC",
# MAGIC     "pause_status": "PAUSED"
# MAGIC   }
# MAGIC }
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## The quality-check task (this cell can be the second task's body)
# MAGIC When this notebook runs as task 2, it verifies the gold table the pipeline produced.

# COMMAND ----------

# MAGIC %run ../notebooks/00_config

# COMMAND ----------

# A light post-pipeline assertion. Uses the build_all gold table if the pipeline hasn't run.
tbl = "gold_portfolio_summary"
if not spark.catalog.tableExists(f"{FQ}.{tbl}"):
    tbl = "3_gold_portfolio_summary"
rows = spark.table(f"{FQ}.{tbl}").count()
tenants = spark.sql(f"SELECT count(DISTINCT tenant) n FROM {FQ}.{tbl}").first()["n"]
print(f"{tbl}: {rows} rows across {tenants} tenants")
assert rows > 0 and tenants >= 1, "gold table looks empty — pipeline may not have run"
print("quality check passed ✅")

# COMMAND ----------

# MAGIC %md ✅ **Done.** That's Track D. Next: `E1 — ask questions in plain language (Genie)`.
