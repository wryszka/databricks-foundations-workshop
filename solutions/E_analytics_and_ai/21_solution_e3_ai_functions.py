# Databricks notebook source
# MAGIC %md
# MAGIC # E3 — AI functions in SQL (solution)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for:** real AI is a *SQL function call* away on Keystone — no model
# MAGIC endpoints to deploy, no Python. We classify, score sentiment, mask, extract and
# MAGIC summarise straight over the tenants' data, exactly where a pipeline would.

# COMMAND ----------

# MAGIC %run ../../notebooks/00_setup/00_config

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Sentiment on free-text complaint notes
# MAGIC `ai_analyze_sentiment(text)` returns positive / negative / neutral / mixed.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT tenant, claim_id, note,
# MAGIC        ai_analyze_sentiment(note) AS sentiment
# MAGIC FROM 2_silver_complaints
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Classify a claim's severity
# MAGIC `ai_classify(text, array_of_labels)` picks the best-fitting label. We hand it a short
# MAGIC description built from the structured columns.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT claim_id, claim_type, incurred_amount, status,
# MAGIC        ai_classify(
# MAGIC          concat('A ', claim_type, ' motor claim with incurred amount EUR ',
# MAGIC                 cast(incurred_amount AS string), ' and status ', status),
# MAGIC          array('minor', 'moderate', 'severe')
# MAGIC        ) AS severity
# MAGIC FROM 2_silver_claims
# MAGIC WHERE incurred_amount >= 0
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Mask personal data in a note
# MAGIC `ai_mask(text, array_of_things_to_mask)` redacts the entities you name.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT note,
# MAGIC        ai_mask(note, array('person', 'email', 'phone number')) AS masked_note
# MAGIC FROM 2_silver_complaints
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Extract and summarise a claim document
# MAGIC The `docs` volume holds claim documents as text. We read them, then `ai_extract`
# MAGIC pulls named fields and `ai_summarize` gives a short summary — all in SQL.

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
# MAGIC SELECT
# MAGIC   substring_index(path, '/', -1) AS file,
# MAGIC   ai_extract(value, array('claim reference', 'policy reference', 'date of loss',
# MAGIC                           'claim type', 'reserve estimate')) AS extracted,
# MAGIC   ai_summarize(value, 40) AS summary
# MAGIC FROM claim_docs
# MAGIC LIMIT 5;

# COMMAND ----------

# MAGIC %md
# MAGIC > 💡 **Genie Code:** you could prompt Genie Code — "score the sentiment of every
# MAGIC > complaint note and count negatives by tenant" — and it will write this SQL for you.
# MAGIC
# MAGIC ✅ **Done.** You called five AI functions without leaving SQL. Next: `F1` (share a
# MAGIC table with another attendee) or the optional `I1` LLM primer.
