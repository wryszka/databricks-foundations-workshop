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
| A — Get in & query | A1 meet the platform · A2 Databricks SQL · A3 Git folders · A4 secrets |
| B — Bring a source in | B1 file upload → Delta · B2 Auto Loader · B3 MERGE + Change Data Feed |
| C — Govern across tenants | C1 isolation · C2 RLS + masking · C3 managed-vs-external · C4 time travel + SCD2 · C5 clones · C6 maintenance · C7 Catalog Explorer + lineage · C8 system tables |
| D — Transform & schedule | D1 declarative pipeline · D2 schedule as a job |
| E — Analytics & AI | E1 Genie · E2 dashboard from Genie's SQL · E3 AI functions in SQL |
| F — Share | F1 Delta Sharing, attendee-to-attendee |
| G — Put an app in front | G1 Lakebase (+ branch/clone) · G2 simple app over Genie + Lakebase (`app/`) |
| I — Optional deep-dives | I1 LLM primer / AI Playground · I2 MLOps GLM + MLflow |

**Verified green headless on serverless:** A1–A4, B1–B3, C1–C8, D1 (live pipeline run), D2
check-cell, E3 (all five `ai_*` functions), I1 (`ai_query` via `databricks-gpt-oss-120b`),
I2 (GLM + MLflow on a recent environment).

**Need live UI / infra / a second identity to fully demonstrate** (built + written as
instructions; flagged in each notebook): E1 Genie space, E2 dashboard object, F1 share
recipient + partner mount, G1 Lakebase provisioning, G2 app deploy, and the true
cross-tenant *isolation* in C1/C2 (needs a second principal). System/billing tables (C8)
depend on workspace tier.

### Data the generator produces

| Asset | Contents |
|---|---|
| Volume `raw/` | `policies.csv`, `claims.csv` (deliberately messy), `claims_batch_02.csv` (staged for lab B2) |
| Volume `landing/claims/` | `claims_batch_01.csv` — an arrived Auto Loader batch |
| Volume `docs/` | ~15 claim documents as text (for `ai_extract` / `ai_summarize`) |
| `2_silver_complaints` | free-text complaint notes with real sentiment (for `ai_analyze_sentiment`) |
| `2_silver_property_policies` | a small, clean second line of business |
| `build_all=yes` also builds | `2_silver_policies`, `2_silver_claims`, `3_gold_portfolio_summary`, `3_gold_loss_ratio_monthly` |

Quick start: import this repo (Workspace → Git folder), open `00_config`, set your
catalog/schema, run `01_data_generator`, then follow the labs.

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
notebooks/    "to solve" lab notebooks (00_config, 01_data_generator, then NN_lab_*)
solutions/    complete, runnable solution notebooks (NN_solution_*)
app/          the G2 Databricks App (FastAPI: Genie Q&A + portfolio lookup)
docs/         AUTHORING.md — conventions and the lab numbering map
```
