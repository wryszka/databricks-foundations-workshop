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
