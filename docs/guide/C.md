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
