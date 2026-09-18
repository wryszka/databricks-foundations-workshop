# Databricks notebook source
# MAGIC %md
# MAGIC # H1 — Query Snowflake in place (Lakehouse Federation) · *Optional*
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company is fictional.
# MAGIC
# MAGIC **What is this for.** A Keystone client keeps data in **Snowflake**. *Lakehouse
# MAGIC Federation* lets you query it from Databricks **without copying** — the query runs on
# MAGIC Snowflake and results come back here. You'll register the connection, query it live,
# MAGIC cache it with a Materialized View (MV), and push a native query with `remote_query`.
# MAGIC
# MAGIC > ⚠️ **Optional — needs a Snowflake instance.** Enable it:
# MAGIC > 1. `databricks secrets create-scope keystone_workshop` then
# MAGIC >    `databricks secrets put-secret keystone_workshop snowflake_password`.
# MAGIC > 2. Fill the widgets (host, user, warehouse, database, schema, table).
# MAGIC > 3. Set **snowflake_configured** to `yes` and Run all.
# MAGIC >
# MAGIC > Stuck? The complete version is `solutions/27_solution_h1_snowflake_federation`.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

dbutils.widgets.dropdown("snowflake_configured", "no", ["no", "yes"], "Snowflake set up?")
dbutils.widgets.text("sf_host", "<account>.snowflakecomputing.com", "Snowflake host")
dbutils.widgets.text("sf_user", "KEYSTONE_SVC", "Snowflake user")
dbutils.widgets.text("sf_warehouse", "COMPUTE_WH", "Snowflake warehouse")
dbutils.widgets.text("sf_database", "INSURANCE", "Snowflake database")
dbutils.widgets.text("sf_schema", "PUBLIC", "Snowflake schema")
dbutils.widgets.text("sf_table", "POLICIES", "Snowflake table")
dbutils.widgets.text("secret_scope", "keystone_workshop", "Secret scope")
dbutils.widgets.text("secret_key", "snowflake_password", "Secret key (password)")

CONFIGURED = dbutils.widgets.get("snowflake_configured") == "yes"
SF = {k: dbutils.widgets.get(k) for k in
      ["sf_host", "sf_user", "sf_warehouse", "sf_database", "sf_schema", "sf_table",
       "secret_scope", "secret_key"]}
CONNECTION = "keystone_snowflake"
FOREIGN_CATALOG = "keystone_snowflake_cat"

if not CONFIGURED:
    print("Optional lab — Snowflake not configured. See the first cell.")
    dbutils.notebook.exit("skipped: snowflake not configured")

# COMMAND ----------

# MAGIC %md ## 1. Create the connection (password comes from the secret, never typed here)

# COMMAND ----------

# TODO: create a connection named `CONNECTION` of TYPE snowflake, using the SF widgets.
# Hint — the password uses: password secret('<scope>', '<key>')
# spark.sql(f"""
#     CREATE CONNECTION IF NOT EXISTS {CONNECTION} TYPE snowflake
#     OPTIONS (host '...', port '443', sfWarehouse '...', user '...',
#              password secret('...', '...'))
# """)

# COMMAND ----------

# MAGIC %md ## 2. Register the Snowflake database as a foreign catalog

# COMMAND ----------

# TODO: CREATE FOREIGN CATALOG {FOREIGN_CATALOG} USING CONNECTION {CONNECTION}
#       OPTIONS (database '<sf_database>'), then SHOW SCHEMAS IN it.

# COMMAND ----------

# MAGIC %md ## 3. Query it in place — no copy

# COMMAND ----------

# TODO: SELECT * ... LIMIT 20 from {FOREIGN_CATALOG}.{sf_schema}.{sf_table}, and a count(*).

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Cache it locally
# MAGIC Ideally a Materialized View (MV) — but MVs aren't enabled on Free Edition serverless,
# MAGIC so try the MV and fall back to a plain Delta table if it fails (same idea).

# COMMAND ----------

# TODO: try `CREATE MATERIALIZED VIEW {FQ}.sf_source_cached AS SELECT * FROM {fq_source}`;
#       in an `except`, fall back to `CREATE OR REPLACE TABLE {FQ}.sf_source_cached AS SELECT ...`.
#       Then SELECT count(*) from it.

# COMMAND ----------

# MAGIC %md ## 5. Push a native query with remote_query

# COMMAND ----------

# TODO: SELECT * FROM remote_query('{CONNECTION}', database => '<sf_database>',
#       query => 'SELECT count(*) AS n FROM <sf_schema>.<sf_table>')
#       (remote_query needs the `database` option; the inner query is native Snowflake SQL.)

# COMMAND ----------

# MAGIC %md ✅ **Done.** Optional next: `28 — H2 scheduled ingestion`.
