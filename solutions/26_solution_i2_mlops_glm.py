# Databricks notebook source
# MAGIC %md
# MAGIC # I2 — MLOps taster: a claim-frequency GLM (solution)
# MAGIC
# MAGIC **About this workshop:** all data is synthetic; every company named is fictional.
# MAGIC
# MAGIC **What is this for (optional / stretch):** the platform is not just tables — it tracks
# MAGIC models too. We fit a simple **Generalized Linear Model (GLM)** for claim frequency
# MAGIC (a Poisson regression, the classic actuarial model), track the run with **MLflow**,
# MAGIC and register a governed model version in Unity Catalog with a `@champion` alias.
# MAGIC
# MAGIC > 💡 **Genie Code:** instead of writing the training code, you can prompt Genie Code —
# MAGIC > "fit a Poisson GLM for claim_count on driver_age, engine_cc, penalty_points,
# MAGIC > ncd_years, cover_type and region, log it to MLflow and register it" — and refine
# MAGIC > what it produces.
# MAGIC
# MAGIC > ⚠️ **Serverless environment:** pick a **recent environment version** (top-right
# MAGIC > *Environment* panel — v3 or newer). Recent versions ship `mlflow` and
# MAGIC > `scikit-learn`; very old ones do not and this lab will fail with
# MAGIC > `No module named 'mlflow'`.

# COMMAND ----------

# MAGIC %run ../notebooks/00_config

# COMMAND ----------

# MAGIC %md ## 1. Build the modelling dataset
# MAGIC One row per policy, with a `claim_count` target joined from the claims table.

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

# COMMAND ----------

import mlflow
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import PoissonRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_poisson_deviance, mean_absolute_error
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
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    dev = mean_poisson_deviance(y_test, preds.clip(min=1e-6))
    mlflow.log_params({"model": "PoissonRegressor", "alpha": 1e-3,
                       "num_cols": ",".join(num_cols), "cat_cols": ",".join(cat_cols)})
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("poisson_deviance", dev)
    info = mlflow.sklearn.log_model(
        pipe, artifact_path="model",
        signature=infer_signature(X_test, preds),
        input_example=X_test.head(3),
        registered_model_name=MODEL_NAME,
    )
    print(f"run_id={run.info.run_id}  mae={mae:.4f}  poisson_deviance={dev:.4f}")

# COMMAND ----------

# MAGIC %md ## 3. Register the version and mark it champion

# COMMAND ----------

from mlflow import MlflowClient

client = MlflowClient(registry_uri="databricks-uc")
version = info.registered_model_version
client.set_registered_model_alias(MODEL_NAME, "champion", version)
print(f"registered {MODEL_NAME} version {version} as @champion")

# COMMAND ----------

# MAGIC %md ## 4. Load the champion and score a few policies

# COMMAND ----------

champion = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@champion")
scored = X_test.head(5).copy()
scored["expected_frequency"] = champion.predict(X_test.head(5)).round(3)
display(scored)

# COMMAND ----------

# MAGIC %md
# MAGIC ✅ **Done.** You trained a GLM, tracked it in MLflow, and registered a governed,
# MAGIC aliased model version in Unity Catalog — the core MLOps loop. That is the optional
# MAGIC deep-dive complete.
