# Databricks notebook source
# MAGIC %md
# MAGIC # C1 — Tenant isolation with schemas and grants
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** Keystone runs one platform for competing insurers, so the
# MAGIC number-one question is *"how do I stop tenant A seeing tenant B's data?"* The cleanest
# MAGIC answer in Unity Catalog is a **schema (or catalog) per tenant** plus **grants**.
# MAGIC
# MAGIC Fill in the `# TODO`s. A worked answer is in `solutions/09_solution_c1_isolation`.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# MAGIC %md ## 1. Create a schema per tenant and load only that tenant's rows

# COMMAND ----------

for t in TENANTS:
    tenant_schema = f"{SCHEMA}_t_{t}"
    # TODO: create the schema if it doesn't exist
    # spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{tenant_schema}")
    # TODO: create a `policies` table in it holding only rows WHERE tenant = '{t}'
    #       from {FQ}.`2_silver_policies`
    print(tenant_schema)

# COMMAND ----------

# MAGIC %md ## 2. Grant USE SCHEMA + SELECT on ONE tenant's schema to `account users`

# COMMAND ----------

bricks = f"{CATALOG}.{SCHEMA}_t_bricksurance_se"
# TODO: GRANT USE SCHEMA ON SCHEMA {bricks} TO `account users`
# TODO: GRANT SELECT ON TABLE {bricks}.policies TO `account users`

# COMMAND ----------

# MAGIC %md ## 3. Show the grants, then revoke them

# COMMAND ----------

# TODO: display(spark.sql(f"SHOW GRANTS ON SCHEMA {bricks}"))
# TODO: REVOKE both grants

# COMMAND ----------

# MAGIC %md
# MAGIC **Think about:** why does the owner still see every schema? What would you need to
# MAGIC actually *prove* tenant B cannot read tenant A's data? (Answer: a second identity —
# MAGIC pair up in the workshop and grant each other access.)

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C2 — row-level security and column masking`.
