"""Keystone mini-app — a tiny Databricks App over Genie + a governed table.

Two data paths, chosen by environment:
  * portfolio lookup: Lakebase Postgres if LAKEBASE_HOST is set, else the SQL warehouse
    (DATABRICKS_WAREHOUSE_ID) reading <CATALOG>.<SCHEMA>.3_gold_portfolio_summary
  * ask: Databricks Genie (GENIE_SPACE_ID)

Deliberately small and dependency-light so it is easy to read in a workshop.
"""
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from databricks.sdk import WorkspaceClient

CATALOG = os.environ.get("KEYSTONE_CATALOG", "main")
SCHEMA = os.environ.get("KEYSTONE_SCHEMA", "keystone")
WAREHOUSE_ID = os.environ.get("DATABRICKS_WAREHOUSE_ID", "")
GENIE_SPACE_ID = os.environ.get("GENIE_SPACE_ID", "")
LAKEBASE_HOST = os.environ.get("LAKEBASE_HOST", "")

app = FastAPI(title="Keystone mini-app")
w = WorkspaceClient()


def portfolio_from_warehouse(tenant: str):
    """Read the gold table through the SQL warehouse (no Lakebase required)."""
    where = f"WHERE tenant = '{tenant}'" if tenant else ""
    sql = (f"SELECT tenant, region, cover_type, policies, gwp "
           f"FROM {CATALOG}.{SCHEMA}.`3_gold_portfolio_summary` {where} "
           f"ORDER BY gwp DESC LIMIT 50")
    resp = w.statement_execution.execute_statement(
        warehouse_id=WAREHOUSE_ID, statement=sql, wait_timeout="30s")
    data = resp.result.data_array if resp.result else []
    cols = [c.name for c in resp.manifest.schema.columns] if resp.manifest else []
    return [dict(zip(cols, row)) for row in (data or [])]


def portfolio_from_lakebase(tenant: str):
    """Read the synced table from Lakebase Postgres (operational path)."""
    import psycopg  # imported lazily so the app runs without the driver when unused
    cred = w.database.generate_database_credential(instance_names=[os.environ["LAKEBASE_INSTANCE"]])
    where = "WHERE tenant = %s" if tenant else ""
    params = (tenant,) if tenant else ()
    with psycopg.connect(host=LAKEBASE_HOST, dbname="databricks_postgres",
                         user=os.environ["LAKEBASE_USER"], password=cred.token,
                         sslmode="require") as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT tenant, region, cover_type, policies, gwp "
                        f"FROM portfolio_pg {where} ORDER BY gwp DESC LIMIT 50", params)
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]


@app.get("/api/portfolio")
def portfolio(tenant: str = ""):
    try:
        rows = portfolio_from_lakebase(tenant) if LAKEBASE_HOST else portfolio_from_warehouse(tenant)
        return {"rows": rows}
    except Exception as e:  # keep the app responsive; surface the error to the page
        return JSONResponse({"error": str(e)}, status_code=500)


class Ask(BaseModel):
    question: str


@app.post("/api/ask")
def ask(body: Ask):
    if not GENIE_SPACE_ID:
        return JSONResponse({"error": "GENIE_SPACE_ID not set"}, status_code=400)
    try:
        msg = w.genie.start_conversation_and_wait(GENIE_SPACE_ID, body.question)
        text = " ".join(a.text.content for a in (msg.attachments or []) if a.text)
        sql = next((a.query.query for a in (msg.attachments or []) if a.query), "")
        return {"answer": text or "(no text answer)", "sql": sql}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/", response_class=HTMLResponse)
def home():
    return """<!doctype html><meta charset=utf-8><title>Keystone mini-app</title>
<style>body{font:14px system-ui;margin:2rem;max-width:800px}input{padding:.4rem}
button{padding:.4rem .8rem}table{border-collapse:collapse;margin-top:1rem}
td,th{border:1px solid #ccc;padding:.3rem .6rem}pre{background:#f4f4f4;padding:.6rem}</style>
<h1>Keystone mini-app</h1>
<h3>Ask Genie</h3>
<input id=q size=50 placeholder="which tenant has the most policies?">
<button onclick=ask()>Ask</button>
<div id=ans></div>
<h3>Portfolio lookup</h3>
<input id=t size=20 placeholder="tenant (blank = all)">
<button onclick=load()>Load</button>
<div id=tbl></div>
<script>
async function ask(){let r=await fetch('/api/ask',{method:'POST',headers:{'content-type':'application/json'},
 body:JSON.stringify({question:document.getElementById('q').value})});let d=await r.json();
 document.getElementById('ans').innerHTML=d.error?('<p style=color:red>'+d.error+'</p>'):
 ('<p>'+d.answer+'</p>'+(d.sql?'<pre>'+d.sql+'</pre>':''));}
async function load(){let r=await fetch('/api/portfolio?tenant='+encodeURIComponent(document.getElementById('t').value));
 let d=await r.json();if(d.error){document.getElementById('tbl').innerHTML='<p style=color:red>'+d.error+'</p>';return;}
 let rows=d.rows;if(!rows.length){document.getElementById('tbl').innerHTML='<p>no rows</p>';return;}
 let h='<table><tr>'+Object.keys(rows[0]).map(k=>'<th>'+k+'</th>').join('')+'</tr>';
 h+=rows.map(x=>'<tr>'+Object.values(x).map(v=>'<td>'+v+'</td>').join('')+'</tr>').join('')+'</table>';
 document.getElementById('tbl').innerHTML=h;}
</script>"""
