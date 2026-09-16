## Track A — Get in and query

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

**Where in Databricks.** Notebook `notebooks/02_lab_a1_meet_platform` — open it from the
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

**Where in Databricks.** Notebook `notebooks/03_lab_a2_sql_warehouse` (Workspace →
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
`notebooks/04_lab_a3_git_folders` (for the confirmation cell). This is mostly a UI action.

**Steps.**
1. You already did this in Part 0, so here you're just confirming you understand it. In
   the left menu click **Workspace**, then your username / **Home**.
2. Click the **Create** button (top-right) → **Git folder**.
3. In **Git repository URL** you would paste a repo address, e.g.
   `https://github.com/wryszka/databricks-foundations-workshop`, leave the provider as
   **GitHub**, and click **Create Git folder**. (You've already got this folder, so you
   don't need to create it again — just note the steps.)
4. Open `notebooks/04_lab_a3_git_folders` and run the single code cell. It prints the path
   where the notebook lives, showing you're running from a repo-backed folder.
5. Note the tip: to use the **Git** button (pull/commit changes on a branch), a private
   repo needs a Git credential set under **Settings → Linked accounts** first.

**You should see.** A printed line like
`This notebook lives at: /Workspace/Users/you/databricks-foundations-workshop/notebooks/04_lab_a3_git_folders`.

**Needs the instructor.** Creating a Git folder against a *private* repo needs a linked
Git credential — your instructor will show this if relevant; the public workshop repo
needs nothing.

---

### A4. Store credentials safely with secrets

**What this is.** Real products connect to other systems using passwords/keys. You never
paste those into a notebook — you store them in a **secret scope** and read them back by
name. Here you read a pre-made secret.

**Where in Databricks.** Notebook `notebooks/05_lab_a4_secrets`. Creating a secret is a
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
