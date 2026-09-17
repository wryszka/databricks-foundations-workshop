# Databricks notebook source
# MAGIC %md
# MAGIC # C8 — System tables: access, lineage, cost
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** the `system` catalog records the platform's own operations as
# MAGIC queryable tables. Fill in the `# TODO`s; answer in `solutions/16_solution_c8_system_tables`.
# MAGIC Some system schemas may be empty on Free Edition — wrap queries in try/except.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# MAGIC %md ## 1. List the available system schemas

# COMMAND ----------

# TODO: SELECT schema_name FROM system.information_schema.schemata

# COMMAND ----------

# MAGIC %md ## 2. Recent audit activity — who did what

# COMMAND ----------

# TODO: SELECT event_time, action_name, user_identity.email FROM system.access.audit ORDER BY event_time DESC LIMIT 20

# COMMAND ----------

# MAGIC %md ## 3. (If available) usage/cost in DBUs from system.billing.usage

# COMMAND ----------

# TODO: aggregate system.billing.usage over the last 7 days (may be empty on Free Edition)

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `D1 — a declarative pipeline`.
