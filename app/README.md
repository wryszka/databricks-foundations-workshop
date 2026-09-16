# Keystone mini-app (lab G2)

A deliberately small Databricks App: ask **Genie** a question, and look up the governed
**portfolio** table. The portfolio comes from **Lakebase** (Postgres) when `LAKEBASE_HOST`
is set, otherwise from the **SQL warehouse** — so it works even before you finish lab G1.

## Files
- `app.py` — FastAPI app (one HTML page + `/api/ask` and `/api/portfolio`)
- `app.yaml` — run command + environment
- `requirements.txt` — dependencies

## Configure
Edit `app.yaml` (or wire app resources):
- `KEYSTONE_CATALOG`, `KEYSTONE_SCHEMA` — where `3_gold_portfolio_summary` lives
- `DATABRICKS_WAREHOUSE_ID` — a SQL warehouse the app can use
- `GENIE_SPACE_ID` — the space from lab E1
- `LAKEBASE_*` — only if you want the operational (Postgres) path from lab G1

## Run locally
```
pip install -r requirements.txt
export DATABRICKS_WAREHOUSE_ID=... GENIE_SPACE_ID=... KEYSTONE_CATALOG=... KEYSTONE_SCHEMA=...
uvicorn app:app --reload
```

## Deploy as a Databricks App
```
databricks apps create keystone-mini-app
databricks sync . /Workspace/Users/<you>/keystone-mini-app
databricks apps deploy keystone-mini-app --source-code-path /Workspace/Users/<you>/keystone-mini-app
```
Grant the app's service principal `CAN USE` on the warehouse, `CAN RUN` on the Genie space,
and access to the catalog/schema (and the Lakebase instance if used).
