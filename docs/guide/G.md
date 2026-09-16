## Track G — Put an application in front of it

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

**Where in Databricks.** Notebook `notebooks/23_lab_g1_lakebase` (open from the **Workspace**
menu on the left). Real provisioning is also visible later under **Compute → Database
instances** (or **Lakebase**) in the left menu.

**Steps.**
1. Open `notebooks/23_lab_g1_lakebase` from the **Workspace** browser and confirm
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

**Needs the instructor / a partner / live infra.** Creating a real instance + synced table
+ branch (the `provision=yes` path) builds infrastructure that takes minutes and may not be
available on **Databricks Free Edition** — confirm with your instructor before flipping the
widget; otherwise the dry-run printouts and the instructor's live demo cover it.

### G2. A simple app powered by Genie + Lakebase

**What this is.** You'll stand up a tiny web application — a Databricks **App** — that has
one page where you can ask a plain-English question (answered by Genie) and see the
portfolio table. It's the moment the whole day becomes a "product" you can click. The app's
code is already written for you in the `app/` folder; this lab is about pointing it at your
data and deploying it.

**Where in Databricks.** Notebook `notebooks/24_lab_g2_app` (from the **Workspace** menu),
the `app/` folder in your Git folder (its files: `app.py`, `app.yaml`, `requirements.txt`,
`README.md`), and later the **Compute → Apps** area (left menu) where deployed apps appear.

**Steps.**
1. Open `notebooks/24_lab_g2_app` from the **Workspace** browser; confirm **Serverless** is
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

**Needs the instructor / a partner / live infra.** A real app **deploy** needs the
Databricks command-line tool and a workspace where **Databricks Apps** is enabled (confirm
for **Free Edition**), plus a working **Genie space id** from lab E1 and a SQL warehouse.
If Apps isn't available to you, the instructor deploys and demonstrates it and you follow
the configuration steps in the notebook.
