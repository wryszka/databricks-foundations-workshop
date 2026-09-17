# Databricks notebook source
# MAGIC %md
# MAGIC # I1 — LLM primer (solution)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for (optional):** many people do not realise **large language models
# MAGIC (LLMs) live right inside the platform**. There is nothing to install and no key to
# MAGIC manage. This short primer shows you where they are and how to call one.
# MAGIC
# MAGIC ### Where to find it — the AI Playground
# MAGIC In the left sidebar open **Machine Learning → Playground** (the **AI Playground**).
# MAGIC A dropdown at the top lists the models your workspace can use. Pick one, type a
# MAGIC prompt, and chat. Use it to try prompts before you put them in SQL or code.
# MAGIC
# MAGIC ### The same models are callable from SQL and code
# MAGIC That is exactly what the AI functions in lab **E3** (`ai_classify`, `ai_extract`, …)
# MAGIC use under the hood. Below we call a model directly with `ai_query`.
# MAGIC
# MAGIC > ⚠️ **Free Edition:** the catalogue of models is limited, there is **no GPU serving**
# MAGIC > and **no provisioned throughput**, and the exact models available vary by region.
# MAGIC > **Open the Playground dropdown to see what *your* workspace has**, then set
# MAGIC > `LLM_ENDPOINT` below to one of those endpoint names.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

# COMMAND ----------

# Set this to an endpoint that appears in YOUR AI Playground dropdown.
# `databricks-gpt-oss-120b` is an open-weight model commonly available.
LLM_ENDPOINT = "databricks-gpt-oss-120b"
print(f"Using foundation-model endpoint: {LLM_ENDPOINT}")

# COMMAND ----------

# MAGIC %md ## Call the model from SQL with `ai_query`

# COMMAND ----------

result = spark.sql(f"""
    SELECT ai_query('{LLM_ENDPOINT}',
      'You are helping an insurer. In two sentences, explain what a no-claims discount is.'
    ) AS answer
""")
print(result.first()["answer"])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Use it over your data
# MAGIC Because it is just a function, you can run a model across a whole column — here, a
# MAGIC one-line plain-English blurb for a sample of policies.

# COMMAND ----------

spark.sql(f"""
    SELECT policy_id, tenant, region, cover_type,
           ai_query('{LLM_ENDPOINT}',
             concat('Write a one-line, friendly summary of this motor policy: ',
                    'region ', region, ', cover ', cover_type,
                    ', annual premium EUR ', cast(annual_premium AS string))
           ) AS blurb
    FROM 2_silver_policies
    LIMIT 5
""").display()

# COMMAND ----------

# MAGIC %md
# MAGIC > 💡 **Genie Code vs the Playground:** the Playground is for *chatting* with a model;
# MAGIC > **Genie Code** is for *building* — it writes notebook and SQL code for you from a
# MAGIC > prompt. Both live in the same workspace.
# MAGIC
# MAGIC ✅ **Done.** You now know where the platform's AI lives and how to call it.
