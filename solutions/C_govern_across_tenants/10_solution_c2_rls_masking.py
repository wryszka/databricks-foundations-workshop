# Databricks notebook source
# MAGIC %md
# MAGIC # C2 — Row-level security and column masking
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** the alternative to a schema per tenant is one **shared** table
# MAGIC that every tenant reads — but each sees only their own rows, with sensitive columns
# MAGIC masked. Unity Catalog does this with a **row filter** and a **column mask**: SQL
# MAGIC functions you attach to a table.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

# COMMAND ----------

# MAGIC %md ## A shared table to protect (a copy, so we don't alter the originals)

# COMMAND ----------

spark.sql(f"CREATE OR REPLACE TABLE {FQ}.c2_shared_policies AS SELECT * FROM {FQ}.`2_silver_policies`")
print("c2_shared_policies ready")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Row filter — each tenant sees only their rows
# MAGIC The filter function returns TRUE for rows a caller may see. We map the caller's group
# MAGIC to a tenant with `is_account_group_member`; admins (a group we treat as privileged)
# MAGIC see everything. In the workshop you would create one group per tenant.

# COMMAND ----------

spark.sql(f"""
    CREATE OR REPLACE FUNCTION {FQ}.rf_tenant(tenant_col STRING)
    RETURN
        is_account_group_member('account users')          -- everyone in this lab, stands in for "admin"
        OR is_account_group_member(concat('tenant_', tenant_col))
""")
spark.sql(f"ALTER TABLE {FQ}.c2_shared_policies SET ROW FILTER {FQ}.rf_tenant ON (tenant)")
print("row filter applied on (tenant)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Column mask — redact a sensitive column
# MAGIC We mask `driver_age` (a stand-in for personal data): privileged callers see the real
# MAGIC value, everyone else sees NULL.

# COMMAND ----------

spark.sql(f"""
    CREATE OR REPLACE FUNCTION {FQ}.mask_age(age INT)
    RETURN CASE WHEN is_account_group_member('account users') THEN age ELSE NULL END
""")
spark.sql(f"ALTER TABLE {FQ}.c2_shared_policies ALTER COLUMN driver_age SET MASK {FQ}.mask_age")
print("column mask applied on driver_age")

# COMMAND ----------

# MAGIC %md ## 3. Query it — the filter and mask apply automatically

# COMMAND ----------

display(spark.sql(f"SELECT tenant, driver_age, annual_premium FROM {FQ}.c2_shared_policies LIMIT 10"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## What this proves (and its limit)
# MAGIC The row filter and mask are attached to the **table**, so they apply no matter how the
# MAGIC data is queried (SQL, Python, a dashboard, an app). As the lab owner you are in
# MAGIC `account users`, so you see everything — to watch a non-privileged caller get filtered
# MAGIC rows and NULL ages you need a second identity that is only in one `tenant_*` group.
# MAGIC
# MAGIC Clean up (optional): `ALTER TABLE ... DROP ROW FILTER` / `ALTER COLUMN ... DROP MASK`.

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C3 — managed vs external tables`.
