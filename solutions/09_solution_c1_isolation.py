# Databricks notebook source
# MAGIC %md
# MAGIC # C1 — Tenant isolation with schemas and grants
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** Keystone runs one platform for competing insurers, so the
# MAGIC number-one question is *"how do I stop tenant A seeing tenant B's data?"* The
# MAGIC cleanest answer in Unity Catalog is a **schema (or catalog) per tenant** plus
# MAGIC **grants**. Here we split the shared book into a schema per tenant and control access
# MAGIC with `USE SCHEMA` / `SELECT`.

# COMMAND ----------

# MAGIC %run ../notebooks/00_config

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. A schema per tenant
# MAGIC We give each tenant its own schema and load only that tenant's rows into it. (Schema
# MAGIC names are prefixed with your own schema so a shared workspace doesn't collide.)

# COMMAND ----------

for t in TENANTS:
    tenant_schema = f"{SCHEMA}_t_{t}"
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{tenant_schema}")
    spark.sql(f"""
        CREATE OR REPLACE TABLE {CATALOG}.{tenant_schema}.policies AS
        SELECT * FROM {FQ}.`2_silver_policies` WHERE tenant = '{t}'
    """)
    n = spark.table(f"{CATALOG}.{tenant_schema}.policies").count()
    print(f"{tenant_schema}.policies -> {n:,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Grant access to just one tenant's schema
# MAGIC A principal needs `USE CATALOG` + `USE SCHEMA` to *see* a schema and `SELECT` to read
# MAGIC its tables. Here we grant on Bricksurance's schema only. In a real deployment you would
# MAGIC grant each tenant's group to its own schema; we use the built-in `account users` group
# MAGIC so the statements run in the lab.

# COMMAND ----------

bricks = f"{CATALOG}.{SCHEMA}_t_bricksurance_se"
spark.sql(f"GRANT USE SCHEMA ON SCHEMA {bricks} TO `account users`")
spark.sql(f"GRANT SELECT ON TABLE {bricks}.policies TO `account users`")
print("granted USE SCHEMA + SELECT on bricksurance schema to `account users`")

# COMMAND ----------

# MAGIC %md ## 3. Inspect and then revoke

# COMMAND ----------

display(spark.sql(f"SHOW GRANTS ON SCHEMA {bricks}"))

# COMMAND ----------

spark.sql(f"REVOKE SELECT ON TABLE {bricks}.policies FROM `account users`")
spark.sql(f"REVOKE USE SCHEMA ON SCHEMA {bricks} FROM `account users`")
print("revoked — back to owner-only")

# COMMAND ----------

# MAGIC %md
# MAGIC ## What this proves (and its limit)
# MAGIC The isolation boundary is the **schema + grant**: with no `USE SCHEMA`/`SELECT`, a
# MAGIC principal cannot read a tenant's tables. To *see* isolation working you need a second
# MAGIC user identity (or group) that is not you — the owner always sees everything. In the
# MAGIC workshop, pair up and grant each other access to test it live.
# MAGIC
# MAGIC > 💡 **Scaling note:** schema-per-tenant scales to very large numbers of tenants;
# MAGIC > catalog-per-tenant gives even cleaner isolation when you have fewer, larger tenants.

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C2 — row-level security and column masking`.
