# Databricks Foundations Workshop

A hands-on, full-day Databricks workshop for engineers and architects who are **new to
the platform** and want to learn how to build a **data product on top of it** — bringing
data in, transforming it, governing it across multiple tenants, and sharing it back out.

It is built around one small synthetic insurance book (fictional insurers), but the
skills are general-purpose: the insurance flavour is just a backdrop for platform
concepts. Nothing here is client-specific and the material is intended to be reusable.

> **About this demo / workshop**
> All data is synthetic and generated on the fly. All company names are fictional.
> Nothing here is real customer, policy, or claims data.

## The scenario

You work at **Keystone**, a fictional company that runs a shared data platform for
insurers. Three client insurers — **Bricksurance SE**, **Northwind Mutual**, and
**Helios Re** — are your *tenants*. Across the day you build the platform underneath them:
bring their data in, transform it, keep each tenant isolated, share results, and put a
small app in front. Every row carries a `tenant` column, which is what powers the
isolation, security, and sharing labs.

## Status

✅ **Foundation + all labs built and tested on serverless.** Each lab is a pair: a
`notebooks/NN_lab_*.py` "to solve" notebook (with `# TODO` gaps) and a complete, runnable
`solutions/NN_solution_*.py`.

> **⚠️ Serverless environment version.** Some labs use libraries (e.g. `mlflow`) that ship
> only with a **recent serverless environment**. In the notebook's *Environment* panel pick
> the latest version — on an old/default one, lab I2 fails with `No module named 'mlflow'`.

### Labs

| Track | Labs |
|---|---|
| A. Get in and Query Data | A1 meet the platform · A2 Databricks SQL · A3 Git folders · A4 secrets |
| B. Bring in a Data Source | B1 file upload → Delta · B2 Auto Loader · B3 MERGE + Change Data Feed |
| C. Govern Data across Tenants | C0 Unity Catalog tour · C1 isolation · C2 RLS + masking · C3 managed-vs-external · C4 time travel + SCD2 · C5 clones · C6 maintenance · C7 Catalog Explorer + lineage · C8 system tables |
| D. Transform and Schedule Data | D1 declarative pipeline · D2 schedule as a job |
| E. Analyse and Apply AI | E1 Genie · E2 dashboard from Genie's SQL · E3 AI functions in SQL |
| F. Share Data | F1 Delta Sharing, attendee-to-attendee |
| G. Build a Data App | G1 Lakebase (+ branch/clone) · G2 simple app over Genie + Lakebase (`app/`) |
| H. Connect an External Database (Snowflake) *· optional* | H1 federation · H2 scheduled ingestion |
| I. Optional Deep Dives | I1 LLM primer / AI Playground · I2 MLOps GLM + MLflow |

### Verified on Databricks Free Edition (2026-09-18)

The whole workshop was run end-to-end on a real Free Edition workspace (catalog `workspace`):

- **Notebooks:** A1–A4, B1–B3, C0–C8, D2, E1–E3, F1, G1/G2, H1/H2, I1/I2 all run green.
- **D1** runs as a real **Lakeflow pipeline** → COMPLETED (Free allows one pipeline).
- **G1 Lakebase** instance provisioned and AVAILABLE (Free allows one project).
- **E1 Genie** space created over the workshop tables.
- **G2 app** deployed and RUNNING (Free allows up to three apps).
- **H1/H2 Snowflake federation** green against a live trial.

**One Free-Edition gap:** Materialized Views aren't enabled on Free serverless, so H1
caches to a plain Delta table instead (handled in the notebook); `remote_query` also needs
an explicit `database` (handled). **Genuinely manual by design:** E2 builds the dashboard in
the UI (its tile SQL is verified), F1 needs a partner to mount the share, and the *true*
cross-tenant isolation in C1/C2 needs a second principal to observe.

### Data the generator produces

| Asset | Contents |
|---|---|
| Volume `raw/` | `policies.csv`, `claims.csv` (deliberately messy), `claims_batch_02.csv` (staged for lab B2) |
| Volume `landing/claims/` | `claims_batch_01.csv` — an arrived Auto Loader batch |
| Volume `docs/` | ~15 claim documents as text (for `ai_extract` / `ai_summarize`) |
| `2_silver_complaints` | free-text complaint notes with real sentiment (for `ai_analyze_sentiment`) |
| `2_silver_property_policies` | a small, clean second line of business |
| `build_all=yes` also builds | `2_silver_policies`, `2_silver_claims`, `3_gold_portfolio_summary`, `3_gold_loss_ratio_monthly` |

Quick start: import this repo (Workspace → Git folder), open `notebooks/00_setup/00_config`, set your
catalog/schema, run `01_data_generator`, then follow the labs.

## Step-by-step attendee runbook (start here if you're new)

A comprehensive, beginner-level walkthrough — signing in, the UI tour, importing this repo,
and click-by-click steps for every lab:

- In the repo: [`ATTENDEE_GUIDE.md`](ATTENDEE_GUIDE.md)
- As a Google Doc: **[Databricks Foundations Workshop — Attendee Runbook](https://docs.google.com/document/d/1TnbQasUgN6s1LMBjLM4ITRNuaISAR6ZHcgUnB8ByaYM/edit)**

## Use-case list & instructions

The living list of use cases (what each lab teaches, hands-on vs. demo, Free Edition
feasibility) lives in the workshop instructions document. This is the source of truth we
add to as the workshop takes shape:

**[Workshop instructions & use-case list (Google Doc)](https://docs.google.com/document/d/1SHEQdec3DxwWHbeUCWGQzPRU7kH5pjzpwNnsflBhFTg/edit)** — under review.

## Portability & Free Edition

- Designed to run on any Databricks workspace, including **Databricks Free Edition**
  (serverless-only, Databricks-managed storage, catalog `main`).
- Plain notebooks, config-driven catalog/schema, no external data dependencies for the
  core hands-on labs.
- Some platform capabilities (cross-organisation sharing, bring-your-own storage,
  federation to external databases) are constrained on Free Edition and are run as
  instructor-led demonstrations rather than attendee hands-on. The instructions document
  marks each case accordingly.

## Layout

```
notebooks/    "to solve" lab notebooks, grouped by track:
  00_setup/                00_config, 01_data_generator
  A_get_in_and_query/      02–05
  B_bring_a_source_in/     06–08
  C_govern_across_tenants/ 09–16
  D_transform_and_schedule/17–18
  E_analytics_and_ai/      19–21
  F_share/                 22
  G_app/                   23–24
  H_external_snowflake/    27–28 (optional)
  I_optional_deep_dives/   25–26
solutions/    complete, runnable solutions in the same per-track subfolders (NN_solution_*)
app/          the G2 Databricks App (FastAPI: Genie Q&A + portfolio lookup)
docs/         AUTHORING.md (conventions + numbering map) and guide/ (runbook sections)
```
