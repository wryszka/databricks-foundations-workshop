# Databricks notebook source
# MAGIC %md
# MAGIC # I2 — MLOps taster: a claim-frequency GLM
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for (optional / stretch):** the platform tracks models, not just
# MAGIC tables. You fit a simple **Generalized Linear Model (GLM)** for claim frequency
# MAGIC (a Poisson regression), track the run with **MLflow**, and register a governed model
# MAGIC version in Unity Catalog with a `@champion` alias.
# MAGIC
# MAGIC Fill in each `TODO`. Solution: `solutions/26_solution_i2_mlops_glm`.
# MAGIC
# MAGIC > 💡 **Genie Code:** you can prompt Genie Code to write the training code for you —
# MAGIC > "fit a Poisson GLM for claim_count and register it to MLflow" — then refine it.
# MAGIC
# MAGIC > ⚠️ **Serverless environment:** pick a **recent environment version** (top-right
# MAGIC > *Environment* panel — v3 or newer), which ships `mlflow` and `scikit-learn`. Very
# MAGIC > old versions fail with `No module named 'mlflow'`.

# COMMAND ----------

# MAGIC %run ../00_setup/00_config

# COMMAND ----------

# MAGIC %md ## 1. Build the modelling dataset (given)

# COMMAND ----------

from pyspark.sql import functions as F

policies = spark.table("2_silver_policies")
claim_counts = (spark.table("2_silver_claims")
                .groupBy("policy_id").agg(F.count("*").alias("claim_count")))
model_df = (policies.join(claim_counts, "policy_id", "left")
            .fillna({"claim_count": 0})
            .select("driver_age", "engine_cc", "penalty_points", "ncd_years",
                    "cover_type", "region", "claim_count"))
pdf = model_df.toPandas()
print(f"rows: {len(pdf):,} | overall frequency: {pdf['claim_count'].mean():.3f}")

# COMMAND ----------

# MAGIC %md ## 2. Fit the GLM and track it with MLflow
# MAGIC Complete the `start_run` block: fit the pipeline, log a metric, and log+register the
# MAGIC model with `registered_model_name=MODEL_NAME`.

# COMMAND ----------

import mlflow
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import PoissonRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from mlflow.models.signature import infer_signature

mlflow.set_registry_uri("databricks-uc")

num_cols = ["driver_age", "engine_cc", "penalty_points", "ncd_years"]
cat_cols = ["cover_type", "region"]
X = pdf[num_cols + cat_cols]
y = pdf["claim_count"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

pipe = Pipeline([
    ("prep", ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ], remainder="passthrough")),
    ("glm", PoissonRegressor(alpha=1e-3, max_iter=300)),
])

with mlflow.start_run(run_name="frequency_glm") as run:
    # TODO: pipe.fit(X_train, y_train)
    # TODO: compute mae = mean_absolute_error(y_test, pipe.predict(X_test)) and mlflow.log_metric(...)
    # TODO: info = mlflow.sklearn.log_model(pipe, artifact_path="model",
    #                signature=infer_signature(X_test, pipe.predict(X_test)),
    #                registered_model_name=MODEL_NAME)
    pass

# COMMAND ----------

# MAGIC %md ## 3. Mark the new version as champion
# MAGIC Use `MlflowClient(registry_uri="databricks-uc").set_registered_model_alias(MODEL_NAME, "champion", info.registered_model_version)`.

# COMMAND ----------

from mlflow import MlflowClient
# TODO: set the @champion alias on the version you just registered

# COMMAND ----------

# MAGIC %md ## 4. Load the champion and score a few policies
# MAGIC `mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@champion")`, then `.predict(X_test.head(5))`.

# COMMAND ----------

# TODO: load the champion model and score the first 5 rows of X_test

# COMMAND ----------

# MAGIC %md ✅ **Done** once a `@champion` version is registered and scores rows. Optional deep-dive complete.
