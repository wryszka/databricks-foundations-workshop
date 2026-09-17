## Part 1 — The tracks at a glance

The day is organised into **tracks**. Each track is a theme; each track has a few **labs**.
Work through them in order — later labs assume the tables from earlier ones. You will not
finish everything, and that's fine: there is more here than one day needs.

| Track | What it's about | Labs |
|---|---|---|
| **A. Get in and Query Data** | Find your way around, run your first queries, and meet the tools. | A1 meet the platform · A2 Databricks SQL · A3 Git folders · A4 secrets |
| **B. Bring in a Data Source** | Get data onto the platform: a one-off file, then files that keep arriving, then keeping a table in sync. | B1 file upload · B2 Auto Loader · B3 MERGE + Change Data Feed |
| **C. Govern Data across Tenants** | Keep each customer's data separate and safe, and understand how the platform tracks and protects data. | C1 isolation · C2 row security + masking · C3 managed vs external tables · C4 time travel + history · C5 clones · C6 maintenance · C7 catalog + lineage · C8 system tables |
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
- **H** and **I** are optional. **H** needs a Snowflake instance (the instructor sets this
  up); until then its notebooks skip themselves safely.

Each lab below follows the same shape: **What this is → Where in Databricks → Steps → You
should see**, plus a **💡 Genie Code** tip where an AI assistant could write the code for
you, and an honest note wherever a step needs the instructor, a partner, or extra setup.

---

# Part 2 — The labs, step by step
