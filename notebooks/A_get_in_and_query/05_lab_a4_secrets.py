# Databricks notebook source
# MAGIC %md
# MAGIC # A4 — Store credentials safely with secrets
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** a real product connects to other systems, and those connections
# MAGIC need credentials. Never paste a password into a notebook — put it in a **secret scope**
# MAGIC and read it back by name.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Create a scope and add a secret (one-off, in a terminal)
# MAGIC ```bash
# MAGIC databricks secrets create-scope keystone_workshop
# MAGIC databricks secrets put-secret keystone_workshop demo_api_key --string-value "s3cr3t-value"
# MAGIC ```

# COMMAND ----------

# MAGIC %md ## 2. Read the secret in code — by name, never by value

# COMMAND ----------

SCOPE = "keystone_workshop"
KEY = "demo_api_key"

print("scopes visible to you:", [s.name for s in dbutils.secrets.listScopes()])

# TODO: read the secret with dbutils.secrets.get(scope=..., key=...) and print its length.
# Note: printed secrets are automatically redacted in cell output.
# value = dbutils.secrets.get(scope=SCOPE, key=KEY)
# print(len(value))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Why this matters
# MAGIC The value never appears in the notebook source or in Git; Databricks redacts printed
# MAGIC secrets; access is governed by ACLs.

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: **B1 — File upload**.
