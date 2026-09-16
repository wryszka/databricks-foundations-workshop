# Databricks notebook source
# MAGIC %md
# MAGIC # E1 — Ask questions in plain language with Genie
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** **Genie** lets a business user ask questions of the tenants'
# MAGIC data in plain English — it writes and runs the SQL. It is the "let someone ask"
# MAGIC surface of a data product. (Its sibling **Genie Code** is for *building* — it writes
# MAGIC notebook/SQL code from a prompt. Different tools, same workspace.)
# MAGIC
# MAGIC ### Your task — create a Genie space (in the UI, ~2 minutes)
# MAGIC 1. Left sidebar → **Genie** → **New**.
# MAGIC 2. Pick the tables in **your** schema (`3_gold_portfolio_summary`,
# MAGIC    `3_gold_loss_ratio_monthly`, `2_silver_policies`, `2_silver_claims`).
# MAGIC 3. Name it (e.g. *Keystone — Portfolio*) and **Create**.
# MAGIC 4. Add sample questions, e.g.:
# MAGIC    - "Which tenant has the highest claim frequency?"
# MAGIC    - "Show gross written premium by region for bricksurance_se."
# MAGIC 5. Ask one, then click **Show generated code** to see the SQL — you will reuse it in
# MAGIC    lab **E2**.
# MAGIC
# MAGIC The optional cell below shows how to ask Genie from code once your space exists.
# MAGIC Full version: `solutions/19_solution_e1_genie`.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

dbutils.widgets.text("space_id", "", "Genie space id (from the space URL)")
SPACE_ID = dbutils.widgets.get("space_id")

# TODO (optional): set the space_id widget to your new space, then complete the call:
if SPACE_ID:
    from databricks.sdk import WorkspaceClient
    w = WorkspaceClient()
    # TODO: msg = w.genie.start_conversation_and_wait(space_id=SPACE_ID, content="<your question>")
    # TODO: print msg.attachments' text / query
    pass
else:
    print("Create your Genie space in the UI first, then set the space_id widget.")

# COMMAND ----------

# MAGIC %md ✅ **Done** once your Genie space answers a question. Next: `E2`.
