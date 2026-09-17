# Databricks notebook source
# MAGIC %md
# MAGIC # C2 — Row-level security and column masking
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** one **shared** table that every tenant reads — but each sees only
# MAGIC their own rows, with sensitive columns masked, via a Unity Catalog **row filter** and
# MAGIC **column mask**. Fill in the `# TODO`s; answer in `solutions/10_solution_c2_rls_masking`.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# MAGIC %md ## A shared table to protect (a copy of 2_silver_policies)

# COMMAND ----------

spark.sql(f"CREATE OR REPLACE TABLE {FQ}.c2_shared_policies AS SELECT * FROM {FQ}.`2_silver_policies`")

# COMMAND ----------

# MAGIC %md ## 1. Create a row-filter function and attach it on (tenant)

# COMMAND ----------

# TODO: CREATE OR REPLACE FUNCTION {FQ}.rf_tenant(tenant_col STRING) RETURN <boolean expr>
#       using is_account_group_member(...) so a caller only sees their tenant's rows
# TODO: ALTER TABLE {FQ}.c2_shared_policies SET ROW FILTER {FQ}.rf_tenant ON (tenant)

# COMMAND ----------

# MAGIC %md ## 2. Create a column-mask function and attach it on driver_age

# COMMAND ----------

# TODO: CREATE OR REPLACE FUNCTION {FQ}.mask_age(age INT) RETURN <NULL unless privileged>
# TODO: ALTER TABLE {FQ}.c2_shared_policies ALTER COLUMN driver_age SET MASK {FQ}.mask_age

# COMMAND ----------

# MAGIC %md ## 3. Query it and see the filter + mask apply

# COMMAND ----------

# TODO: display(spark.sql(f"SELECT tenant, driver_age, annual_premium FROM {FQ}.c2_shared_policies LIMIT 10"))

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `C3 — managed vs external tables`.
