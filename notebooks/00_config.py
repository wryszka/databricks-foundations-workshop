# Databricks notebook source
# MAGIC %md
# MAGIC # 00 — Config
# MAGIC
# MAGIC **About this workshop:** all data is synthetic and generated on the fly. Every
# MAGIC company named here is fictional. Nothing is real customer, policy, or claims data.
# MAGIC
# MAGIC ### The scenario
# MAGIC You work at **Keystone**, a (fictional) company that provides a shared data platform
# MAGIC to insurers. Three client insurers — **Bricksurance SE**, **Northwind Mutual**, and
# MAGIC **Helios Re** — are your *tenants*. Today you build the platform underneath them:
# MAGIC bring their data in, transform it, keep each tenant safely isolated, share results,
# MAGIC and put a small app in front of it.
# MAGIC
# MAGIC Set the catalog and schema **once here**. Every other notebook runs this via
# MAGIC `%run ./00_config`.
# MAGIC
# MAGIC | Environment | catalog |
# MAGIC |---|---|
# MAGIC | Databricks Free Edition | `main` |
# MAGIC | Customer / demo workspace | any catalog you can create schemas in |

# COMMAND ----------

# Each attendee works in their OWN schema, so tables, jobs and registered models don't
# collide across a room of people. The default derives from your username — leave it
# alone unless told otherwise.
_user = spark.sql("SELECT current_user()").first()[0]
_user_slug = _user.split("@")[0].replace(".", "_").replace("-", "_").lower()

# Catalog default = the workspace's default catalog. Widgets are PER NOTEBOOK, so a
# hardcoded default would silently point a lab at the wrong catalog even after you fixed
# it elsewhere. Auto-detect makes every notebook land in the right place.
_default_catalog = spark.sql("SELECT current_catalog()").first()[0]
if _default_catalog in ("spark_catalog", "hive_metastore", "system", "samples"):
    _default_catalog = "main"

dbutils.widgets.text("catalog", _default_catalog, "Catalog")
dbutils.widgets.text("schema", f"keystone_{_user_slug}", "Schema")

CATALOG = dbutils.widgets.get("catalog")
SCHEMA = dbutils.widgets.get("schema")
FQ = f"{CATALOG}.{SCHEMA}"

# Volumes: raw (messy one-off files), landing (new files arriving for Auto Loader),
# docs (claim documents for the AI-functions lab).
RAW_VOLUME = f"/Volumes/{CATALOG}/{SCHEMA}/raw"
LANDING_VOLUME = f"/Volumes/{CATALOG}/{SCHEMA}/landing"
DOCS_VOLUME = f"/Volumes/{CATALOG}/{SCHEMA}/docs"

MODEL_NAME = f"{FQ}.keystone_frequency_glm"

# The tenants (fictional client insurers) whose data flows through the whole day.
TENANTS = ["bricksurance_se", "northwind_mutual", "helios_re"]

assert spark.sql(f"SHOW CATALOGS LIKE '{CATALOG}'").count() == 1, (
    f"Catalog '{CATALOG}' not found in this workspace — "
    "set the 'catalog' widget (top of this notebook) to one you can use")

# COMMAND ----------

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {FQ}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {FQ}.raw")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {FQ}.landing")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {FQ}.docs")
spark.sql(f"USE {FQ}")

print(f"Using {FQ}")
print(f"  raw files     -> {RAW_VOLUME}")
print(f"  landing files -> {LANDING_VOLUME}")
print(f"  claim docs    -> {DOCS_VOLUME}")
print(f"  tenants       -> {', '.join(TENANTS)}")
