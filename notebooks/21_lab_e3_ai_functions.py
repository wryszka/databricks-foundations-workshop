# Databricks notebook source
# MAGIC %md
# MAGIC # E3 — AI functions in SQL
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** real AI is a *SQL function call* away on Keystone — no model
# MAGIC endpoints to deploy, no Python. In this lab you classify, score sentiment, mask,
# MAGIC extract and summarise straight over the tenants' data.
# MAGIC
# MAGIC Fill in each `TODO`. The solution is in `solutions/21_solution_e3_ai_functions`.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Sentiment on free-text complaint notes
# MAGIC Use `ai_analyze_sentiment(<column>)` on the `note` column of `2_silver_complaints`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT tenant, claim_id, note,
# MAGIC        -- TODO: add a column `sentiment` using ai_analyze_sentiment(note)
# MAGIC        note AS todo_replace_me
# MAGIC FROM 2_silver_complaints
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Classify a claim's severity
# MAGIC `ai_classify(text, array('minor','moderate','severe'))`. Build `text` from the
# MAGIC structured columns with `concat(...)`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT claim_id, claim_type, incurred_amount, status
# MAGIC        -- TODO: add a column `severity` using ai_classify(...) over a description
# MAGIC FROM 2_silver_claims
# MAGIC WHERE incurred_amount >= 0
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Mask personal data in a note
# MAGIC `ai_mask(note, array('person','email','phone number'))`.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT note
# MAGIC        -- TODO: add a column `masked_note` using ai_mask(...)
# MAGIC FROM 2_silver_complaints
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Extract and summarise a claim document
# MAGIC First read the text documents from the `docs` volume into a temp view (given), then
# MAGIC use `ai_extract` and `ai_summarize` in SQL.

# COMMAND ----------

from pyspark.sql import functions as F

docs = (
    spark.read.option("wholetext", "true").text(DOCS_VOLUME)
    .withColumn("path", F.col("_metadata.file_path"))
)
docs.createOrReplaceTempView("claim_docs")
print(f"loaded {docs.count()} claim documents from {DOCS_VOLUME}")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT substring_index(path, '/', -1) AS file
# MAGIC        -- TODO: add `extracted` via ai_extract(value, array('claim reference', ...))
# MAGIC        -- TODO: add `summary`   via ai_summarize(value, 40)
# MAGIC FROM claim_docs
# MAGIC LIMIT 5;

# COMMAND ----------

# MAGIC %md
# MAGIC > 💡 **Genie Code:** you could prompt Genie Code — "score the sentiment of every
# MAGIC > complaint note and count negatives by tenant" — and it will write this SQL for you.
# MAGIC
# MAGIC ✅ **Done** once all four queries return AI-generated columns. Next: `F1` or `I1`.
