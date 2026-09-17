# Databricks notebook source
# MAGIC %md
# MAGIC # G1 — An operational database with instant branching (Lakebase) (solution)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** the analytical tables you built all day are great for reporting,
# MAGIC but an *application* needs fast, row-at-a-time lookups. **Lakebase** is managed Postgres
# MAGIC inside Databricks. Here you sync a gold table into it, then use **instant branching** to
# MAGIC spin up a throwaway copy of the whole database for a what-if — in seconds, no data copy.
# MAGIC
# MAGIC Provisioning real infrastructure is gated behind the `provision` widget (default **no**)
# MAGIC so this notebook runs safely; flip it to `yes` when you want to create the instance.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

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

# MAGIC %md ### 1. The database API is reachable — list existing instances

# COMMAND ----------

code, out = api("GET", "/api/2.0/database/instances")
print("status", code)
for inst in out.get("database_instances", []):
    print(f"  {inst['name']:40} {inst.get('state'):12} {inst.get('capacity')}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Create a Lakebase instance  *(guarded)*
# MAGIC Smallest capacity is fine for a workshop. Creation takes a few minutes.

# COMMAND ----------

dbutils.widgets.dropdown("provision", "no", ["no", "yes"], "Actually create infra?")
PROVISION = dbutils.widgets.get("provision") == "yes"

if PROVISION:
    code, out = api("POST", "/api/2.0/database/instances",
                    {"name": INSTANCE, "capacity": "CU_1"})
    print("create:", code, json.dumps(out)[:300])
else:
    print("provision=no — would POST /api/2.0/database/instances with:")
    print(json.dumps({"name": INSTANCE, "capacity": "CU_1"}, indent=2))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3. Sync a gold table into Postgres  *(guarded)*
# MAGIC A **synced table** keeps a Postgres copy of a Unity Catalog table up to date, so the
# MAGIC app reads Postgres while the source of truth stays in the lakehouse.
# MAGIC ```
# MAGIC databricks database create-synced-database-table \
# MAGIC   <catalog>.<schema>.portfolio_pg \
# MAGIC   --database-instance-name <instance> \
# MAGIC   --logical-database-name databricks_postgres \
# MAGIC   --json '{"spec":{"source_table_full_name":"<catalog>.<schema>.3_gold_portfolio_summary",
# MAGIC            "primary_key_columns":["tenant","region","cover_type"],
# MAGIC            "scheduling_policy":"SNAPSHOT"}}'
# MAGIC ```

# COMMAND ----------

if PROVISION:
    body = {"name": f"{FQ}.portfolio_pg",
            "spec": {"source_table_full_name": f"{FQ}.3_gold_portfolio_summary",
                     "primary_key_columns": ["tenant", "region", "cover_type"],
                     "scheduling_policy": "SNAPSHOT",
                     "database_instance_name": INSTANCE,
                     "logical_database_name": "databricks_postgres"}}
    code, out = api("POST", "/api/2.0/database/synced_tables", body)
    print("sync:", code, json.dumps(out)[:300])
else:
    print("provision=no — synced-table call skipped (see CLI above).")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. Instant branching — a copy of the whole database in seconds
# MAGIC Branching creates a **child instance** from a parent at a point in time. It is
# MAGIC copy-on-write, so it is near-instant and cheap — ideal for a what-if or a test that you
# MAGIC throw away afterwards.
# MAGIC ```
# MAGIC databricks database create-database-instance <instance>-whatif --json '{
# MAGIC   "name":"<instance>-whatif","capacity":"CU_1",
# MAGIC   "parent_instance_ref":{"name":"<instance>"} }'
# MAGIC ```
# MAGIC Delete it with `databricks database delete-database-instance <instance>-whatif` when done.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5. Connect from code
# MAGIC Generate a short-lived credential, then use any Postgres driver (`psycopg`):
# MAGIC ```python
# MAGIC cred = api("POST", "/api/2.0/database/credentials", {"instance_names":[INSTANCE]})
# MAGIC # host = <instance>.read_write_dns ; user = current_user ; password = cred token
# MAGIC # psycopg.connect(host=..., dbname="databricks_postgres", user=..., password=..., sslmode="require")
# MAGIC ```
# MAGIC Clean up the instance with `databricks database delete-database-instance <instance>`.

# COMMAND ----------

# MAGIC %md
# MAGIC ✅ **Done.** You have an operational database (and know how to branch it). Next: `G2` —
# MAGIC an app that reads from it.
