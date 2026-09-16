# Databricks notebook source
# MAGIC %md
# MAGIC # G1 — An operational database with instant branching (Lakebase)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** an *application* needs fast, row-at-a-time lookups. **Lakebase** is
# MAGIC managed Postgres inside Databricks. You will sync a gold table into it, then use
# MAGIC **instant branching** to spin up a throwaway copy of the database for a what-if.
# MAGIC
# MAGIC Real provisioning is gated behind the `provision` widget (default **no**).

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

import requests, json
ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
HOST = ctx.apiUrl().get()
TOKEN = ctx.apiToken().get()
H = {"Authorization": f"Bearer {TOKEN}"}
INSTANCE = f"keystone-{SCHEMA}".replace("_", "-")[:60]

def api(method, path, body=None):
    r = requests.request(method, f"{HOST}{path}", headers=H, json=body)
    return r.status_code, (r.json() if r.text else {})

# COMMAND ----------

# MAGIC %md ### 1. List existing Lakebase instances
# MAGIC TODO 1: GET `/api/2.0/database/instances` with `api(...)` and print each instance's
# MAGIC name + state. (Confirms the API is reachable.)

# COMMAND ----------

# your code here

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Create an instance *(guarded — set provision=yes to run)*

# COMMAND ----------

dbutils.widgets.dropdown("provision", "no", ["no", "yes"], "Actually create infra?")
PROVISION = dbutils.widgets.get("provision") == "yes"

# TODO 2: when PROVISION, POST /api/2.0/database/instances with {"name": INSTANCE, "capacity":"CU_1"}.
#         Otherwise just print what you would send.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3. Sync a gold table into Postgres *(guarded)*
# MAGIC TODO 3: when PROVISION, create a synced table from `{FQ}.3_gold_portfolio_summary`
# MAGIC (primary keys tenant/region/cover_type, SNAPSHOT). See the solution for the body shape,
# MAGIC or use the CLI `databricks database create-synced-database-table`.

# COMMAND ----------

# your code here

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. Branch the database (what-if)
# MAGIC Branching = create a child instance from a parent — near-instant, copy-on-write:
# MAGIC ```
# MAGIC databricks database create-database-instance <instance>-whatif --json '{
# MAGIC   "name":"<instance>-whatif","capacity":"CU_1","parent_instance_ref":{"name":"<instance>"}}'
# MAGIC ```

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: `G2` — an app over Genie + Lakebase.
