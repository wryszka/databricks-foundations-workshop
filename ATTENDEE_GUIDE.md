# Databricks Foundations Workshop — Attendee Runbook

A full-day, hands-on introduction to Databricks for people who have **never used it
before**. You will build a small but complete data platform for a fictional company,
step by step. No prior Databricks knowledge is assumed — every click is spelled out.

> **About this workshop.** All data is synthetic and generated during the workshop. Every
> company name is fictional. Nothing here is real customer, policy, or claims data.

---

## Part 0 — Getting started (do this first)

### What Databricks is, in one paragraph

Databricks is a single web-based platform where you store data, transform it, query it,
build dashboards, apply artificial intelligence (AI), and put small applications in front
of it — without stitching together separate tools. Everything lives in your **workspace**,
which you open in a normal web browser. You don't install anything.

### The scenario you'll build

You work at **Keystone**, a (fictional) company that runs a shared data platform for
insurers. Three client insurers — **Bricksurance SE**, **Northwind Mutual**, and
**Helios Re** — are your *tenants* (your customers). Throughout the day you build the
platform underneath them: bring their data in, clean it, keep each tenant's data safely
separated from the others, analyse it, share results, and finish with a small app. Every
row of data carries a `tenant` label, which is what makes the "keep customers separated"
labs possible.

### 1. Sign in

1. Open your browser and go to the workshop URL your instructor gives you (for the free
   option, that is [Databricks Free Edition](https://www.databricks.com/learn/free-edition)).
2. Sign in. You'll land on the **workspace home page**.

### 2. A quick tour of the screen

Down the **left-hand side** is the navigation menu. The names you'll use today:

- **Workspace** — your folders and notebooks (a *notebook* is a document of runnable
  code and notes; it's where most labs happen).
- **Catalog** — the browser for all your data: catalogs → schemas → tables. Think of a
  *catalog* as a top-level container, a *schema* as a folder of tables inside it.
- **SQL Editor** — a place to write and run SQL queries (the language for asking questions
  of data).
- **Jobs & Pipelines** (sometimes called *Workflows*) — for scheduling work to run
  automatically, and for building *pipelines* that transform data.
- **Dashboards** — visual reports built from your data.
- **Genie** — ask questions of your data in plain English.
- **Compute** — the machines that run your code. Today everything uses **serverless**
  compute, which starts on demand — you don't manage any servers.

Your menu may differ slightly by version; the items above are what matters.

### 3. Bring the workshop material into your workspace (Git folder)

The labs live in a public code repository. You'll import it once:

1. In the left menu click **Workspace**.
2. Click your username / **Home** so you're in your own area.
3. Click the blue **Create** button (top-right) → **Git folder**.
4. In **Git repository URL** paste:
   `https://github.com/wryszka/databricks-foundations-workshop`
5. Leave the provider as GitHub and click **Create Git folder**.
6. A folder `databricks-foundations-workshop` appears. Open it. Inside:
   - `notebooks/` — the labs you fill in, grouped into per-track subfolders
     (`00_setup/`, `A_get_in_and_query/`, `B_bring_a_source_in/`, …); files are named `NN_lab_...`.
   - `solutions/` — the finished versions in the same per-track subfolders
     (`NN_solution_...`), if you get stuck.

### 4. Open a notebook and connect compute

1. In `notebooks/00_setup/`, click `00_config` to open it.
2. **Top-right**, find the compute selector. Click it and choose **Serverless**.
3. **Important — pick a recent environment.** Open the **Environment** panel (a small
   icon on the right edge, or via the compute selector) and select the **latest version**.
   A couple of labs use libraries that only ship with a recent environment; on an old one,
   lab I2 fails with `No module named 'mlflow'`.

### 5. How to run things

- A notebook is a stack of **cells**. Run the selected cell with **Shift+Enter**, or click
  the ▶ arrow at its top-left. Run everything with **Run all** (top of the notebook).
- Cells marked as **markdown** (text/notes) don't "run" — they just explain what's next.
- Some cells at the top of a notebook show **widgets** (little input boxes, e.g. for the
  catalog and schema names). Leave the defaults unless told otherwise.

### 6. Set up your own workspace area (run these two notebooks once)

1. **`notebooks/00_setup/00_config`** — sets the catalog and schema you'll work in. It gives you
   your **own** schema (named `keystone_<your-username>`) so your tables never clash with
   anyone else's in the room. On Free Edition the catalog defaults to `main`. Click **Run
   all**. When it finishes you'll see a line like `Using main.keystone_you`.
2. **`notebooks/00_setup/01_data_generator`** — creates all the sample data for the day (the
   insurers' policies, claims, complaint notes, documents, and files). Open it, and if you
   want every table ready up front, set the **build_all** widget to `yes`. Click **Run
   all**. It takes about a minute.

You're ready. The rest of this runbook walks you through the labs in order.

### How the labs are named

Each lab has two files with the same number, in matching per-track subfolders:

- `notebooks/<track>/NN_lab_<id>_<name>` — **the one you work in.** It has notes plus gaps
  marked `# TODO` for you to fill in.
- `solutions/<track>/NN_solution_<id>_<name>` — the complete answer. Peek if you're stuck;
  try first.

A **💡 Genie Code** tip appears where an AI assistant could write the code for you: Genie
Code is a panel in the notebook and SQL editors that turns a plain-English request into
code. It's optional — typing it yourself teaches you more.

---
## Part 1 — The tracks at a glance

The day is organised into **tracks**. Each track is a theme; each track has a few **labs**.
Work through them in order — later labs assume the tables from earlier ones. You will not
finish everything, and that's fine: there is more here than one day needs.

| Track | What it's about | Labs |
|---|---|---|
| **A. Get in and Query Data** | Find your way around, run your first queries, and meet the tools. | A1 meet the platform · A2 Databricks SQL · A3 Git folders · A4 secrets |
| **B. Bring in a Data Source** | Get data onto the platform: a one-off file, then files that keep arriving, then keeping a table in sync. | B1 file upload · B2 Auto Loader · B3 MERGE + Change Data Feed |
| **C. Govern Data across Tenants** | Keep each customer's data separate and safe, and understand how the platform tracks and protects data. | C0 Unity Catalog tour · C1 isolation · C2 row security + masking · C3 managed vs external tables · C4 time travel + history · C5 clones · C6 maintenance · C7 catalog + lineage · C8 system tables |
| **D. Transform and Schedule Data** | Turn raw data into clean, ready-to-use tables with a pipeline, and run it automatically. | D1 declarative pipeline · D2 schedule as a job |
| **E. Analyse and Apply AI** | Ask questions in plain English, build a dashboard, and use built-in AI. | E1 Genie · E2 dashboard · E3 AI functions in SQL |
| **F. Share Data** | Hand governed results to someone outside your walls, safely. | F1 Delta Sharing |
| **G. Build a Data App** | Add a fast operational database and a small app over everything you built. | G1 Lakebase · G2 a simple app |
| **H. Connect an External Database (Snowflake)** *· optional* | Connect to a client's existing Snowflake database: query it live, or copy it on a schedule. | H1 federation · H2 scheduled ingestion |
| **I. Optional Deep Dives** | Extra material for those who want more or finish early. | I1 the AI Playground / language models · I2 a simple predictive model with tracking |

**How to read the difficulty:**

- Tracks **A, B, C, D** are the solid core — everyone should get through these hands-on.
- **E, F, G** make it feel like a real product. Some steps (a shared link to a partner, an
  operational database, a deployed app) may be shown by the instructor rather than done by
  everyone, depending on the workspace — each lab says so honestly.
- **H** and **I** are optional. **H** is hands-on on Free Edition (federation to Snowflake
  is verified working there), using a shared Snowflake login the instructor provides; until
  that's set, its notebooks skip themselves safely.

Each lab below follows the same shape: **What this is → Where in Databricks → Steps → You
should see**, plus a **💡 Genie Code** tip where an AI assistant could write the code for
you, and an honest note wherever a step needs the instructor, a partner, or extra setup.

---

# Part 2 — The labs, step by step

## A. Get in and Query Data

This track is about finding your feet. You'll open your first notebook, look at the
sample data two different ways (with SQL and with Python), make a quick chart, save a
reusable query, and see that credentials and code live in proper, safe places. Nothing
here is hard — the point is to get comfortable moving around Databricks and running
things, because every later track builds on these basics.

Words we'll use: a **notebook** is a document of runnable cells; **SQL** (Structured
Query Language) is the language for asking questions of tables; a **DataFrame** is a
table held in memory while your Python code works on it; **Delta** is the table format
Databricks stores data in.

---

### A1. Meet the platform

**What this is.** Your first look at the data. You'll read the same table of insurance
policies from both SQL and Python, draw a small chart, and try the built-in AI assistant.

**Where in Databricks.** Notebook `notebooks/A_get_in_and_query/02_lab_a1_meet_platform` — open it from the
**Workspace** menu on the left (`databricks-foundations-workshop → notebooks`).

**Steps.**
1. Open the notebook. Make sure **Serverless** is selected in the compute box at the
   top-right (from Part 0). The first grey cell is a **markdown** cell — it just explains
   the lab; you don't run it.
2. Run the `%run ./00_config` cell (click into it, press **Shift+Enter**). This loads your
   catalog/schema settings so the notebook knows where your tables are. You must run this
   before anything else in every lab.
3. **Section 1 — query a Delta table.** Find the cell with `# TODO: load the table`. It
   already reads the table into a variable `df` and prints the row count. Complete it by
   adding a line to show the first ten rows. Type:
   `display(df.limit(10))`
   Then run the cell. `display(...)` renders a nicely formatted, scrollable table.
4. **Section 2 — the same data from SQL.** The next cell starts with `%sql`, which tells
   Databricks the cell is SQL, not Python. Finish the query so it returns, per tenant, the
   number of policies and the average premium. Replace the comment with real columns:
   `SELECT tenant, count(*) AS policies, round(avg(annual_premium)) AS avg_premium FROM 2_silver_policies GROUP BY tenant ORDER BY tenant`
   Run it.
5. **The same query in Python.** In the following cell, write it with a DataFrame instead
   of SQL, and show it:
   `by_tenant = spark.table("2_silver_policies").groupBy("tenant").agg(F.count("*").alias("policies"), F.round(F.avg("annual_premium")).alias("avg_premium"))`
   then `display(by_tenant)`. This shows SQL and Python are two doors to the same data.
6. **Section 3 — a quick chart.** Build a small table of average premium by age band (the
   cell hint shows the `CASE WHEN driver_age < 25 THEN '18-24' ...` pattern), then run it.
   In the result area click the **+** and choose **Visualization**, pick **Bar**, and set
   the age band as the X axis and average premium as the Y axis.
7. **Section 4 — let the AI write a query.** In a cell's toolbar click the **✨** icon
   (the Databricks Assistant) and type: *"which region has the highest average premium?"*.
   Read the SQL it suggests and run it.

**You should see.** A ten-row table of policies; a three-row per-tenant summary
(Bricksurance, Helios, Northwind) with different average premiums; the same numbers again
from Python; and a bar chart where the youngest age band clearly has the highest premium.

**💡 Genie Code.** Instead of typing the queries, open the **Genie Code** side panel and
ask it to generate a whole cell, e.g. *"average premium by region for each tenant"*.

---

### A2. Databricks SQL and the SQL warehouse

**What this is.** You'll save a reusable query as a **view**, and discover that AI is
available as an ordinary SQL function — no special setup.

**Where in Databricks.** Notebook `notebooks/A_get_in_and_query/03_lab_a2_sql_warehouse` (Workspace →
notebooks). Later steps mention the **SQL Editor** (left menu).

**Steps.**
1. Open the notebook and run the `%run ./00_config` cell.
2. **Section 1 — create a view.** A *view* is a saved query that behaves like a table. In
   the `%sql` cell, complete `CREATE OR REPLACE VIEW v_tenant_kpis` so that per tenant it
   returns: number of policies, gross written premium (the sum of `annual_premium`), number
   of claims, and claim frequency (claims ÷ policies). The hint tells you to `LEFT JOIN
   2_silver_policies` to `2_silver_claims` on `policy_id`. Run the cell — it also does a
   `SELECT * FROM v_tenant_kpis` so you see the result.
3. **Section 2 — AI as a SQL function.** In the next `%sql` cell, use `ai_classify` to
   label each complaint note as `'angry'`, `'neutral'`, or `'happy'`. Replace the comment
   with: `, ai_classify(note, ARRAY('angry','neutral','happy')) AS tone`. Run it — Databricks
   calls a language model for each row, right inside SQL.
4. **Section 3 — where this runs for real.** Read the markdown. Then, to see the "warehouse"
   idea, open the **SQL Editor** from the left menu: it's a standalone place to write SQL
   that runs on a **SQL warehouse** (a compute engine tuned for SQL). Paste
   `SELECT * FROM v_tenant_kpis` and run it there too.

**You should see.** A three-row per-tenant table with policies, premium, claims, and a
claim-frequency figure; and an eight-row list of complaint notes each tagged angry/neutral/
happy that matches the tone of the text.

**💡 Genie Code.** In the SQL Editor, ask Genie Code for *"average premium by region per
tenant"* and let it write the query.

---

### A3. Bring code in with Git folders

**What this is.** How code gets into Databricks in a professional setup: you clone a Git
repository (version-controlled code) into your workspace. It's literally how this workshop
arrived.

**Where in Databricks.** The **Workspace** menu (for the clicks) and notebook
`notebooks/A_get_in_and_query/04_lab_a3_git_folders` (for the confirmation cell). This is mostly a UI action.

**Steps.**
1. You already did this in Part 0, so here you're just confirming you understand it. In
   the left menu click **Workspace**, then your username / **Home**.
2. Click the **Create** button (top-right) → **Git folder**.
3. In **Git repository URL** you would paste a repo address, e.g.
   `https://github.com/wryszka/databricks-foundations-workshop`, leave the provider as
   **GitHub**, and click **Create Git folder**. (You've already got this folder, so you
   don't need to create it again — just note the steps.)
4. Open `notebooks/A_get_in_and_query/04_lab_a3_git_folders` and run the single code cell. It prints the path
   where the notebook lives, showing you're running from a repo-backed folder.
5. Note the tip: to use the **Git** button (pull/commit changes on a branch), a private
   repo needs a Git credential set under **Settings → Linked accounts** first.

**You should see.** A printed line like
`This notebook lives at: /Workspace/Users/you/databricks-foundations-workshop/notebooks/A_get_in_and_query/04_lab_a3_git_folders`.

**Needs the instructor.** Creating a Git folder against a *private* repo needs a linked
Git credential — your instructor will show this if relevant; the public workshop repo
needs nothing.

---

### A4. Store credentials safely with secrets

**What this is.** Real products connect to other systems using passwords/keys. You never
paste those into a notebook — you store them in a **secret scope** and read them back by
name. Here you read a pre-made secret.

**Where in Databricks.** Notebook `notebooks/A_get_in_and_query/05_lab_a4_secrets`. Creating a secret is a
one-off command in a **terminal** (your instructor may have done this already for the room).

**Steps.**
1. Open the notebook and run `%run ./00_config`.
2. **Section 1 — read how a secret is created.** The markdown shows the two commands that
   create a *scope* (a named container for secrets) and put a secret in it:
   `databricks secrets create-scope keystone_workshop` and
   `databricks secrets put-secret keystone_workshop demo_api_key --string-value "..."`.
   You don't need to run these — the scope `keystone_workshop` already exists.
3. **Section 2 — read the secret in code.** Run the cell that prints the scopes visible to
   you. Then complete the `# TODO`: read the secret and print only its **length** (never its
   value):
   `value = dbutils.secrets.get(scope=SCOPE, key=KEY)` then `print(len(value))`.
   Run it.
4. **Section 3 — why.** Read the markdown: the secret's value never appears in the notebook
   or in Git, Databricks automatically redacts any printed secret, and access is controlled.

**You should see.** A list of scope names including `keystone_workshop`, and a printed
number (the length of the secret). If you try to print the value itself, Databricks shows
`[REDACTED]`.

**Needs the instructor.** If the `keystone_workshop` scope isn't present, the instructor
(or you, in a terminal) runs the two `databricks secrets` commands from Section 1 once;
the notebook prints a friendly message rather than failing if the scope is missing.

---

## B. Bring in a Data Source

This track is about getting data *into* the platform and cleaning it up — the everyday
job of onboarding a customer's data. You'll load a deliberately messy file by hand, then
set up a folder that ingests new files automatically as they arrive, then learn the
standard way to apply a batch of changes (updates and inserts) and read back exactly what
changed.

Words we'll use: **bronze/silver/gold** are the common names for data layers — bronze is
the raw file landed as-is, silver is cleaned and typed, gold is the business-ready summary;
a **volume** is a folder for files inside the Catalog; **CSV** is Comma-Separated Values, a
plain-text table format.

---

### B1. File upload to a Delta table

**What this is.** Onboarding a new client's extract. A messy CSV has arrived; you land it
unchanged (bronze), then produce a clean, correctly typed version (silver).

**Where in Databricks.** Notebook `notebooks/B_bring_a_source_in/06_lab_b1_file_upload`. The file lives in your
**raw volume**, which you can also see under **Catalog** → your catalog → schema → Volumes.

**Steps.**
1. Open the notebook and run `%run ./00_config`.
2. Run the cell that lists your `raw` volume — you'll see `policies.csv` (and a couple of
   other files). In real life you'd put a file there via **Catalog → your volume → Upload**;
   here the data generator already placed a deliberately messy one (duplicate rows, a
   corrupted date `31/02/2025`, some negative premiums).
3. **Section 1 — Bronze (land as-is).** Complete the `# TODO`: read `raw/policies.csv` with
   `header=True` and everything as text, add two lineage columns, and save it. For example:
   `bronze = (spark.read.option("header", True).csv(f"{RAW_VOLUME}/policies.csv").withColumn("_ingest_file", F.col("_metadata.file_path")).withColumn("_ingest_ts", F.current_timestamp()))`
   then `bronze.write.mode("overwrite").saveAsTable("1_bronze_policies")`. Reading as text
   means a bad date won't crash the load. Run the cell.
4. **Section 2 — Silver (clean and type).** Complete the `# TODO` to build the clean table
   from bronze: cast the number columns to their proper types; turn the bad date into
   `NULL` safely with `try_cast(start_date AS date)`; drop duplicate `policy_id` rows with
   `.dropDuplicates(["policy_id"])`; and keep only good rows with a filter like
   `start_date IS NOT NULL AND annual_premium > 0`. Save it as `2_silver_policies`. Run it.
5. Compare the row counts printed for bronze versus silver — silver is smaller because the
   duplicates and bad rows were removed.

**You should see.** `1_bronze_policies` with a few hundred more rows than expected (the
planted duplicates), and `2_silver_policies` slightly smaller and clean — every date valid,
no negative premiums.

**💡 Genie Code.** Prompt it: *"read raw/policies.csv, drop duplicates, fix the date, drop
negative premiums, save as 2_silver_policies"* and review what it writes.

---

### B2. Auto Loader — an incremental CSV pipeline

**What this is.** Files don't arrive once — they keep coming. **Auto Loader** watches a
folder and processes **only files it hasn't seen before**. You'll load one batch, drop a
second file in, and watch only the new file get picked up.

**Where in Databricks.** Notebook `notebooks/B_bring_a_source_in/07_lab_b2_autoloader`. The watched folder is
`landing/claims/` in your landing volume.

**Steps.**
1. Open the notebook and run `%run ./00_config`.
2. Run the **reset** cell. It clears any previous run's tracking files so the lab is
   repeatable, and prints what's currently in `landing/claims/` — you should see
   `claims_batch_01.csv`.
3. **Section 1 — point Auto Loader at the folder.** Complete the `run_autoloader()`
   function's `# TODO`s. The read side uses the `cloudFiles` format (that's Auto Loader):
   `stream = (spark.readStream.format("cloudFiles").option("cloudFiles.format", "csv").option("cloudFiles.schemaLocation", SCHEMA_LOC).option("header", "true").option("cloudFiles.inferColumnTypes", "true").load(f"{LANDING_VOLUME}/claims"))`.
   The write side runs once over whatever is present and stops:
   `q = (stream.writeStream.trigger(availableNow=True).option("checkpointLocation", CHK).toTable("1_bronze_incoming_claims"))` then `q.awaitTermination()`. Run the cell; it
   prints the row count after batch 1.
4. **Section 2 — a new file lands.** Run the cell that copies `claims_batch_02.csv` from the
   `raw` volume into `landing/claims/`. It lists the folder so you can see two files now.
5. **Section 3 — run again.** Run the last code cell. It runs Auto Loader a second time and
   prints the before/after counts. Only the second file's rows are added — the first file is
   remembered and skipped.

**You should see.** A row count after batch 1, then a larger count after batch 2, with a
message like `rows 1,000 -> 2,000 (only the new file's rows were added)`.

**💡 Genie Code.** Ask it for *"an Auto Loader stream that reads CSVs from this folder into
a bronze table, processing only new files"*.

---

### B3. Upserts with MERGE (and reading the changes)

**What this is.** A source keeps changing. `MERGE` applies updates to existing rows and
inserts brand-new rows **in a single statement**. With **Change Data Feed** turned on, you
can then read exactly which rows were updated versus inserted.

**Where in Databricks.** Notebook `notebooks/B_bring_a_source_in/08_lab_b3_merge_cdf`.

**Steps.**
1. Open the notebook and run `%run ./00_config`.
2. **Section 1 — a target table with Change Data Feed on.** Complete the `# TODO`: create
   `2_silver_claims_cdf` from 800 rows of `2_silver_claims`, with Change Data Feed enabled.
   The simplest way is to create it, then run
   `ALTER TABLE 2_silver_claims_cdf SET TBLPROPERTIES (delta.enableChangeDataFeed = true)`.
   Change Data Feed makes Delta record the row-level changes so you can query them later. Run it.
3. **Section 2 — prepare a batch of changes.** Just run this cell — it's pre-written. It
   builds `claim_updates`: 100 existing claims marked `settled` with a 10% higher amount,
   plus 50 brand-new claims. This stands in for "a fresh extract from the source system".
4. **Section 3 — one MERGE.** The cell first records the table's current version number.
   Complete the `# TODO` with a `MERGE`:
   `MERGE INTO 2_silver_claims_cdf t USING claim_updates s ON t.claim_id = s.claim_id WHEN MATCHED THEN UPDATE SET status = s.status, incurred_amount = s.incurred_amount WHEN NOT MATCHED THEN INSERT *`.
   Run it — the 100 matches are updated, the 50 new ones inserted.
5. **Section 4 — read exactly what changed.** Complete the `# TODO` to query the changes
   since the version you recorded, grouped by change type:
   `display(spark.sql(f"SELECT _change_type, count(*) AS rows FROM table_changes('2_silver_claims_cdf', {start_v + 1}) GROUP BY _change_type"))`. Run it.

**You should see.** The row count grow by 50 after the MERGE, and a small summary showing
the change types — around 100 `update_postimage` (and matching pre-images) plus 50 `insert`
rows.

**💡 Genie Code.** Prompt it: *"merge these updates and new claims into 2_silver_claims_cdf
on claim_id, then show me what changed using Change Data Feed"*.

---

## C. Govern Data across Tenants

This is the heart of building a platform for many customers on shared infrastructure. You
will learn how to keep each insurer's data separate and safe, how to protect sensitive
columns, why Databricks-managed tables are the right default (and why the old "use external
tables or you'll lose your data" fear is out of date), how to travel back in time to see
what the data said before, how to make instant cheap copies for testing, how to keep tables
fast, and how to see where data came from and what it cost. Everything here uses **Unity
Catalog**, the part of Databricks that governs data (a *catalog* holds *schemas*, a schema
holds *tables*, and *grants* decide who can see what).

Before starting Track C, make sure you ran `01_data_generator` with the **build_all**
widget set to `yes` — several labs read the `2_silver_policies` table it creates.

### C0. Unity Catalog tour (start here)

**What this is.** A guided, read-and-run tour of **Unity Catalog** — the governance layer
that organises and secures everything. Unlike the other labs there are no gaps to fill: you
read each note and run the cell under it. It both *explains* and *creates* one of every kind
of object (table, view, volume, function, model) and shows how access is controlled with
grants (RBAC) and tags (ABAC). Do this before the rest of Track C so the concepts and
vocabulary are clear.

**Where in Databricks.** Notebook
`notebooks/C_govern_across_tenants/00_lab_c0_unity_catalog_tour` (Workspace → your
`databricks-foundations-workshop/notebooks` folder). Attach **Serverless** and pick a recent
**Environment** (the model step uses `mlflow`).

**Steps.**
1. Open the notebook and run the `%run ../00_setup/00_config` cell.
2. Work top to bottom: for each markdown note, run the cell beneath it. You'll see where you
   are (metastore/catalog/schema), then create a **table** (`uc_tour_regions`), a **view**,
   look at **volumes**, create a **function** (`premium_band`), register a placeholder
   **model**, **grant** a privilege and list grants (RBAC), and **tag** a column (ABAC).
3. Read the recap table at the end.

**You should see.** A row of your current metastore/catalog/schema; the new table and view;
your volumes and their files; the function used in a query; (if the environment allows) a
registered model; a grants listing; and a column tag. No errors — any step your workspace
can't do (model, tagging, granting) prints a short note and continues.

**💡 Genie Code.** Ask it things like *"list all tables and their owners in my schema"* to
explore Unity Catalog by conversation.

### C1. Tenant isolation with schemas and grants

**What this is.** The number-one question when one platform serves competing customers is
"how do I stop customer A seeing customer B's data?" The cleanest answer is to give each
tenant its own **schema** (a folder of tables) and use **grants** (permissions) to control
who can open it. You'll split the shared book into one schema per insurer and grant, inspect,
then revoke access.

**Where in Databricks.** Notebook `notebooks/C_govern_across_tenants/09_lab_c1_isolation` (open it from the
**Workspace** menu on the left, inside your `databricks-foundations-workshop/notebooks`
folder). Attach **Serverless** compute (top-right) if it isn't already.

**Steps.**
1. Open the notebook and read the top markdown cell so you understand the goal.
2. Run the second cell (`%run ./00_config`) with **Shift+Enter** — this loads your catalog,
   schema and the `TENANTS` list so the rest of the notebook knows where to work.
3. Find the first `# TODO` cell (section 1). It loops over the three tenants. Fill in the two
   lines so that for each tenant it (a) creates a schema and (b) creates a `policies` table
   holding only that tenant's rows. Type:
   ```python
   spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{tenant_schema}")
   spark.sql(f"""
       CREATE OR REPLACE TABLE {CATALOG}.{tenant_schema}.policies AS
       SELECT * FROM {FQ}.`2_silver_policies` WHERE tenant = '{t}'
   """)
   ```
   The first line makes the per-tenant folder; the second copies in only the rows where the
   `tenant` column matches. Run the cell.
4. In section 2, fill in the two `GRANT` lines. `GRANT USE SCHEMA` lets someone *open* the
   schema; `GRANT SELECT` lets them *read* the table. We grant to the built-in group
   `account users` just so the statement runs in the lab:
   ```python
   spark.sql(f"GRANT USE SCHEMA ON SCHEMA {bricks} TO `account users`")
   spark.sql(f"GRANT SELECT ON TABLE {bricks}.policies TO `account users`")
   ```
   Run it.
5. In section 3, uncomment/fill the last lines to list the grants and then remove them:
   ```python
   display(spark.sql(f"SHOW GRANTS ON SCHEMA {bricks}"))
   spark.sql(f"REVOKE SELECT ON TABLE {bricks}.policies FROM `account users`")
   spark.sql(f"REVOKE USE SCHEMA ON SCHEMA {bricks} FROM `account users`")
   ```
   Run it. (Stuck? The finished version is `solutions/C_govern_across_tenants/09_solution_c1_isolation`.)

**You should see.** Three lines like `..._t_bricksurance_se.policies -> 14,998 rows` (one per
tenant), a confirmation that the grants were applied, a small table from `SHOW GRANTS`
listing the principal `account users` with `USE SCHEMA`/`SELECT`, and finally `revoked —
back to owner-only`.

**Needs the instructor / a partner.** As the owner of these schemas *you* can always see
everything, so you can't watch yourself be blocked. To actually prove isolation, pair up with
a neighbour: grant each other access to one of your tenant schemas and confirm you can only
read the one you were granted. This is the honest limit of doing it solo.

### C2. Row-level security and column masking

**What this is.** Instead of a separate schema per tenant, you can keep **one shared table**
that everyone queries — but each caller automatically sees only their own rows, and sensitive
columns are hidden. Unity Catalog does this with a **row filter** and a **column mask**:
small SQL functions you attach to a table so the rules follow the data everywhere (SQL,
Python, dashboards, apps).

**Where in Databricks.** Notebook `notebooks/C_govern_across_tenants/10_lab_c2_rls_masking` (Workspace → your
notebooks folder), on Serverless.

**Steps.**
1. Run the `%run ../notebooks/00_config` cell (in the lab file it's `%run ./00_config`; either
   works — it just loads your settings).
2. Run the cell that creates `c2_shared_policies` — a copy of the shared table so you don't
   change the original.
3. Section 1 — create and attach the **row filter**. A row-filter function returns TRUE for
   rows the caller may see. Fill the `# TODO`:
   ```python
   spark.sql(f"""
       CREATE OR REPLACE FUNCTION {FQ}.rf_tenant(tenant_col STRING)
       RETURN is_account_group_member('account users')
              OR is_account_group_member(concat('tenant_', tenant_col))
   """)
   spark.sql(f"ALTER TABLE {FQ}.c2_shared_policies SET ROW FILTER {FQ}.rf_tenant ON (tenant)")
   ```
   `is_account_group_member(...)` checks which group the caller belongs to. Run it.
4. Section 2 — create and attach the **column mask** on `driver_age` (standing in for
   personal data): privileged callers see the real value, others see NULL.
   ```python
   spark.sql(f"""
       CREATE OR REPLACE FUNCTION {FQ}.mask_age(age INT)
       RETURN CASE WHEN is_account_group_member('account users') THEN age ELSE NULL END
   """)
   spark.sql(f"ALTER TABLE {FQ}.c2_shared_policies ALTER COLUMN driver_age SET MASK {FQ}.mask_age")
   ```
   Run it.
5. Run the final query cell (`SELECT tenant, driver_age, annual_premium ...`). The filter and
   mask apply automatically — you don't have to mention them in the query.

**You should see.** Confirmation messages that the filter and mask were applied, then a
10-row result. As the lab owner you're in `account users`, so you'll still see all tenants and
real ages — that's expected.

**Needs the instructor / a partner.** To watch the filter actually hide rows and the mask
turn ages into NULL, a second identity that is only in one `tenant_*` group must run the same
query. Pair up or watch the instructor demonstrate it.

### C3. Managed vs external tables (and why managed wins)

**What this is.** Many people arrive with an old instinct: "we must use *external* tables,
otherwise dropping a table deletes the files." On Databricks with Unity Catalog that habit is
out of date. **Managed tables are the recommended default** — the platform owns the storage
and lifecycle and gives you automatic optimisation plus safety nets. You'll prove the myth
wrong by dropping a table and getting it back.

**Where in Databricks.** Notebook `notebooks/C_govern_across_tenants/11_lab_c3_managed_vs_external` (Workspace),
Serverless.

**Steps.**
1. Run `%run` to load settings.
2. Section 1 — run the cell that creates `c3_demo` (a managed table of Helios's policies) and
   prints its type. `DESCRIBE EXTENDED ... Type` confirms it is `MANAGED`.
3. Section 2 — run `DROP TABLE {FQ}.c3_demo`. This is the "scary" step.
4. Section 3 — run `UNDROP TABLE {FQ}.c3_demo` and the row count. The count matches what it was
   before the drop: the data was never actually gone.
5. Section 4 — run the time-travel cell: it deletes some rows, then reads `VERSION AS OF 0`
   (the original version) and shows `DESCRIBE HISTORY`, the log of every change to the table.

**You should see.** `c3_demo has 5,328 rows`, then `Type = MANAGED`, then after UNDROP
`recovered c3_demo: 5,328 rows (was 5,328)`, and finally a comparison showing the current row
count is lower than version 0 — proving you can still read the earlier state.

### C4. Time travel and Slowly Changing Dimension Type 2 (SCD2) history

**What this is.** Regulated customers need to reproduce *what the data said on a given day*
and keep long-term history. **Time travel** covers the short term (read any recent version of
a whole table). A **Slowly Changing Dimension Type 2 (SCD2)** table keeps full history of
individual records by never overwriting a row — it closes the old one and adds a new one.

**Where in Databricks.** Notebook `notebooks/C_govern_across_tenants/12_lab_c4_time_travel_scd2` (Workspace),
Serverless.

**Steps.**
1. Run `%run`.
2. Section 1 (time travel) — run the cell that creates `c4_premiums`, applies a 10% rate
   increase with `UPDATE`, then compares the average premium *now* against `VERSION AS OF 0`
   (before the increase). Run the `DESCRIBE HISTORY` cell to see the versions.
3. Section 2 (SCD2) — run the cells that: create a small `c4_tenant_config` table with
   `valid_from` / `valid_to` / `is_current` columns; insert a starting row per tenant; then
   apply a change (Bricksurance upgrades from `standard` to `premium`) using a `MERGE` that
   **closes** the old row (sets `is_current = false`, stamps `valid_to`) and an `INSERT` that
   adds the new current row.
4. Run the final `SELECT * ... ORDER BY tenant, valid_from` to view the history.

**You should see.** Two average-premium numbers where "now" is ~10% higher than "version 0",
a history table listing `CREATE`/`UPDATE` operations, and a `c4_tenant_config` where
Bricksurance has **two** rows — an old `standard` row with `is_current = false` and a new
`premium` row with `is_current = true`.

### C5. Zero-copy clones for dev and test

**What this is.** You constantly need safe copies of real data to experiment on. Delta
`CLONE` gives two kinds: a **shallow** clone (points at the same underlying files — almost
instant and cheap, ideal for a throwaway test) and a **deep** clone (a fully independent
copy). Editing a clone never touches the original.

**Where in Databricks.** Notebook `notebooks/C_govern_across_tenants/13_lab_c5_clones` (Workspace), Serverless.

**Steps.**
1. Run `%run`.
2. Run the **deep clone** cell: `CREATE OR REPLACE TABLE {FQ}.c5_deep DEEP CLONE {FQ}.`2_silver_policies``
   and its row count.
3. Run the **shallow clone** cell (it's wrapped in a `try` so it won't crash if this workspace
   restricts shallow clones on managed tables — it'll just say so).
4. Run the "change a clone" cell: it deletes all Helios rows from the clone, then prints the
   source count and the clone count to show the **source is unchanged**.

**You should see.** A deep-clone row count matching the source (~29,500), a shallow-clone
count (or a friendly "not available here" message), and a final line like
`source=29,539, clone=24,211 (source unchanged)`.

### C6. Keeping tables fast and tidy

**What this is.** A quick tour of table upkeep: `OPTIMIZE` (compact many small files into
fewer big ones), **liquid clustering** (organise a table by the columns you filter on), and
`VACUUM` (remove files no longer referenced). The good news: managed tables do most of this
automatically — here you see the manual levers so you understand what's happening.

**Where in Databricks.** Notebook `notebooks/C_govern_across_tenants/14_lab_c6_maintenance` (Workspace), Serverless.

**Steps.**
1. Run `%run`, then the cell that creates the working table `c6_demo`.
2. Run `ALTER TABLE {FQ}.c6_demo CLUSTER BY (tenant, region)` — tells Databricks to organise
   the data by the columns you'll most often filter on.
3. Run `OPTIMIZE {FQ}.c6_demo` — compacts small files.
4. Run `VACUUM {FQ}.c6_demo DRY RUN` — a **dry run** only *lists* what would be removed
   (nothing is deleted), which is safe in a workshop.

**You should see.** A confirmation of the clustering, an `OPTIMIZE` result row (files added
/ removed), and a `VACUUM ... DRY RUN` list of files that *would* be cleaned up beyond the
default 7-day retention window.

### C7. Catalog Explorer and data lineage

**What this is.** How to find data and understand where it came from without reading anyone's
code. **Catalog Explorer** is the point-and-click browser for your data; **lineage** shows,
as a graph, how tables flow into one another.

**Where in Databricks.** First the **Catalog** browser (left sidebar), then notebook
`notebooks/C_govern_across_tenants/15_lab_c7_catalog_lineage` (Workspace), Serverless.

**Steps.**
1. In the left sidebar click **Catalog**. Expand your catalog (e.g. `main`) → your schema
   (`keystone_<you>`). Click the table `2_silver_policies`.
2. Look at the tabs across the top of that panel — **Overview**, **Sample Data**,
   **Details**, **Permissions**, **Lineage**. Click **Lineage** to see a graph of upstream and
   downstream tables/columns. (If it's empty, lineage can take a few minutes to appear, or may
   be limited on this workspace — see the note below.)
3. Now open the notebook and run `%run`.
4. Run the first query cell — it lists your tables from `information_schema.tables` (a
   standard, always-available catalog of metadata).
5. Run the second query cell — it lists the columns of `2_silver_policies` from
   `information_schema.columns`.
6. Run the lineage cell — it queries `system.access.table_lineage`. It's wrapped in a `try`,
   so if that system table isn't enabled here it prints a friendly message instead of failing.

**You should see.** In the UI, a lineage graph (or an empty one). In the notebook, a table of
your table names and types, a list of columns with data types, and either lineage rows or a
"not available/enabled here" message.

**Needs the instructor / live infra.** The lineage **graph** and `system.access.table_lineage`
depend on the workspace tier and can take minutes to populate; on Free Edition they may be
empty. The `information_schema` queries always work.

### C8. System tables: access, lineage, cost

**What this is.** The platform records its own operations as queryable tables under the
`system` catalog — the answer to "who queried this?", "where did it come from?", and "what is
this costing?" This is how builders answer the cost and audit questions.

**Where in Databricks.** Notebook `notebooks/C_govern_across_tenants/16_lab_c8_system_tables` (Workspace), Serverless.

**Steps.**
1. Run `%run`, then run the cell that defines a small `probe(label, sql)` helper — it runs a
   query and, if the table isn't available, prints `[N/A]` instead of crashing.
2. Run the "system schemas" cell to list which `system.*` schemas exist for you.
3. Run the **audit** cell — recent activity (who did what), from `system.access.audit`.
4. Run the **cost** cell — usage in Databricks Units (DBUs) over the last 7 days, from
   `system.billing.usage`.

**You should see.** For each probe, either `[OK] ... N rows` with a result table, or `[N/A]
...` — which is itself the lesson: which of these are populated depends on your workspace.

**Needs the instructor / live infra.** `system.billing.usage` (cost) is typically **empty or
unavailable on Free Edition** because there's no billing account behind it; `system.access.*`
may also be limited. Note which probes returned `[OK]` on your workspace.

---

## D. Transform and Schedule Data

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

**Where in Databricks.** The notebook `notebooks/D_transform_and_schedule/17_lab_d1_pipeline` (Workspace) is the
*definition*; you create the pipeline itself in **Jobs & Pipelines** (left sidebar; the entry
may read *Jobs & Pipelines*, *Workflows*, *Pipelines*, or *ETL*).

**Steps.**
1. Open `notebooks/D_transform_and_schedule/17_lab_d1_pipeline` and **read** it — don't run it. Notice the `import dlt`
   line and the `@dlt.table` decorators: each decorated function defines one table in the
   pipeline. `bronze_policies` / `bronze_claims` read the raw CSVs; `silver_policies` /
   `silver_claims` cast the columns to proper types, turn bad dates into NULL and drop them,
   drop duplicates and drop the `-1` placeholder claims (the `@dlt.expect_or_drop(...)` lines
   are the quality rules); `gold_portfolio_summary` joins them into a per-tenant summary.
   Fill in any `# TODO`s to complete the table definitions (compare with
   `solutions/D_transform_and_schedule/17_solution_d1_pipeline` if stuck).
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
the notebook `notebooks/D_transform_and_schedule/18_lab_d2_job` (Workspace) whose final cell is the check that becomes
task 2.

**Steps.**
1. First, complete the check cell in `notebooks/D_transform_and_schedule/18_lab_d2_job`. Run its `%run` cell, then fill
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

---

## E. Analyse and Apply AI

So far you have moved and governed data. This track is about **getting answers out of it**.
You'll let people ask questions in plain English (Genie), turn one of those questions into
a shareable dashboard, and call artificial-intelligence (AI) models straight from SQL — the
"make it useful" layer that sits on top of a data product. Everything here reads the
finished `3_gold_*` and `2_silver_*` tables you created earlier, so make sure you ran
`01_data_generator` (ideally with the **build_all** widget set to `yes`).

### E1. Ask questions in plain language with Genie

**What this is.** **Genie** is a feature that lets someone ask a question about your data in
ordinary English — "which tenant has the highest claim frequency?" — and it writes and runs
the SQL (Structured Query Language, the language for querying data) for you. It is the
"let a business user ask" surface of a data product. (Its sibling, **Genie Code**, is a
different tool for *building* — it writes notebook and SQL code from a prompt. Same
workspace, different job.)

**Where in Databricks.** Mostly the **Genie** area (left sidebar). There is also a companion
notebook, `notebooks/E_analytics_and_ai/19_lab_e1_genie` (open it from the **Workspace** menu), whose optional
last cell asks Genie from code.

**Steps.**
1. In the **left sidebar**, click **Genie**. (If you don't see it, it may sit under a
   heading like *SQL* or *AI/BI* — look for the word "Genie".)
2. Click **New** (top-right) to start a new **Genie space** (a Genie space is a saved
   question-answering assistant scoped to a chosen set of tables).
3. When asked which data to include, browse to **your own schema** — it is named
   `keystone_<your-username>` inside your catalog (`main` on Free Edition) — and tick these
   tables: `3_gold_portfolio_summary`, `3_gold_loss_ratio_monthly`, `2_silver_policies`,
   `2_silver_claims`. Confirm your selection.
4. Give the space a name, for example *Keystone — Portfolio*, and click **Create**.
5. You'll land in a chat box. In the **sample questions** area (or just the chat), add and
   then ask questions such as:
   - "Which tenant has the highest claim frequency?"
   - "Show gross written premium by region for bricksurance_se."
   - "What is the monthly incurred trend this year?"
6. Ask one. Genie replies with a table or chart. Now click **Show generated code** (or the
   **SQL** toggle on the answer) to reveal the SQL Genie wrote. **Copy that SQL and keep it
   in a scratch note — you reuse it in lab E2.**
7. *(Optional, for the curious.)* Open `notebooks/E_analytics_and_ai/19_lab_e1_genie`. Copy your space's id
   from its web address — the part after `.../genie/rooms/` — and paste it into the
   **space_id** widget at the top of the notebook. Then run the last code cell to ask Genie
   the same question from Python and print both the answer and the SQL.

**You should see.** Genie answering your question with a result table/chart, and — when you
click **Show generated code** — the SQL it generated (a `SELECT ... FROM
3_gold_portfolio_summary ...`).

**💡 Genie Code.** Genie (this lab) *answers* questions; **Genie Code** *writes code*. If
you'd rather build a query in a notebook, open the Genie Code panel there and describe what
you want.

**On Free Edition.** ✅ Verified — Genie works on Free; a space was created over these exact
tables. Creating a space is normally a click-through in the user interface, so you do it
yourself (there's nothing to run headless).

### E2. Build a dashboard from Genie's SQL

**What this is.** You take the SQL Genie generated in E1 (or the ready-made queries below)
and build a proper **AI/BI dashboard** — a saved, shareable report with a headline number,
a bar chart, and a trend line. This is how a one-off question becomes something a team can
open every morning.

**Where in Databricks.** The **Dashboards** area (left sidebar) for building the report; the
companion notebook `notebooks/E_analytics_and_ai/20_lab_e2_dashboard` (open from **Workspace**) to check the
numbers first.

**Steps.**
1. First, sanity-check the numbers. Open `notebooks/E_analytics_and_ai/20_lab_e2_dashboard` and attach
   **Serverless** compute (top-right), as in Part 0.
2. The first `%sql` cell (the **KPI**, or key-performance-indicator, tile) is given — run it.
   It totals gross written premium (the sum of annual premiums) and the overall claim
   frequency across all tenants.
3. Fill the two `# TODO` cells:
   - **Bar tile** — replace the placeholder query with:
     `SELECT tenant, round(sum(gwp)) AS gwp, sum(claims) AS claims FROM 3_gold_portfolio_summary GROUP BY tenant ORDER BY gwp DESC;`
     This gives premium and claim counts per tenant (per customer insurer).
   - **Line tile** — replace the placeholder with:
     `SELECT tenant, month, round(sum(incurred)) AS incurred FROM 3_gold_loss_ratio_monthly GROUP BY tenant, month ORDER BY month;`
     This is the monthly claims-cost trend per tenant.
   Run both and confirm they return rows.
4. Now build the dashboard. In the **left sidebar** click **Dashboards**, then
   **Create dashboard** (top-right).
5. Click the **Data** tab. Click **Create from SQL** / **Add a dataset**, and paste the KPI
   query from step 2. Give the dataset a name. Repeat, adding a second dataset with the bar
   query and a third with the line query. (These three queries are exactly the kind of SQL
   Genie produces — in E1 you can paste your own copied from **Show generated code**.)
6. Click the **Canvas** tab. Use **Add a widget** (or drag from the toolbar) to place:
   - a **Counter** widget bound to the KPI dataset (shows total gross written premium),
   - a **Bar** widget bound to the by-tenant dataset (tenant on one axis, premium on the
     other),
   - a **Line** widget bound to the monthly dataset (month across the bottom, incurred up
     the side, one line per tenant).
7. Click **Publish** (top-right) so the dashboard is saved and shareable.

**You should see.** A published dashboard with three panels: a big number (around
€12–13 million total gross written premium), a bar chart comparing the three tenants, and a
line chart of monthly claims cost.

**💡 Genie Code.** You can prompt Genie Code to generate a starter dashboard definition and
then tweak it, instead of adding each tile by hand.

**On Free Edition.** ✅ The tile SQL is verified on Free; building and publishing the
dashboard object is a user-interface action, so you do that part yourself.

### E3. AI functions in SQL

**What this is.** Real artificial intelligence is a **single SQL function call** on this
platform — there is no model to deploy and no Python needed. You'll classify claims, score
the sentiment (tone) of complaint notes, hide personal data, and extract and summarise claim
documents, all in SQL, right where a data pipeline would.

**Where in Databricks.** The notebook `notebooks/E_analytics_and_ai/21_lab_e3_ai_functions` (open it from the
**Workspace** menu).

**Steps.**
1. Open `notebooks/E_analytics_and_ai/21_lab_e3_ai_functions` and attach **Serverless** compute.
2. **Section 1 — sentiment.** Find the first `%sql` cell. Replace the `note AS
   todo_replace_me` line with `ai_analyze_sentiment(note) AS sentiment`. Run it. This reads
   the free-text complaint notes in `2_silver_complaints` and labels each as positive,
   negative, neutral, or mixed — the tone is genuinely in the wording, so the labels make
   sense.
3. **Section 2 — classify severity.** In the next `%sql` cell, add a `severity` column using
   `ai_classify`, which picks the best-fitting label from a list you supply. Use:
   ```
   ai_classify(
     concat('A ', claim_type, ' motor claim with incurred amount EUR ',
            cast(incurred_amount AS string), ' and status ', status),
     array('minor', 'moderate', 'severe')
   ) AS severity
   ```
   The `concat(...)` builds a short sentence from the structured columns; `ai_classify` reads
   it and returns minor / moderate / severe. Run it.
4. **Section 3 — mask personal data.** In the next `%sql` cell add
   `ai_mask(note, array('person', 'email', 'phone number')) AS masked_note`. Run it: the
   model redacts the named kinds of personal information from each note.
5. **Section 4 — read documents, then extract and summarise.** Run the given Python cell
   first — it reads the text documents from your `docs` volume (the folder of claim
   documents the generator created) into a temporary view called `claim_docs` and prints how
   many it loaded. Then, in the following `%sql` cell, add these two columns:
   ```
   ai_extract(value, array('claim reference', 'policy reference', 'date of loss',
                           'claim type', 'reserve estimate')) AS extracted,
   ai_summarize(value, 40) AS summary
   ```
   `ai_extract` pulls the named fields out of each document; `ai_summarize` writes a short
   (~40-word) summary. Run it.

**You should see.** Four result tables, each with a new AI-generated column: a `sentiment`
label per note; a `severity` label per claim; a `masked_note` with personal details
redacted; and, for each document, an `extracted` set of fields plus a short `summary`.

**💡 Genie Code.** Instead of typing these, you could prompt Genie Code — for example
"score the sentiment of every complaint note and count negatives by tenant" — and it will
write the SQL for you.

---

## F. Share Data

A data platform is only useful if the results can leave your walls safely. Track F is
about **Delta Sharing**: an open way to hand a live table to someone in a *different*
Databricks workspace or organisation — a client insurer, an auditor, a reinsurer —
**without copying any files** and **without giving them a login to your workspace**. They
always see the current data, and you can scope exactly what they get (even down to a single
tenant's rows). This is how Keystone would deliver each insurer *their* results and no one
else's.

### F1. Delta Sharing, attendee to attendee

**What this is.** You will publish one tenant's results table as a read-only "share", grant
it to a recipient, and then — paired with the person next to you — actually query each
other's shared data. It shows how governed results move between organisations with no file
copying.

**Where in Databricks.** Notebook `notebooks/F_share/22_lab_f1_delta_sharing` (open it from the
**Workspace** menu on the left). You will run its cells; the person you pair with runs a
couple of SQL statements in **their** workspace's **SQL Editor**.

**Steps.**
1. In the **Workspace** file browser on the left, open your `databricks-foundations-workshop`
   Git folder, then `notebooks/`, and click `22_lab_f1_delta_sharing` to open it. Make sure
   **Serverless** compute is selected in the top-right (as in Part 0).
2. **Pair up with a neighbour now.** One of you will publish first while the other adds it;
   then swap. You each need the other's *sharing identifier* (you'll fetch it in step 6).
3. Run the first code cell (**Shift+Enter**). It is `%run ./00_config` — it loads your
   catalog, schema and the `TENANTS` list so the notebook knows where your data is. Wait for
   it to finish (a small green tick appears).
4. Run the **"0. Make sure there is something to share"** cell. It checks that the table
   `3_gold_portfolio_summary` exists. If it errors, go back and run `01_data_generator` with
   the **build_all** widget set to `yes`, then return here.
   - *You should see:* `shareable table ready`.
5. Fill in **TODO 1 and TODO 2** in the *"1. Create a share and add ONE tenant's slice"*
   cell. A **share** is a named, read-only bundle of tables you offer to others. Type:
   ```python
   spark.sql(f"CREATE SHARE IF NOT EXISTS {SHARE} COMMENT 'Keystone gold portfolio share'")
   spark.sql(f"ALTER SHARE {SHARE} ADD TABLE {FQ}.`3_gold_portfolio_summary` "
             f"PARTITION (tenant = '{SHARE_TENANT}') AS keystone.portfolio_{SHARE_TENANT}")
   ```
   The `PARTITION (tenant = ...)` line is the important bit: it adds **only one tenant's
   rows**, so the recipient can never see the other insurers. Run the cell.
   - *If you get a `PERMISSION_DENIED` message*, creating shares needs a metastore-admin
     privilege you may not have — that's expected on a locked-down or Free Edition workspace.
     Read the "Needs…" note below and watch the instructor instead; the rest still teaches.
6. **Get your partner's sharing identifier.** Your partner runs, in *their* notebook or SQL
   Editor, `SELECT current_metastore()` and reads you the value. At the top of your notebook
   find the **partner_sharing_id** widget (a small text box) and paste their value in. (Leave
   it blank if you want "open sharing", which instead produces an activation link you can
   send to anyone.)
7. Fill in **TODO 3 and TODO 4** in the *"2. Create a recipient and grant the share"* cell.
   A **recipient** is who you're sharing with. Type:
   ```python
   spark.sql(f"CREATE RECIPIENT IF NOT EXISTS {RECIPIENT} USING ID '{partner}'")   # if partner set
   spark.sql(f"GRANT SELECT ON SHARE {SHARE} TO RECIPIENT {RECIPIENT}")
   ```
   (If `partner` is blank, create the recipient without `USING ID '...'` — that's the
   open-sharing path.) Run the cell.
8. Fill in **TODO 5** in the *"3. Inspect what you published"* cell and run it:
   ```python
   display(spark.sql(f"SHOW SHARES LIKE '{SHARE}'"))
   display(spark.sql(f"SHOW ALL IN SHARE {SHARE}"))
   display(spark.sql(f"DESCRIBE RECIPIENT {RECIPIENT}"))
   ```
   For open sharing, the activation link appears in the `DESCRIBE RECIPIENT` output — hand
   that to your partner.
9. **The partner side.** Now your partner mounts *your* share in their own **SQL Editor**
   (left menu → **SQL Editor**) and queries it — no copy, always live:
   ```sql
   CREATE CATALOG IF NOT EXISTS from_keystone USING SHARE <your_provider_name>.<share_name>;
   SELECT * FROM from_keystone.keystone.portfolio_bricksurance_se;
   ```
10. **Swap roles** and repeat so you each publish and each query the other's share.

**You should see.** `SHOW ALL IN SHARE` lists your one shared table, and your partner's
`SELECT` returns rows for a single tenant only (never the others) — proving the share is
live and correctly scoped.

**💡 Genie Code.** In the notebook's Genie Code panel you could type "create a Delta share
called keystone_share and add only the bricksurance_se rows of 3_gold_portfolio_summary"
and let it draft the `CREATE SHARE` / `ALTER SHARE` statements for you.

**On Free Edition.** Partially. ✅ You *can* **author the share** — create it and add a
tenant's table (the notebook self-grants the `USE CATALOG` / `USE SCHEMA` you need). ❌ You
**cannot create an external recipient**: Free reports *"External Delta Sharing is not enabled
on the metastore"* and Free has no account console to enable it. So the actual hand-off to a
partner is shown on a full workspace (where an admin has enabled External Delta Sharing) and
needs a second person to mount the share. On Free, treat F1 as "author the share" + watch the
recipient hand-off.

---

## G. Build a Data App

The tables you built all day are perfect for reporting, but a real *product* needs a fast
database behind a user interface and a screen people can actually click. Track G adds the
last two pieces: **Lakebase** (a managed Postgres operational database inside Databricks,
for quick row-at-a-time lookups) and a small **Databricks App** that ties everything
together — ask a question in plain English (via Genie) and look up the portfolio table.
These are the most infrastructure-heavy labs of the day, so parts are watched rather than
built solo.

### G1. An operational database with instant branching (Lakebase)

**What this is.** You'll reach Lakebase (managed Postgres), see how a lakehouse table is
kept in sync into it for an app to read, and learn how to **branch** the whole database —
make a near-instant, throwaway copy for a what-if. Actually creating infrastructure is
switched off by default so the notebook is safe to run.

**Where in Databricks.** Notebook `notebooks/G_app/23_lab_g1_lakebase` (open from the **Workspace**
menu on the left). Real provisioning is also visible later under **Compute → Database
instances** (or **Lakebase**) in the left menu.

**Steps.**
1. Open `notebooks/G_app/23_lab_g1_lakebase` from the **Workspace** browser and confirm
   **Serverless** compute is selected (top-right).
2. Run the first cell — `%run ./00_config` — to load your catalog and schema.
3. Run the next cell (the one importing `requests` and defining `api(...)`). It sets up a
   small helper that talks to the Databricks **Database API** using your notebook's own
   credentials — nothing to configure.
4. Fill in **TODO 1** in the *"1. List existing Lakebase instances"* cell and run it. This
   just asks the platform what database instances already exist, which proves the API is
   reachable:
   ```python
   code, out = api("GET", "/api/2.0/database/instances")
   print("status", code)
   for inst in out.get("database_instances", []):
       print(f"  {inst['name']:40} {inst.get('state'):12} {inst.get('capacity')}")
   ```
   - *You should see:* `status 200` and a line per existing instance (there may be none —
     that's fine; a `200` means it works).
5. Look at the top of the notebook for the **provision** widget (a dropdown, default `no`).
   Leave it on **no** for now — that keeps the create-infrastructure steps in "dry run" so
   nothing costly is built.
6. Run the *"2. Create an instance (guarded)"* cell. With `provision=no` it just **prints
   the request it would send** (creating an instance named after your schema, smallest
   `CU_1` capacity). Read it so you understand what a real create looks like.
7. Run the *"3. Sync a gold table into Postgres (guarded)"* cell. Again with `provision=no`
   it shows the call (and the equivalent `databricks database create-synced-database-table`
   command). A **synced table** keeps a Postgres copy of `3_gold_portfolio_summary` current,
   so an app can read Postgres while the lakehouse stays the source of truth.
8. Read the *"4. Instant branching"* and *"5. Connect from code"* markdown. Branching makes
   a **child instance** from a parent at a point in time — copy-on-write, so it's seconds,
   not a full copy — ideal for a disposable what-if or test.
9. **(Optional, instructor-led.)** If your instructor says Lakebase is available and there's
   time, set the **provision** widget to **yes** and re-run steps 6–7 to actually create an
   instance and a synced table (this takes a few minutes), then delete it afterwards with
   `databricks database delete-database-instance <instance>`.

**You should see.** A `200` from the instances call, and — with `provision=no` — clear
printouts of exactly what the real create/sync calls would send, so you understand the
shape without building anything.

**💡 Genie Code.** You could ask Genie Code to "write a Python call to the Databricks
database API that lists all database instances" instead of typing TODO 1 yourself.

**On Free Edition.** ✅ Verified — a Lakebase instance was provisioned and reached
**AVAILABLE** on Free (Free allows **one** Lakebase project). The `provision=yes` path builds
real infrastructure and takes a few minutes; leave it `no` if you just want the walkthrough.

### G2. A simple app powered by Genie + Lakebase

**What this is.** You'll stand up a tiny web application — a Databricks **App** — that has
one page where you can ask a plain-English question (answered by Genie) and see the
portfolio table. It's the moment the whole day becomes a "product" you can click. The app's
code is already written for you in the `app/` folder; this lab is about pointing it at your
data and deploying it.

**Where in Databricks.** Notebook `notebooks/G_app/24_lab_g2_app` (from the **Workspace** menu),
the `app/` folder in your Git folder (its files: `app.py`, `app.yaml`, `requirements.txt`,
`README.md`), and later the **Compute → Apps** area (left menu) where deployed apps appear.

**Steps.**
1. Open `notebooks/G_app/24_lab_g2_app` from the **Workspace** browser; confirm **Serverless** is
   selected. Run the first cell (`%run ./00_config`).
2. Fill in **TODO 1** in the *"1. Confirm the app's data source"* cell and run it. This
   proves the table the app will read actually exists and has data:
   ```python
   assert spark.catalog.tableExists(f"{FQ}.3_gold_portfolio_summary"), "run the generator first"
   display(spark.sql(f"SELECT * FROM {FQ}.`3_gold_portfolio_summary` ORDER BY gwp DESC LIMIT 10"))
   ```
   - *You should see:* the top 10 portfolio rows by GWP (gross written premium). This is
     exactly what the app's `/api/portfolio` page will return.
3. In the **Workspace** browser, open the `app/` folder and click `app.yaml` to view it.
   This file sets the app's configuration. Fill in the values for your workspace:
   - `KEYSTONE_CATALOG` and `KEYSTONE_SCHEMA` — where your `3_gold_portfolio_summary` lives
     (your catalog, e.g. `main`, and your `keystone_<you>` schema).
   - `DATABRICKS_WAREHOUSE_ID` — the identifier of a SQL warehouse the app can query with
     (ask your instructor, or find it under **SQL Warehouses** in the left menu).
   - `GENIE_SPACE_ID` — the identifier of the Genie space you created in lab **E1** (open
     that space and copy the id from its URL).
   - `LAKEBASE_*` — leave **blank** unless you finished G1's optional provisioning; blank
     means the app reads the portfolio via the SQL warehouse instead, which is fine.
4. Read the app's `README.md` (in the same folder). It explains the two pages: `/api/ask`
   (sends your question to Genie) and `/api/portfolio` (the lookup table).
5. **Deploy the app.** This uses the command line (your instructor will show where — the
   web terminal or a local machine). The steps, from the notebook's *"3. Deploy"* cell:
   ```
   databricks apps create keystone-mini-app
   databricks sync ./app /Workspace/Users/<you>/keystone-mini-app
   databricks apps deploy keystone-mini-app --source-code-path /Workspace/Users/<you>/keystone-mini-app
   ```
6. **Grant the app permission** to reach its data. Every app runs as its own *service
   principal* (a non-human identity). Give that principal: `CAN USE` on the SQL warehouse,
   `CAN RUN` on the Genie space, and read access on your catalog/schema (and the Lakebase
   instance if you used it). Your instructor will point to the **Permissions** dialog for
   each.
7. Open the app's URL (shown after deploy, or under **Compute → Apps**), type a question
   like "which tenant has the highest premium?", and click the portfolio page.

**You should see.** A running web page: your typed question comes back with a Genie answer,
and the portfolio page lists the same rows you saw in step 2.

**💡 Genie Code.** Genie Code can help you edit or extend `app.py` — e.g. "add a second API
endpoint that returns total premium per tenant" — generating the FastAPI route for you.

**On Free Edition.** ✅ Verified — the app **deployed and is RUNNING** on Free (Free allows
**up to three** apps; each runs ~24h after start, then you restart it). You need the
Databricks command-line tool, a **Genie space id** from lab E1, and a SQL warehouse.

---

## H. Connect an External Database (Snowflake) · *Optional*

Not every client will move their data to you. This optional track connects Keystone to a
client's existing **Snowflake** database (another cloud data warehouse) two ways: query it
**live without copying** (federation), and **copy it on a schedule**. You then compare the
trade-offs. This track only works once a Snowflake account exists and the widgets are
pointed at it — until then the notebooks skip themselves cleanly, so they're safe to open
and read.

**This has been verified working on Databricks Free Edition** — Lakehouse Federation to
Snowflake runs fine there. Your instructor provides one shared, read-only Snowflake login
(account URL + user + password); you store the password in a secret (exactly like lab
**A4**) and everyone points at the same Snowflake account. Two Free-Edition notes are
already handled in the notebooks: Materialized Views aren't enabled on Free serverless
(the cache step falls back to a plain table automatically), and `remote_query` needs an
explicit `database`. *(If your Free account has no outbound internet access, "Verify with
LinkedIn" in account settings unlocks it.)*

### H1. Query Snowflake in place (Lakehouse Federation)

**What this is.** Register a Snowflake database inside Databricks as a *foreign catalog* and
query it directly — the query runs on Snowflake and the results come back to you, with no
copy. You'll also cache it with a Materialized View and push a native query with
`remote_query`.

**Where in Databricks.** Notebook `notebooks/H_external_snowflake/27_lab_h1_snowflake_federation` (open it from
the **Workspace** menu), plus a one-time secret set from a terminal.

**Steps.**
1. **Store the Snowflake password as a secret** (so it's never written in a notebook). Open
   a terminal with the Databricks CLI and run:
   `databricks secrets create-scope keystone_workshop` (skip if it already exists), then
   `databricks secrets put-secret keystone_workshop snowflake_password` and paste the
   password when prompted.
2. Open the notebook. At the top, fill the **widgets**: `sf_host`
   (`<account>.snowflakecomputing.com`), `sf_user`, `sf_warehouse`, `sf_database`,
   `sf_schema`, `sf_table`. Leave `secret_scope`/`secret_key` as-is if you used the names above.
3. Set the **snowflake_configured** widget to `yes`. (If it's `no`, the notebook prints a
   message and stops — that's the safe default.)
4. Run the cell that creates the **connection** (`CREATE CONNECTION ... TYPE snowflake`) —
   fill the `# TODO` using the hint (the password uses `secret('scope','key')`).
5. Run the cell that creates the **foreign catalog** (`CREATE FOREIGN CATALOG ... USING
   CONNECTION ...`). Open the **Catalog** browser on the left — the Snowflake database now
   appears there like any other.
6. Run the **live query** cell (a `SELECT ... LIMIT 20` and a `count(*)`).
7. Run the **Materialized View** cell to cache the data locally in your schema.
8. Run the **`remote_query`** cell to push a native count straight to Snowflake.

**You should see.** Snowflake rows displayed in Databricks, a cached-row count from the
Materialized View, and a count returned by `remote_query` — all without importing a file.

**💡 Genie Code.** Ask it to "create a Snowflake connection and foreign catalog, then query
table X" and it drafts the SQL.

**Needs the instructor.** The shared **Snowflake login** (account URL + user + password) —
your instructor provides it. Everything else you run yourself on Free Edition.

### H2. Copy vs federate — scheduled ingestion

**What this is.** Instead of querying Snowflake live, **copy** the table into a managed
Databricks table, refresh it incrementally with `MERGE`, and schedule it — then compare
copy vs federate.

**Where in Databricks.** Notebook `notebooks/H_external_snowflake/28_lab_h2_scheduled_ingest`, then **Jobs &
Pipelines** to schedule it.

**Steps.**
1. Make sure **H1 has run** (this lab uses the foreign catalog H1 created). Open the
   notebook, set `snowflake_configured` to `yes`, and check `sf_schema`/`sf_table` and the
   `key_column` (the primary key used to match rows, e.g. `policy_id`).
2. Run the **first-load** cell (`CREATE OR REPLACE TABLE ... AS SELECT * FROM` the foreign
   table) — this materialises a local copy `4_ingested_snowflake`.
3. Run the **MERGE** cell — on repeat runs this updates changed rows and inserts new ones,
   rather than reloading everything.
4. **Schedule it:** left menu **Jobs & Pipelines → Create → Job**, add a task pointing at
   this notebook, set a schedule (e.g. hourly), and save — exactly like lab D2.
5. Read the **copy-vs-federate** table at the bottom.

**You should see.** A local table `4_ingested_snowflake` with the Snowflake row count,
unchanged after a second `MERGE` (no duplicates), and a job you could leave running.

**💡 Genie Code.** Ask it to "MERGE the latest rows from the foreign table into
`4_ingested_snowflake` on the key column."

**Needs the instructor.** The same shared Snowflake login as H1 (and H1 run first). Note:
Databricks' fully-managed *Lakeflow Connect* connectors (SQL Server, Salesforce,
ServiceNow, …) don't include Snowflake today, so this lab ingests through the H1 federation
connection. Verified working on Free Edition.

---

## I. Optional Deep Dives

Two extra labs for anyone who is curious or finishes early. Neither is required to complete
the workshop. The first shows you that large language models (the technology behind chat
assistants) live right inside the platform; the second is a taster of machine learning —
training a small predictive model and tracking it properly.

### I1. LLM primer — the AI Playground and foundation models

**What this is.** A short, no-pressure tour of the fact that **large language models (LLMs)
are built into the platform** — nothing to install, no key to manage. You'll chat with a
model in the AI Playground, then call the same model from SQL. ("Foundation models" is
Databricks' name for the ready-to-use LLMs it hosts.)

**Where in Databricks.** The **AI Playground** (left sidebar, usually under **Machine
Learning → Playground**) for chatting; the notebook `notebooks/I_optional_deep_dives/25_lab_i1_llm_playground`
(open from **Workspace**) for calling a model from code.

**Steps.**
1. In the **left sidebar**, open **Machine Learning → Playground** (the **AI Playground**).
2. At the **top of the Playground** there is a **model dropdown**. Open it — this is the
   list of models *your* workspace can use. **Note what's there**, because the list varies
   (see the warning below). Pick one, type a prompt like *"In two sentences, explain what a
   no-claims discount is,"* and read the reply. This is a safe place to try prompts before
   putting them into SQL or code.
3. Now call a model from code. Open `notebooks/I_optional_deep_dives/25_lab_i1_llm_playground` and attach
   **Serverless** compute.
4. Look at the `LLM_ENDPOINT` line near the top. It is set to `databricks-gpt-oss-120b`, an
   open-weight model that is commonly available. **If that name was *not* in your Playground
   dropdown, change `LLM_ENDPOINT` to one that was.**
5. Fill the `# TODO` in the first `ai_query` cell — put a prompt string where the empty
   quotes are, for example:
   `'You are helping an insurer. In two sentences, explain what a no-claims discount is.'`
   `ai_query(endpoint, prompt)` sends your prompt to the model and returns its answer. Run
   the cell and read the printed answer.
6. Run the next cell (given). It runs the model across a **column** of data — writing a
   one-line friendly summary for five sample policies — to show that because it's just a
   function, you can apply a model to a whole table.

**You should see.** A chat reply in the Playground, then a printed answer from `ai_query`,
then a small table of five policies each with an AI-written `blurb`.

> ⚠️ **Free Edition model availability.** On Free Edition the catalogue of models is
> limited, there is no graphics-processor (GPU) serving and no provisioned throughput, and
> exactly which models are enabled varies by region. **Always open the Playground dropdown
> to see what your workspace actually has, and set `LLM_ENDPOINT` to one of those names.**
> `databricks-gpt-oss-120b` is known to work with `ai_query`.

**💡 Genie Code vs the Playground.** The Playground is for *chatting* with a model; **Genie
Code** is for *building* — it writes notebook and SQL code for you from a prompt. Both live
in the same workspace.

### I2. MLOps taster — a claim-frequency model

**What this is.** A gentle introduction to machine learning on the platform. You'll train a
simple **Generalized Linear Model (GLM)** — the classic model actuaries use — to predict how
often a policy will have a claim, record the experiment with **MLflow** (the built-in tool
for tracking models), and register a governed, named version of the model so it can be
reused and audited.

**Where in Databricks.** The notebook `notebooks/I_optional_deep_dives/26_lab_i2_mlops_glm` (open from
**Workspace**).

> ⚠️ **Pick a recent serverless environment first.** This lab uses the `mlflow` and
> `scikit-learn` libraries, which only ship with a **recent environment version**. Before
> running, open the **Environment** panel (top-right of the notebook) and select the latest
> version. On a very old/default environment this lab fails with `No module named 'mlflow'`.

**Steps.**
1. Open `notebooks/I_optional_deep_dives/26_lab_i2_mlops_glm`, attach **Serverless** compute, and select a recent
   **Environment** version (see the warning above).
2. **Section 1 (given)** — run it. It builds the training table: one row per policy with a
   `claim_count` (how many claims that policy had) joined on, and prints the overall claim
   frequency.
3. **Section 2 — fit and track the model.** The setup (imports, train/test split, and the
   model "pipeline") is given. Fill the three `# TODO` lines inside the `with
   mlflow.start_run(...)` block:
   - `pipe.fit(X_train, y_train)` — trains the model.
   - compute the error and log it:
     `mae = mean_absolute_error(y_test, pipe.predict(X_test))` then
     `mlflow.log_metric("mae", mae)`.
   - log and register the trained model:
     ```
     info = mlflow.sklearn.log_model(pipe, artifact_path="model",
              signature=infer_signature(X_test, pipe.predict(X_test)),
              registered_model_name=MODEL_NAME)
     ```
     `MODEL_NAME` comes from `00_config`. Run the cell — this records the run in MLflow and
     saves a versioned model in Unity Catalog (the governance layer).
4. **Section 3 — mark it "champion."** Fill the `# TODO` to tag the new version as the
   current best:
   `MlflowClient(registry_uri="databricks-uc").set_registered_model_alias(MODEL_NAME, "champion", info.registered_model_version)`.
   An *alias* like `@champion` is a friendly pointer to a specific version, so downstream
   code doesn't hard-code a number.
5. **Section 4 — use the model.** Fill the `# TODO` to load the champion and score a few
   rows:
   `champion = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@champion")`, then predict on
   `X_test.head(5)`. Run it.

**You should see.** A printed run id with an error metric (`mae`), a message confirming the
version was registered as `@champion`, and a small table of five policies each with an
`expected_frequency` prediction. You can also open **Machine Learning → Experiments** in the
left sidebar to see the logged run.

**💡 Genie Code.** You can prompt Genie Code — "fit a Poisson GLM for claim_count on
driver_age, engine_cc, penalty_points, ncd_years, cover_type and region, log it to MLflow
and register it" — and refine what it generates instead of filling the TODOs by hand.

---
