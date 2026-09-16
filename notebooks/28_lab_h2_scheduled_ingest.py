# Databricks notebook source
# MAGIC %md
# MAGIC # H2 — Copy vs federate: scheduled ingestion from Snowflake · *Optional*
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company is fictional.
# MAGIC
# MAGIC **What is this for.** H1 queried Snowflake *live*. Here you **copy** the table into a
# MAGIC managed Delta table, refresh it incrementally with `MERGE`, and see how to schedule
# MAGIC it — then weigh copy vs federate.
# MAGIC
# MAGIC > **Note.** Databricks *Lakeflow Connect* has managed connectors for sources like SQL
# MAGIC > Server, Salesforce and ServiceNow (not Snowflake today), so we ingest via the H1
# MAGIC > federation connection on a schedule.
# MAGIC >
# MAGIC > ⚠️ **Optional — needs Snowflake + lab H1 first.** Set **snowflake_configured** to
# MAGIC > `yes` once H1 has run. Stuck? See `solutions/28_solution_h2_scheduled_ingest`.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

dbutils.widgets.dropdown("snowflake_configured", "no", ["no", "yes"], "Snowflake set up (H1 done)?")
dbutils.widgets.text("sf_schema", "PUBLIC", "Snowflake schema")
dbutils.widgets.text("sf_table", "POLICIES", "Snowflake table")
dbutils.widgets.text("key_column", "policy_id", "Primary key column for MERGE")

CONFIGURED = dbutils.widgets.get("snowflake_configured") == "yes"
SF_SCHEMA = dbutils.widgets.get("sf_schema")
SF_TABLE = dbutils.widgets.get("sf_table")
KEY = dbutils.widgets.get("key_column")
FOREIGN_CATALOG = "keystone_snowflake_cat"       # created in H1
SOURCE = f"{FOREIGN_CATALOG}.{SF_SCHEMA}.{SF_TABLE}"
TARGET = f"{FQ}.4_ingested_snowflake"

if not CONFIGURED:
    print("Optional lab — run H1 first, then set 'snowflake_configured' to 'yes'.")
    dbutils.notebook.exit("skipped: snowflake not configured")

# COMMAND ----------

# MAGIC %md ## 1. First load — CTAS the federated table into a managed table

# COMMAND ----------

# TODO: CREATE OR REPLACE TABLE {TARGET} AS SELECT * FROM {SOURCE}; then print a count.

# COMMAND ----------

# MAGIC %md ## 2. Incremental refresh with MERGE (upsert on the key column)

# COMMAND ----------

# TODO: MERGE INTO {TARGET} t USING {SOURCE} s ON t.{KEY}=s.{KEY}
#       WHEN MATCHED THEN UPDATE SET *  WHEN NOT MATCHED THEN INSERT *

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Put it on a schedule
# MAGIC Wrap this notebook in a **Job** (like lab D2): Jobs & Pipelines → Create → Job → add
# MAGIC a task on this notebook → set an hourly schedule → save.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Copy vs federate
# MAGIC Federate (H1) = always fresh, no storage, but every read hits Snowflake.
# MAGIC Copy (H2) = fast local reads, protects the source, but only as fresh as the last run.

# COMMAND ----------

# MAGIC %md ✅ **Done.** That's the optional Snowflake track.
