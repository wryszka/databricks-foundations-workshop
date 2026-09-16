# Databricks notebook source
# MAGIC %md
# MAGIC # A4 — Store credentials safely with secrets
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** a real product connects to other systems, and those connections
# MAGIC need credentials. You never paste a password into a notebook — you put it in a **secret
# MAGIC scope** and read it back by name. (This is what Track H would use to reach an external
# MAGIC database.)

# COMMAND ----------

# MAGIC %run ../notebooks/00_config

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Create a scope and add a secret (one-off, in a terminal)
# MAGIC Secrets are created with the CLI (or the Secrets API), not from a notebook:
# MAGIC ```bash
# MAGIC databricks secrets create-scope keystone_workshop
# MAGIC databricks secrets put-secret keystone_workshop demo_api_key --string-value "s3cr3t-value"
# MAGIC ```
# MAGIC On Free Edition you run these from your own machine's Databricks CLI against your
# MAGIC workspace.

# COMMAND ----------

# MAGIC %md ## 2. Read the secret in code — by name, never by value

# COMMAND ----------

SCOPE = "keystone_workshop"
KEY = "demo_api_key"

scopes = [s.name for s in dbutils.secrets.listScopes()]
print(f"scopes visible to you: {scopes}")

if SCOPE in scopes:
    value = dbutils.secrets.get(scope=SCOPE, key=KEY)          # returns the real value...
    print(f"read '{KEY}' from '{SCOPE}'. Length = {len(value)} chars.")
    print(f"Notebook output redacts it automatically: {value}")  # ...but output shows [REDACTED]
else:
    print(f"Scope '{SCOPE}' not found yet — create it with the CLI in step 1, then re-run.")
    print("The pattern is always: dbutils.secrets.get(scope=..., key=...)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Why this matters
# MAGIC - The value never appears in the notebook source or in Git.
# MAGIC - Databricks **redacts** any printed secret in cell output (see above).
# MAGIC - Access to a scope is governed by ACLs, so only the right people can read it.

# COMMAND ----------

# MAGIC %md ✅ **Done.** Credentials are handled safely. Next: **B1 — File upload**.
