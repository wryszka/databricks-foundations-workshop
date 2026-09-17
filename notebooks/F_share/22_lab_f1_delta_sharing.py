# Databricks notebook source
# MAGIC %md
# MAGIC # F1 — Delta Sharing, attendee to attendee
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** a Keystone tenant's results often need to go to someone *outside*
# MAGIC your walls — the client insurer, an auditor, a reinsurer. Delta Sharing hands over a
# MAGIC live, governed table **without copying files** and **without giving access to your
# MAGIC workspace**. Pair up: you publish a share, your partner adds it and queries it.
# MAGIC
# MAGIC > 💡 **Genie Code:** you could prompt Genie Code to draft these `CREATE SHARE` /
# MAGIC > `ALTER SHARE` statements for you.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# MAGIC %md
# MAGIC ### 0. Make sure there is something to share
# MAGIC We share a gold table. If `3_gold_portfolio_summary` does not exist, run
# MAGIC `01_data_generator` with `build_all=yes` (or finish Track D) first.

# COMMAND ----------

assert spark.catalog.tableExists(f"{FQ}.3_gold_portfolio_summary"), \
    "Run 01_data_generator with build_all=yes first."
print("shareable table ready")

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Create a share and add ONE tenant's slice
# MAGIC A **share** is a named, read-only bundle of tables. Add a single tenant's partition so
# MAGIC the recipient sees only that tenant.

# COMMAND ----------

SHARE = f"keystone_share_{SCHEMA}"
SHARE_TENANT = TENANTS[0]

# TODO 1: create a share named `SHARE`.
#   Hint: spark.sql(f"CREATE SHARE IF NOT EXISTS {SHARE} COMMENT '...'")
# TODO 2: add only SHARE_TENANT's rows of `3_gold_portfolio_summary` to the share.
#   Hint: ALTER SHARE {SHARE} ADD TABLE {FQ}.`3_gold_portfolio_summary`
#         PARTITION (tenant = '{SHARE_TENANT}') AS keystone.portfolio_{SHARE_TENANT}
# (These need CREATE SHARE on the metastore. If you lack it, ask your instructor.)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. Create a recipient and grant the share
# MAGIC Databricks-to-Databricks: your partner runs `SELECT current_metastore()` and gives you
# MAGIC the value. Set it below, or leave blank for open sharing (activation link).

# COMMAND ----------

RECIPIENT = f"keystone_partner_{SCHEMA}"
dbutils.widgets.text("partner_sharing_id", "", "Partner sharing identifier (blank = open)")
partner = dbutils.widgets.get("partner_sharing_id").strip()

# TODO 3: create the recipient. If `partner` is set, use `... USING ID '{partner}'`;
#         otherwise create a plain (open-sharing) recipient.
# TODO 4: GRANT SELECT ON SHARE {SHARE} TO RECIPIENT {RECIPIENT}

# COMMAND ----------

# MAGIC %md ### 3. Inspect what you published

# COMMAND ----------

# TODO 5: display SHOW SHARES LIKE '{SHARE}', SHOW ALL IN SHARE {SHARE},
#         and DESCRIBE RECIPIENT {RECIPIENT} (the activation link is here for open sharing).

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. The partner side (in your partner's workspace)
# MAGIC ```sql
# MAGIC CREATE CATALOG IF NOT EXISTS from_keystone USING SHARE <provider>.<share>;
# MAGIC SELECT * FROM from_keystone.keystone.portfolio_bricksurance_se;
# MAGIC ```

# COMMAND ----------

# MAGIC %md ✅ **Done** when your partner can query your share. Next: `G1`.
