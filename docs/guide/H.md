## H. Connect an External Database (Snowflake) · *Optional*

Not every client will move their data to you. This optional track connects Keystone to a
client's existing **Snowflake** database (another cloud data warehouse) two ways: query it
**live without copying** (federation), and **copy it on a schedule**. You then compare the
trade-offs. This track only works once a Snowflake instance is set up and the two widgets
are pointed at it — until then the notebooks skip themselves cleanly, so they're safe to
open and read.

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

**Needs the instructor / live infra.** A **Snowflake instance** and the `CREATE CONNECTION`
privilege on the metastore. If you don't have those, watch the instructor run it.

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

**Needs the instructor / live infra.** Same Snowflake instance as H1. Note: Databricks'
fully-managed *Lakeflow Connect* connectors (SQL Server, Salesforce, ServiceNow, …) don't
include Snowflake today, so this lab ingests through the H1 federation connection.
