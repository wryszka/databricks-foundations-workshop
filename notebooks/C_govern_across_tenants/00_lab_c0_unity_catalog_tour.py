# Databricks notebook source
# MAGIC %md
# MAGIC # C0 — Unity Catalog tour (start here)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for.** Before the governance labs, this is a **guided tour of Unity
# MAGIC Catalog (UC)** — the part of Databricks that organises and secures everything. Unlike
# MAGIC the other labs there are no gaps to fill: **read each markdown note, then run the cell
# MAGIC under it.** By the end you'll have seen — and created — every kind of object UC
# MAGIC governs, and you'll understand how access is controlled.
# MAGIC
# MAGIC You will meet: **metastore, catalog, schema (a.k.a. database), table, view, volume,
# MAGIC function, (registered) model, grants/privileges, RBAC and ABAC (tags)**.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0. The big picture — how everything nests
# MAGIC
# MAGIC Unity Catalog is one **governance layer** across all your workspaces. Everything lives
# MAGIC in a three-level namespace `catalog.schema.object`:
# MAGIC
# MAGIC ```
# MAGIC Metastore                     ← one per region; the top-level UC container
# MAGIC └── Catalog                   ← a top-level bucket (e.g. per environment or product)
# MAGIC     └── Schema  (= "database")← a folder of objects
# MAGIC         ├── Table             ← rows & columns (stored as Delta)
# MAGIC         ├── View              ← a saved query that looks like a table
# MAGIC         ├── Volume            ← a folder for FILES (non-tabular: CSV, PDF, images…)
# MAGIC         ├── Function          ← reusable SQL/Python logic you call in queries
# MAGIC         └── Model             ← a registered machine-learning model + its versions
# MAGIC ```
# MAGIC
# MAGIC **"Schema" and "database" mean the same thing** in Databricks — `CREATE SCHEMA` and
# MAGIC `CREATE DATABASE` are interchangeable. Access to every object above is controlled by
# MAGIC **privileges** you `GRANT` to users/groups (more on that at the end).

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Where am I right now?
# MAGIC Every session sits in a current metastore, catalog and schema. `00_config` already put
# MAGIC you in your own schema.

# COMMAND ----------

display(spark.sql("SELECT current_metastore() AS metastore, current_catalog() AS catalog, current_schema() AS schema"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Catalogs — the top-level buckets
# MAGIC List the catalogs you can see. A catalog groups schemas; a common pattern is one
# MAGIC catalog per environment (dev/prod) or per product. (On Free Edition you usually have
# MAGIC the built-in `main` catalog and can't create new ones — that needs admin rights.)

# COMMAND ----------

display(spark.sql("SHOW CATALOGS"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Schemas (databases) — folders of objects
# MAGIC A **schema** groups your tables, views, volumes, functions and models. You're working
# MAGIC in your own schema so nothing clashes with other people. `CREATE SCHEMA` = `CREATE
# MAGIC DATABASE`.

# COMMAND ----------

print(f"Your schema: {FQ}")
display(spark.sql(f"SHOW SCHEMAS IN {CATALOG} LIKE 'keystone*'"))
display(spark.sql(f"SHOW TABLES IN {FQ}"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Tables — rows and columns
# MAGIC Tables hold structured data (stored in the **Delta** format). Let's create a small
# MAGIC reference table of regions and their risk factor, then describe it.

# COMMAND ----------

spark.sql(f"""
    CREATE OR REPLACE TABLE {FQ}.uc_tour_regions (
        region STRING,
        risk_factor DOUBLE COMMENT 'relative claim risk vs average'
    )
""")
spark.sql(f"""
    INSERT OVERWRITE {FQ}.uc_tour_regions VALUES
    ('Metro North',1.25),('Metro South',1.10),('Coastal',1.05),('Central',1.00),
    ('Highland',0.92),('Lakes',0.95),('Border',0.98),('Western',0.90)
""")
display(spark.sql(f"DESCRIBE TABLE {FQ}.uc_tour_regions"))
display(spark.sql(f"SELECT * FROM {FQ}.uc_tour_regions ORDER BY risk_factor DESC"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Views — a saved query that behaves like a table
# MAGIC A **view** stores no data; it's a named query. Great for exposing a curated slice
# MAGIC without copying anything.

# COMMAND ----------

spark.sql(f"""
    CREATE OR REPLACE VIEW {FQ}.v_uc_tour_high_risk AS
    SELECT region, risk_factor FROM {FQ}.uc_tour_regions WHERE risk_factor >= 1.0
""")
display(spark.sql(f"SELECT * FROM {FQ}.v_uc_tour_high_risk ORDER BY risk_factor DESC"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Volumes — governed folders for FILES
# MAGIC Not everything is a table. A **volume** is a governed place for files (CSV, PDF,
# MAGIC images, model artifacts…). Your workshop already has `raw`, `landing` and `docs`
# MAGIC volumes. Volumes are also `catalog.schema.name`, and you read them by path under
# MAGIC `/Volumes/...`.

# COMMAND ----------

display(spark.sql(f"SHOW VOLUMES IN {FQ}"))
print(f"Files in the raw volume ({RAW_VOLUME}):")
display(dbutils.fs.ls(RAW_VOLUME))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Functions — reusable logic you call in SQL
# MAGIC A **function** is governed logic you can reuse across queries. Here's a tiny SQL
# MAGIC function that buckets a premium into a band, then we use it.

# COMMAND ----------

spark.sql(f"""
    CREATE OR REPLACE FUNCTION {FQ}.premium_band(p DOUBLE)
    RETURNS STRING
    COMMENT 'Bucket an annual premium into low/medium/high'
    RETURN CASE WHEN p < 400 THEN 'low' WHEN p < 700 THEN 'medium' ELSE 'high' END
""")
display(spark.sql(f"""
    SELECT annual_premium, {FQ}.premium_band(annual_premium) AS band
    FROM {FQ}.2_silver_policies LIMIT 10
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Models — registered ML models live in UC too
# MAGIC A trained machine-learning **model** is a first-class UC object with **versions** and
# MAGIC **aliases** (e.g. `@champion`). We register a tiny placeholder model here so you can
# MAGIC see it appear; lab **I2** registers a real one from the data.
# MAGIC
# MAGIC > Needs a recent serverless environment (for the `mlflow` library). If it isn't
# MAGIC > available this cell prints a note and moves on — that's fine.

# COMMAND ----------

try:
    import mlflow
    mlflow.set_registry_uri("databricks-uc")

    class _Const(mlflow.pyfunc.PythonModel):
        def predict(self, ctx, model_input):
            return [0.05] * len(model_input)

    import pandas as pd
    with mlflow.start_run(run_name="uc_tour_placeholder"):
        mlflow.pyfunc.log_model(
            artifact_path="model",
            python_model=_Const(),
            registered_model_name=f"{FQ}.uc_tour_model",
            input_example=pd.DataFrame({"x": [1.0]}),
        )
    print(f"registered model {FQ}.uc_tour_model")
    display(spark.sql(f"SHOW MODELS IN {FQ}"))
except Exception as e:
    print("Skipped model registration (needs a recent serverless environment for mlflow):")
    print(f"  {type(e).__name__}: {str(e)[:200]}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Permissions & privileges — who can do what
# MAGIC Access is granted per object. To *read* a table a user needs a chain of privileges:
# MAGIC `USE CATALOG` on the catalog, `USE SCHEMA` on the schema, and `SELECT` on the table.
# MAGIC Other common privileges: `MODIFY` (write), `EXECUTE` (functions), `ALL PRIVILEGES`,
# MAGIC and every object has an **owner** who can manage it.
# MAGIC
# MAGIC Below we grant read access on our table to the built-in `account users` group, then
# MAGIC list the grants. (Wrapped so it prints a note if you lack grant rights here.)

# COMMAND ----------

try:
    spark.sql(f"GRANT SELECT ON TABLE {FQ}.uc_tour_regions TO `account users`")
    print("granted SELECT on uc_tour_regions to `account users`")
except Exception as e:
    print(f"Grant skipped (need manage rights): {type(e).__name__}: {str(e)[:150]}")
display(spark.sql(f"SHOW GRANTS ON TABLE {FQ}.uc_tour_regions"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10. RBAC vs ABAC — two ways to decide access
# MAGIC
# MAGIC - **RBAC (Role-Based Access Control)** — the grants above: you give *this group* the
# MAGIC   *SELECT* privilege on *this object*. Access follows **who you are** (your group/role).
# MAGIC - **ABAC (Attribute-Based Access Control)** — access follows **attributes** attached to
# MAGIC   data, chiefly **tags**. You tag columns/tables (e.g. `classification = pii`) once, and
# MAGIC   a policy then applies everywhere that tag appears — no per-object grant needed.
# MAGIC
# MAGIC Below we tag a column, then read the tag back. The enforcement side of ABAC —
# MAGIC **column masks and row filters** driven by tags/policies — is exactly what you build
# MAGIC hands-on in lab **C2**.

# COMMAND ----------

try:
    spark.sql(f"ALTER TABLE {FQ}.uc_tour_regions ALTER COLUMN risk_factor SET TAGS ('classification' = 'internal')")
    print("tagged uc_tour_regions.risk_factor with classification=internal")
    display(spark.sql(f"""
        SELECT column_name, tag_name, tag_value
        FROM {CATALOG}.information_schema.column_tags
        WHERE schema_name = '{SCHEMA}' AND table_name = 'uc_tour_regions'
    """))
except Exception as e:
    print(f"Column tagging skipped on this workspace: {type(e).__name__}: {str(e)[:180]}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11. Finding & tracing things
# MAGIC - **Catalog Explorer** (left menu → **Catalog**) is the point-and-click browser for
# MAGIC   everything above, with a **Permissions** tab and a **Lineage** graph per table.
# MAGIC - `information_schema` (per catalog) is the queryable metadata; `system.*` tables hold
# MAGIC   account-wide access, lineage and cost history (lab **C8**).

# COMMAND ----------

display(spark.sql(f"SELECT table_name, table_type FROM {CATALOG}.information_schema.tables WHERE table_schema = '{SCHEMA}' ORDER BY table_name"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Recap
# MAGIC | Object | What it is | You created |
# MAGIC |---|---|---|
# MAGIC | Catalog | top-level bucket of schemas | (listed) |
# MAGIC | Schema / database | folder of objects | your workshop schema |
# MAGIC | Table | rows & columns (Delta) | `uc_tour_regions` |
# MAGIC | View | a saved query | `v_uc_tour_high_risk` |
# MAGIC | Volume | governed folder for files | `raw` / `landing` / `docs` |
# MAGIC | Function | reusable logic | `premium_band` |
# MAGIC | Model | registered ML model + versions | `uc_tour_model` (if env allowed) |
# MAGIC | Grant | a privilege given to a principal | `SELECT` to `account users` |
# MAGIC | Tag | an attribute for ABAC | `classification=internal` |
# MAGIC
# MAGIC ✅ **Done.** Now do the governance labs, starting with **C1 — tenant isolation**.
