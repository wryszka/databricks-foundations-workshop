# Databricks notebook source
# MAGIC %md
# MAGIC # E1 — Ask questions in plain language with Genie (solution)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** **Genie** lets a business user ask questions of the tenants'
# MAGIC data in plain English — it writes and runs the SQL. It is the "let someone ask"
# MAGIC surface of a data product. (Its sibling **Genie Code** is for *building* — it writes
# MAGIC notebook/SQL code from a prompt. Different tools, same workspace.)
# MAGIC
# MAGIC ### Create a Genie space (in the UI — 2 minutes)
# MAGIC 1. Left sidebar → **Genie** → **New**.
# MAGIC 2. Pick the tables in **your** schema (`3_gold_portfolio_summary`,
# MAGIC    `3_gold_loss_ratio_monthly`, `2_silver_policies`, `2_silver_claims`).
# MAGIC 3. Give it a name (e.g. *Keystone — Portfolio*) and **Create**.
# MAGIC 4. Add a couple of **sample questions** so colleagues know what to ask:
# MAGIC    - "Which tenant has the highest claim frequency?"
# MAGIC    - "Show gross written premium by region for bricksurance_se."
# MAGIC    - "What is the monthly incurred trend this year?"
# MAGIC 5. Ask a question and watch it generate SQL. Click **Show generated code** to see the
# MAGIC    SQL — you will reuse that in lab **E2** to build a dashboard.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Optional / advanced: ask Genie from code
# MAGIC Once your space exists, copy its **space id** from the URL
# MAGIC (`.../genie/rooms/<SPACE_ID>`) into the widget, and run the cell below to ask a
# MAGIC question through the Genie Conversation API.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

# COMMAND ----------

dbutils.widgets.text("space_id", "", "Genie space id (from the space URL)")
SPACE_ID = dbutils.widgets.get("space_id")

if not SPACE_ID:
    print("Set the 'space_id' widget to your Genie space id to run this optional cell.")
else:
    from databricks.sdk import WorkspaceClient
    w = WorkspaceClient()
    msg = w.genie.start_conversation_and_wait(
        space_id=SPACE_ID,
        content="Which tenant has the highest claim frequency?",
    )
    # Print Genie's text answer and any generated SQL
    for att in (msg.attachments or []):
        if att.text:
            print("Answer:", att.text.content)
        if att.query:
            print("Generated SQL:\n", att.query.query)

# COMMAND ----------

# MAGIC %md
# MAGIC ✅ **Done** once your Genie space answers a question. Next: `E2` — turn Genie's
# MAGIC generated SQL into a dashboard.
