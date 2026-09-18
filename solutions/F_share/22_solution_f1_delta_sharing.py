# Databricks notebook source
# MAGIC %md
# MAGIC # F1 — Delta Sharing, attendee to attendee (solution)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** a Keystone tenant's results often need to go to someone *outside*
# MAGIC your walls — the client insurer, an auditor, a reinsurer. Delta Sharing hands over a
# MAGIC live, governed table **without copying files** and **without giving access to your
# MAGIC workspace**. In this lab you pair up: you publish a share, your partner adds it and
# MAGIC queries it (and vice-versa).
# MAGIC
# MAGIC > 💡 **Genie Code:** you could prompt Genie Code to draft these `CREATE SHARE` /
# MAGIC > `ALTER SHARE` statements for you.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

# COMMAND ----------

# MAGIC %md
# MAGIC ### 0. Make sure there is something to share
# MAGIC We share a gold table. If you have not run the generator with `build_all=yes` (or done
# MAGIC Track D), build a small one now from whatever silver data exists.

# COMMAND ----------

if not spark.catalog.tableExists(f"{FQ}.3_gold_portfolio_summary"):
    if spark.catalog.tableExists(f"{FQ}.2_silver_policies"):
        spark.sql(f"""
            CREATE OR REPLACE TABLE {FQ}.`3_gold_portfolio_summary` AS
            SELECT tenant, region, cover_type, count(*) AS policies,
                   round(sum(annual_premium), 2) AS gwp
            FROM {FQ}.`2_silver_policies` GROUP BY tenant, region, cover_type
        """)
    else:
        raise Exception("No silver data — run 01_data_generator with build_all=yes first.")
print("shareable table ready:", f"{FQ}.3_gold_portfolio_summary")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Create a share and add a tenant's table
# MAGIC A **share** is a named, read-only bundle of tables a provider offers. We add one
# MAGIC tenant's slice of the gold table using a partition, so the recipient sees only that
# MAGIC tenant — exactly how you would hand a client *their* data and no one else's.
# MAGIC
# MAGIC > These statements need `CREATE SHARE` on the metastore (a metastore-admin privilege).
# MAGIC > The helper below runs them and, if you do not have the privilege yet, prints what to
# MAGIC > ask for instead of failing — so the rest of the notebook still teaches.

# COMMAND ----------

SHARE = f"keystone_share_{SCHEMA}"
RECIPIENT = f"keystone_partner_{SCHEMA}"
SHARE_TENANT = TENANTS[0]  # share only this tenant's rows

def try_sql(sql, need=""):
    try:
        spark.sql(sql); print("OK:", sql.split(chr(10))[0][:90]); return True
    except Exception as e:
        msg = str(e)
        if "PERMISSION_DENIED" in msg or "does not have" in msg:
            print(f"NEEDS PRIVILEGE ({need}): {sql.splitlines()[0][:80]}")
        else:
            print("ERROR:", msg[:200])
        return False

# You must hold USE CATALOG / USE SCHEMA on a table to add it to a share — grant to yourself.
me = spark.sql("SELECT current_user()").first()[0]
try_sql(f"GRANT USE CATALOG ON CATALOG {CATALOG} TO `{me}`", need="owner/admin")
try_sql(f"GRANT USE SCHEMA ON SCHEMA {FQ} TO `{me}`", need="owner/admin")

try_sql(f"CREATE SHARE IF NOT EXISTS {SHARE} COMMENT 'Keystone gold portfolio share'",
        need="CREATE SHARE on metastore")
# Add just one tenant's partition — the recipient never sees the others.
try_sql(f"ALTER SHARE {SHARE} ADD TABLE {FQ}.`3_gold_portfolio_summary` "
        f"PARTITION (tenant = '{SHARE_TENANT}') AS keystone.portfolio_{SHARE_TENANT}",
        need="CREATE SHARE on metastore")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Create a recipient and grant the share
# MAGIC For **Databricks-to-Databricks** sharing, your partner gives you their *sharing
# MAGIC identifier* (`SELECT current_metastore()` in their workspace) and you set the
# MAGIC `partner_sharing_id` widget. Leave it blank for **open sharing**, which produces an
# MAGIC activation link file you can hand to any client.
# MAGIC
# MAGIC > **On Free Edition:** creating an external **recipient** needs *External Delta Sharing*
# MAGIC > enabled on the metastore, which Free doesn't permit ("External Delta Sharing is not
# MAGIC > enabled on the metastore"). So on Free you author the share (steps 0–1, which work)
# MAGIC > and the recipient hand-off is shown on a full workspace. The helper prints a note
# MAGIC > instead of failing, so the notebook still completes.

# COMMAND ----------

dbutils.widgets.text("partner_sharing_id", "", "Partner sharing identifier (blank = open sharing)")
partner = dbutils.widgets.get("partner_sharing_id").strip()

if partner:
    try_sql(f"CREATE RECIPIENT IF NOT EXISTS {RECIPIENT} USING ID '{partner}'",
            need="CREATE RECIPIENT on metastore")
else:
    try_sql(f"CREATE RECIPIENT IF NOT EXISTS {RECIPIENT}", need="CREATE RECIPIENT on metastore")

try_sql(f"GRANT SELECT ON SHARE {SHARE} TO RECIPIENT {RECIPIENT}", need="owner of the share")

# COMMAND ----------

# MAGIC %md ### 3. Inspect what you published

# COMMAND ----------

for q in (f"SHOW SHARES LIKE '{SHARE}'",
          f"SHOW ALL IN SHARE {SHARE}",
          f"DESCRIBE RECIPIENT {RECIPIENT}"):  # activation link shows here for open sharing
    try:
        print("#", q); display(spark.sql(q))
    except Exception as e:
        print("  (skipped —", str(e)[:80], ")")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. The partner side (run in your partner's workspace)
# MAGIC Your partner mounts your share as a catalog and queries it — no copy, always live:
# MAGIC ```sql
# MAGIC -- partner lists providers, then mounts the share
# MAGIC CREATE CATALOG IF NOT EXISTS from_keystone USING SHARE <your_provider_name>.<share_name>;
# MAGIC SELECT * FROM from_keystone.keystone.portfolio_bricksurance_se;
# MAGIC ```
# MAGIC For **open sharing**, hand them the activation link from step 3 instead.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5. Clean up (optional)

# COMMAND ----------

# Uncomment to remove what you created:
# try_sql(f"DROP RECIPIENT IF EXISTS {RECIPIENT}")
# try_sql(f"DROP SHARE IF EXISTS {SHARE}")
print("done")

# COMMAND ----------

# MAGIC %md
# MAGIC ✅ **Done.** You published a governed, tenant-scoped share. Next: `G1` — put an
# MAGIC operational database behind an app.
