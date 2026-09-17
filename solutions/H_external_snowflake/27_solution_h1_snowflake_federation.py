# Databricks notebook source
# MAGIC %md
# MAGIC # H1 — Query Snowflake in place (Lakehouse Federation) · *Optional*
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company is fictional.
# MAGIC
# MAGIC **What is this for.** One of your Keystone clients keeps data in **Snowflake** (a
# MAGIC different cloud data warehouse). *Lakehouse Federation* lets you register that
# MAGIC Snowflake database as a **foreign catalog** and query it from Databricks **without
# MAGIC copying the data** — the query runs against Snowflake and the results come back here.
# MAGIC You then compare three patterns: live query, a cached **Materialized View (MV)**, and
# MAGIC pushing a native query straight to Snowflake with `remote_query`.
# MAGIC
# MAGIC > ⚠️ **Optional — needs a Snowflake instance.** This lab does nothing until you point
# MAGIC > it at a real Snowflake account. To enable it:
# MAGIC > 1. Store the Snowflake password in a secret: in a terminal
# MAGIC >    `databricks secrets create-scope keystone_workshop` (ignore if it exists) then
# MAGIC >    `databricks secrets put-secret keystone_workshop snowflake_password`.
# MAGIC > 2. Fill the widgets below (host, user, warehouse, database, schema, table).
# MAGIC > 3. Set the **snowflake_configured** widget to `yes` and Run all.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

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
    print("Optional lab — Snowflake not configured. Follow the steps in the first cell,")
    print("then set the 'snowflake_configured' widget to 'yes' and Run all.")
    dbutils.notebook.exit("skipped: snowflake not configured")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Create the connection to Snowflake
# MAGIC A **connection** holds where Snowflake is and how to sign in. The password is read
# MAGIC from a secret, never written in the notebook. Connections live at the metastore
# MAGIC level — creating one needs the `CREATE CONNECTION` privilege.

# COMMAND ----------

spark.sql(f"""
    CREATE CONNECTION IF NOT EXISTS {CONNECTION} TYPE snowflake
    OPTIONS (
        host '{SF["sf_host"]}',
        port '443',
        sfWarehouse '{SF["sf_warehouse"]}',
        user '{SF["sf_user"]}',
        password secret('{SF["secret_scope"]}', '{SF["secret_key"]}')
    )
""")
print(f"connection {CONNECTION} ready")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Register the Snowflake database as a foreign catalog
# MAGIC Now the whole Snowflake database appears in the Databricks **Catalog** browser, and
# MAGIC you can query its tables with three-level names `catalog.schema.table`.

# COMMAND ----------

spark.sql(f"""
    CREATE FOREIGN CATALOG IF NOT EXISTS {FOREIGN_CATALOG}
    USING CONNECTION {CONNECTION}
    OPTIONS (database '{SF["sf_database"]}')
""")
display(spark.sql(f"SHOW SCHEMAS IN {FOREIGN_CATALOG}"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Query it in place — no copy
# MAGIC This SELECT runs against Snowflake live; Databricks just hands you the result.

# COMMAND ----------

fq_source = f"{FOREIGN_CATALOG}.{SF['sf_schema']}.{SF['sf_table']}"
display(spark.sql(f"SELECT * FROM {fq_source} LIMIT 20"))
print("row count in Snowflake:", spark.sql(f"SELECT count(*) FROM {fq_source}").first()[0])

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Cache it with a Materialized View (MV)
# MAGIC If the same federated data is read often, a **Materialized View** stores a local
# MAGIC copy that refreshes on demand — faster and it takes load off Snowflake. (An MV is a
# MAGIC managed table on Databricks; it lives in your own schema.)

# COMMAND ----------

spark.sql(f"""
    CREATE MATERIALIZED VIEW IF NOT EXISTS {FQ}.sf_source_cached AS
    SELECT * FROM {fq_source}
""")
display(spark.sql(f"SELECT count(*) AS cached_rows FROM {FQ}.sf_source_cached"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Push a native query straight to Snowflake (`remote_query`)
# MAGIC Sometimes you want Snowflake to do the work in its own dialect and just return the
# MAGIC answer. `remote_query` sends the query text to Snowflake as-is.

# COMMAND ----------

display(spark.sql(f"""
    SELECT * FROM remote_query(
        '{CONNECTION}',
        query => 'SELECT count(*) AS n FROM {SF["sf_database"]}.{SF["sf_schema"]}.{SF["sf_table"]}'
    )
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## When to use which
# MAGIC - **Live query / `remote_query`** — always current, no storage here, but every run hits Snowflake.
# MAGIC - **Materialized View** — fast repeat reads and less load on Snowflake, but as fresh as its last refresh.
# MAGIC
# MAGIC Lab **H2** turns this into a *scheduled copy* and compares the trade-offs.
# MAGIC
# MAGIC > 💡 **Genie Code:** you could ask Genie Code to "create a Snowflake connection and
# MAGIC > foreign catalog, then query table X" and it will draft this SQL for you.

# COMMAND ----------

# MAGIC %md ✅ **Done.** Optional next: `28 — H2 scheduled ingestion`.
