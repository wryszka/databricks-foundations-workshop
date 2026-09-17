# Databricks notebook source
# MAGIC %md
# MAGIC # H2 — Copy vs federate: scheduled ingestion from Snowflake · *Optional*
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company is fictional.
# MAGIC
# MAGIC **What is this for.** Lab H1 queried Snowflake *live*. Sometimes you'd rather **copy**
# MAGIC the data into a managed Delta table on a schedule — so reads are fast, cheap, and don't
# MAGIC hammer the source. Here you ingest the Snowflake table into a Keystone table, refresh
# MAGIC it incrementally with `MERGE`, and see how you'd schedule it. You then weigh copy vs
# MAGIC federate.
# MAGIC
# MAGIC > **Note on managed connectors.** Databricks *Lakeflow Connect* offers fully-managed
# MAGIC > ingestion connectors for sources like SQL Server, Salesforce and ServiceNow. Snowflake
# MAGIC > is not one of those today, so we ingest through the **federation connection** from H1
# MAGIC > on a schedule — same idea, and it reuses what you already built.
# MAGIC >
# MAGIC > ⚠️ **Optional — needs Snowflake + lab H1 first** (it uses the foreign catalog H1
# MAGIC > created). Set **snowflake_configured** to `yes` once H1 has run.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

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

# MAGIC %md
# MAGIC ## 1. First load — copy the Snowflake table into a managed Delta table
# MAGIC `CREATE TABLE AS SELECT` (CTAS) reads the federated source once and materialises it
# MAGIC as a normal Databricks table you own.

# COMMAND ----------

spark.sql(f"CREATE OR REPLACE TABLE {TARGET} AS SELECT * FROM {SOURCE}")
print("rows ingested:", spark.sql(f"SELECT count(*) FROM {TARGET}").first()[0])

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Incremental refresh with MERGE
# MAGIC On later runs you don't reload everything — you `MERGE` the current Snowflake rows
# MAGIC into the target: update rows that changed, insert new ones. (This is the same upsert
# MAGIC pattern as lab B3, now against the federated source.)

# COMMAND ----------

spark.sql(f"""
    MERGE INTO {TARGET} AS t
    USING {SOURCE} AS s
    ON t.{KEY} = s.{KEY}
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *
""")
print("after merge:", spark.sql(f"SELECT count(*) FROM {TARGET}").first()[0])

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Put it on a schedule
# MAGIC To make the refresh run automatically, wrap this notebook in a **Job** (exactly like
# MAGIC lab D2): **Jobs & Pipelines → Create → Job**, add a task pointing at this notebook,
# MAGIC set a schedule (say hourly), and save. Each run brings the Keystone copy up to date.
# MAGIC
# MAGIC > 💡 **Genie Code:** ask it to "MERGE the latest rows from the foreign table into
# MAGIC > `4_ingested_snowflake` on the key column" and it will draft the SQL.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Copy vs federate — the trade-off
# MAGIC | | Federate (H1) | Copy on a schedule (H2) |
# MAGIC |---|---|---|
# MAGIC | Freshness | always current | as fresh as the last run |
# MAGIC | Speed of reads | depends on Snowflake | fast (local Delta) |
# MAGIC | Load on Snowflake | every query | only at refresh |
# MAGIC | Storage here | none | a copy |
# MAGIC | Works offline from source | no | yes (between refreshes) |
# MAGIC
# MAGIC Rule of thumb: **federate** for occasional or always-fresh needs; **copy** when the
# MAGIC data is read a lot, must be fast, or you want to protect the source.

# COMMAND ----------

# MAGIC %md ✅ **Done.** That's the optional Snowflake track.
