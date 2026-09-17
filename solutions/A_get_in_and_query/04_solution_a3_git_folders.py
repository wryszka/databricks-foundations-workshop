# Databricks notebook source
# MAGIC %md
# MAGIC # A3 — Bring code in with Git folders
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** notebooks belong in version control, not in a drawer. A **Git
# MAGIC folder** clones a repository straight into your workspace — which is exactly how this
# MAGIC very workshop was brought in.
# MAGIC
# MAGIC *This is a UI action; the steps are below and the cell at the end confirms where you
# MAGIC are running from.*

# COMMAND ----------

# MAGIC %md
# MAGIC ## Steps (do this in the UI)
# MAGIC 1. In the left sidebar, click **Workspace**.
# MAGIC 2. Click your username → **Create** → **Git folder**.
# MAGIC 3. Paste the repository URL:
# MAGIC    `https://github.com/wryszka/databricks-foundations-workshop`
# MAGIC 4. Leave the provider as **GitHub**, click **Create Git folder**.
# MAGIC 5. Open the new folder — you now have `notebooks/` and `solutions/` locally in your
# MAGIC    workspace, tracked against the remote. Use the **Git** button to pull updates or
# MAGIC    commit changes on a branch.
# MAGIC
# MAGIC > For a private repo you first add a Git credential under
# MAGIC > **Settings → Linked accounts → Git integration** (a personal access token).

# COMMAND ----------

# Confirm you're running from a workspace folder (a Git folder is just a folder that
# happens to be backed by a repo).
path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
print(f"This notebook lives at: {path}")

# COMMAND ----------

# MAGIC %md ✅ **Done.** Your code is version-controlled. Next: **A4 — Secrets**.
