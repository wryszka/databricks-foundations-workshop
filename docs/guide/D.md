## Track D — Transform and schedule it

So far you've written transformations by hand in notebooks. This track shows the production
way to do it: a **declarative pipeline** where you simply declare the tables you want and the
quality rules they must meet, and Databricks works out the order, does it incrementally, and
quarantines bad rows for you — then you schedule the whole thing to run automatically with a
**Job**. This is the transform layer that keeps the Keystone platform's tables fresh.

### D1. A Spark Declarative Pipeline (Lakeflow)

**What this is.** A **pipeline** is a set of table definitions plus quality rules; the
platform figures out how to build them in the right order and drops rows that fail the rules
(so bad data never reaches your clean tables). You'll take the messy raw CSV files and build
a clean **bronze → silver → gold** chain: bronze = raw as received, silver = typed and
cleaned, gold = a per-tenant summary. Importantly, this notebook **is** the pipeline
definition — you don't press "Run all" on it like a normal notebook; you attach it to a
pipeline object and start that.

**Where in Databricks.** The notebook `notebooks/17_lab_d1_pipeline` (Workspace) is the
*definition*; you create the pipeline itself in **Jobs & Pipelines** (left sidebar; the entry
may read *Jobs & Pipelines*, *Workflows*, *Pipelines*, or *ETL*).

**Steps.**
1. Open `notebooks/17_lab_d1_pipeline` and **read** it — don't run it. Notice the `import dlt`
   line and the `@dlt.table` decorators: each decorated function defines one table in the
   pipeline. `bronze_policies` / `bronze_claims` read the raw CSVs; `silver_policies` /
   `silver_claims` cast the columns to proper types, turn bad dates into NULL and drop them,
   drop duplicates and drop the `-1` placeholder claims (the `@dlt.expect_or_drop(...)` lines
   are the quality rules); `gold_portfolio_summary` joins them into a per-tenant summary.
   Fill in any `# TODO`s to complete the table definitions (compare with
   `solutions/17_solution_d1_pipeline` if stuck).
2. In the left sidebar open **Jobs & Pipelines** and click **Create → Pipeline** (or **ETL
   pipeline**).
3. Give it a name (e.g. `keystone-pipeline`). For **source code / notebook**, select this D1
   notebook. Choose **Serverless**.
4. Set the **destination**: your **catalog** (e.g. `main`) and **schema** (e.g.
   `keystone_<you>`) — this is where the pipeline writes bronze/silver/gold.
5. Open the **Configuration** (advanced settings) and add a key/value pair:
   `keystone.raw` = `/Volumes/<your-catalog>/<your-schema>/raw` (the folder holding the CSVs
   the data generator wrote). The pipeline reads this to find the input files.
6. Click **Create**, then **Start** (top of the pipeline page).

**You should see.** A **graph (DAG)** appear and light up left to right: `bronze_policies` and
`bronze_claims`, then `silver_policies` / `silver_claims`, then `gold_portfolio_summary`.
Click any silver table to see its **data-quality** panel — it reports how many rows were
dropped (the corrupted dates, duplicates and `-1` claims). When it finishes you'll have clean
`silver_*` and `gold_portfolio_summary` tables in your schema (roughly: bronze ~30,000 →
silver ~29,500 policies, ~1,950 claims, gold ~72 summary rows).

**💡 Genie Code.** You could prompt Genie Code to scaffold a pipeline like this from a
plain-English description of the bronze/silver/gold layers, instead of writing the decorators
by hand.

### D2. Schedule the pipeline as a Job

**What this is.** A pipeline you have to press "Start" on by hand isn't production. A **Job**
runs it automatically on a schedule and can chain **dependent tasks**. You'll build a job
that runs your D1 pipeline and then, only if it succeeds, runs a second task that checks the
gold table looks healthy.

**Where in Databricks.** **Jobs & Pipelines** in the left sidebar (for building the job), plus
the notebook `notebooks/18_lab_d2_job` (Workspace) whose final cell is the check that becomes
task 2.

**Steps.**
1. First, complete the check cell in `notebooks/18_lab_d2_job`. Run its `%run` cell, then fill
   the `# TODO`: count the gold table's rows and distinct tenants and assert it isn't empty.
   Type:
   ```python
   tbl = "gold_portfolio_summary"
   if not spark.catalog.tableExists(f"{FQ}.{tbl}"):
       tbl = "3_gold_portfolio_summary"
   rows = spark.table(f"{FQ}.{tbl}").count()
   tenants = spark.sql(f"SELECT count(DISTINCT tenant) n FROM {FQ}.{tbl}").first()["n"]
   print(f"{tbl}: {rows} rows across {tenants} tenants")
   assert rows > 0 and tenants >= 1, "gold table looks empty — pipeline may not have run"
   ```
   Run it to confirm it passes (the check falls back to the `3_gold_portfolio_summary` table
   from `build_all` if your pipeline hasn't run yet).
2. In the left sidebar open **Jobs & Pipelines** → **Create → Job**.
3. **Task 1:** set **Type = Pipeline** and select your D1 pipeline from the dropdown. Give the
   task a key like `run_pipeline`.
4. **Task 2:** click **+ Add task** → **Type = Notebook**, select `18_lab_d2_job` (or the
   solution). In **Depends on**, choose Task 1 — so it only runs after the pipeline succeeds.
5. Click **Add schedule / trigger** (top-right) and set, say, a daily schedule (you can leave
   it **Paused** so it doesn't fire during the workshop).
6. **Save**, then **Run now** to test the whole chain immediately.

**You should see.** The job page shows two boxes connected by an arrow (pipeline → check).
After **Run now**, both turn green; opening the check task's output shows a line like
`gold_portfolio_summary: 72 rows across 3 tenants` and `quality check passed ✅`.
