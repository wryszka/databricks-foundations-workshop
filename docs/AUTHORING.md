# Authoring guide (for building the labs)

Shared conventions so every lab looks and behaves the same. Read before adding notebooks.

## Scenario & data (recap)

Fictional company **Keystone** runs a data platform for insurers; tenants are
**bricksurance_se**, **northwind_mutual**, **helios_re** (every row has a `tenant` column).
`notebooks/01_data_generator.py` (run with `build_all=yes` for a full set) produces:

- Volume `raw/`: `policies.csv`, `claims.csv` (messy), `claims_batch_02.csv` (staged for B2)
- Volume `landing/claims/`: `claims_batch_01.csv` (arrived Auto Loader batch)
- Volume `docs/`: ~15 `claim_*.txt` documents
- `2_silver_complaints` (claim_id, policy_id, tenant, received_date, note — free text)
- `2_silver_property_policies` (property_policy_id, tenant, region, construction_year, sum_insured, flood_zone, annual_premium)
- with `build_all=yes`: `2_silver_policies` (policy_id, tenant, region, driver_age, ncd_years,
  penalty_points, vehicle_make, engine_cc, cover_type, start_date, annual_premium),
  `2_silver_claims` (claim_id, policy_id, tenant, claim_type, claim_date, incurred_amount, status),
  `3_gold_portfolio_summary`, `3_gold_loss_ratio_monthly`

## Two notebooks per lab

- **`notebooks/NN_lab_<id>_<slug>.py`** — the "to solve" notebook: working scaffolding with
  clearly marked `# TODO` gaps for the attendee to fill, plus hints. It need not run end to
  end (the gaps stop it) — that is expected.
- **`solutions/NN_solution_<id>_<slug>.py`** — the complete, correct version. **This must run
  top to bottom on serverless.**

Same `NN` number for both. Numbering map below is fixed to avoid collisions.

## Notebook conventions

1. First line: `# Databricks notebook source`.
2. First cell (`# MAGIC %md`): H1 title `# <ID> — <name>`, then a one-line
   **About this workshop** disclaimer (synthetic data, fictional companies), then a short
   **What is this for** paragraph framing it in the Keystone builder story.
3. Second cell: `# MAGIC %run ./00_config` (labs read `CATALOG`, `SCHEMA`, `FQ`,
   `RAW_VOLUME`, `LANDING_VOLUME`, `DOCS_VOLUME`, `TENANTS`, `MODEL_NAME` from it).
4. Use the config variables — never hardcode catalog/schema. Tables use the `1_`/`2_`/`3_`
   numeric-prefix convention. Keep insurance framing light; lead with the platform concept.
5. Where an AI helper is a natural shortcut, add a one-line md note:
   `> 💡 **Genie Code:** you could prompt Genie Code to generate this instead of typing it.`
6. Last cell (`# MAGIC %md`): `✅ **Done.**` + one line pointing to the next lab.
7. No "WOW"/marketing labels. Serverless rules: no `.cache()`, seeded `rand()` recomputes;
   write local temp then copy for any non-CSV file to a volume (CSV `to_csv` to `/Volumes` is fine).

## Fixed numbering map

| NN | ID | slug | notes |
|----|----|------|-------|
| 02 | A1 | meet_platform | Delta query, %sql vs Python, chart, Assistant |
| 03 | A2 | sql_warehouse | DBSQL, saved query, view, `ai_classify` teaser |
| 04 | A3 | git_folders | mostly md (UI action) — how to import a repo as a Git folder |
| 05 | A4 | secrets | create a secret scope (CLI/UI, in md) + read it in code |
| 06 | B1 | file_upload | messy `raw/policies.csv` → bronze → silver |
| 07 | B2 | autoloader | Auto Loader on `landing/claims/`; drop `claims_batch_02.csv` mid-lab |
| 08 | B3 | merge_cdf | `MERGE` upsert + Change Data Feed read-back |
| 09 | C1 | isolation | schema-per-tenant + grants (USE/SELECT/browse) |
| 10 | C2 | rls_masking | row filter + column mask on a shared table |
| 11 | C3 | managed_vs_external | create managed, DROP, `UNDROP`/time-travel myth-buster |
| 12 | C4 | time_travel_scd2 | time travel + SCD2 history |
| 13 | C5 | clones | shallow vs deep `CLONE` |
| 14 | C6 | maintenance | `OPTIMIZE`, liquid clustering, `VACUUM` |
| 15 | C7 | catalog_lineage | Catalog Explorer (md) + query lineage/system tables |
| 16 | C8 | system_tables | `system.*` — access, lineage, cost (note FE gaps) |
| 17 | D1 | pipeline | Spark Declarative Pipeline (bronze→silver→gold, expectations) |
| 18 | D2 | job | schedule the pipeline as a Job + a dependent task |
| 19 | E1 | genie | create/query a Genie space over the schema |
| 20 | E2 | dashboard | AI/BI dashboard from Genie's generated SQL |
| 21 | E3 | ai_functions | `ai_classify`/`ai_analyze_sentiment`/`ai_extract`/`ai_summarize`/`ai_mask` in SQL |
| 22 | F1 | delta_sharing | share a tenant gold table attendee-to-attendee |
| 23 | G1 | lakebase | Lakebase (managed Postgres) + sync gold table + branch/clone |
| 24 | G2 | app | simple Databricks App over Genie + Lakebase |
| 25 | I1 | llm_playground | AI Playground / foundation models primer |
| 26 | I2 | mlops_glm | simple frequency GLM + MLflow tracking/versioning |
| 27 | H1 | snowflake_federation | *optional* — federate Snowflake (CONNECTION + FOREIGN CATALOG, query in place, MV cache, remote_query) |
| 28 | H2 | scheduled_ingest | *optional* — copy vs federate: schedule ingestion of the Snowflake data into a managed table |

## Testing recipe (DEV)

Profile `DEV`, catalog `lr_dev_aws_us_catalog`, warehouse `a3b61648ea4809e3`. Run solved
notebooks as serverless notebook jobs:

```
databricks workspace import-dir <local> <ws_path> -p DEV --overwrite
databricks jobs submit --json '{"run_name":"t","tasks":[{"task_key":"t",
  "notebook_task":{"notebook_path":"<ws_path>/<nb>",
  "base_parameters":{"catalog":"lr_dev_aws_us_catalog","schema":"<your_test_schema>"}}}]}' -p DEV
```

UI/infra labs (Genie space, dashboard, Delta Sharing recipient, Lakebase, App) may not run
fully headless — build the asset + instructions and note what needs live infra to verify.
