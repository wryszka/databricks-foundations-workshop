# Databricks notebook source
# MAGIC %md
# MAGIC # A3 — Bring code in with Git folders
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** notebooks belong in version control. A **Git folder** clones a
# MAGIC repository into your workspace — exactly how this workshop was brought in.
# MAGIC
# MAGIC *This is a UI action — follow the steps, then run the confirm cell.*

# COMMAND ----------

# MAGIC %md
# MAGIC ## Steps (in the UI)
# MAGIC 1. Left sidebar → **Workspace**.
# MAGIC 2. Your username → **Create** → **Git folder**.
# MAGIC 3. Repository URL: `https://github.com/wryszka/databricks-foundations-workshop`
# MAGIC 4. Provider **GitHub** → **Create Git folder**.
# MAGIC 5. Open it — you now have `notebooks/` and `solutions/` tracked against the remote.
# MAGIC    Use the **Git** button to pull/commit on a branch.
# MAGIC
# MAGIC > Private repo? Add a Git credential first under **Settings → Linked accounts**.

# COMMAND ----------

# Run to confirm where you're executing from (a Git folder is just a repo-backed folder).
path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
print(f"This notebook lives at: {path}")

# COMMAND ----------

# MAGIC %md ✅ **Done.** Next: **A4 — Secrets**.
