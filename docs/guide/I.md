## I. Optional Deep Dives

Two extra labs for anyone who is curious or finishes early. Neither is required to complete
the workshop. The first shows you that large language models (the technology behind chat
assistants) live right inside the platform; the second is a taster of machine learning —
training a small predictive model and tracking it properly.

### I1. LLM primer — the AI Playground and foundation models

**What this is.** A short, no-pressure tour of the fact that **large language models (LLMs)
are built into the platform** — nothing to install, no key to manage. You'll chat with a
model in the AI Playground, then call the same model from SQL. ("Foundation models" is
Databricks' name for the ready-to-use LLMs it hosts.)

**Where in Databricks.** The **AI Playground** (left sidebar, usually under **Machine
Learning → Playground**) for chatting; the notebook `notebooks/I_optional_deep_dives/25_lab_i1_llm_playground`
(open from **Workspace**) for calling a model from code.

**Steps.**
1. In the **left sidebar**, open **Machine Learning → Playground** (the **AI Playground**).
2. At the **top of the Playground** there is a **model dropdown**. Open it — this is the
   list of models *your* workspace can use. **Note what's there**, because the list varies
   (see the warning below). Pick one, type a prompt like *"In two sentences, explain what a
   no-claims discount is,"* and read the reply. This is a safe place to try prompts before
   putting them into SQL or code.
3. Now call a model from code. Open `notebooks/I_optional_deep_dives/25_lab_i1_llm_playground` and attach
   **Serverless** compute.
4. Look at the `LLM_ENDPOINT` line near the top. It is set to `databricks-gpt-oss-120b`, an
   open-weight model that is commonly available. **If that name was *not* in your Playground
   dropdown, change `LLM_ENDPOINT` to one that was.**
5. Fill the `# TODO` in the first `ai_query` cell — put a prompt string where the empty
   quotes are, for example:
   `'You are helping an insurer. In two sentences, explain what a no-claims discount is.'`
   `ai_query(endpoint, prompt)` sends your prompt to the model and returns its answer. Run
   the cell and read the printed answer.
6. Run the next cell (given). It runs the model across a **column** of data — writing a
   one-line friendly summary for five sample policies — to show that because it's just a
   function, you can apply a model to a whole table.

**You should see.** A chat reply in the Playground, then a printed answer from `ai_query`,
then a small table of five policies each with an AI-written `blurb`.

> ⚠️ **Free Edition model availability.** On Free Edition the catalogue of models is
> limited, there is no graphics-processor (GPU) serving and no provisioned throughput, and
> exactly which models are enabled varies by region. **Always open the Playground dropdown
> to see what your workspace actually has, and set `LLM_ENDPOINT` to one of those names.**
> `databricks-gpt-oss-120b` is known to work with `ai_query`.

**💡 Genie Code vs the Playground.** The Playground is for *chatting* with a model; **Genie
Code** is for *building* — it writes notebook and SQL code for you from a prompt. Both live
in the same workspace.

### I2. MLOps taster — a claim-frequency model

**What this is.** A gentle introduction to machine learning on the platform. You'll train a
simple **Generalized Linear Model (GLM)** — the classic model actuaries use — to predict how
often a policy will have a claim, record the experiment with **MLflow** (the built-in tool
for tracking models), and register a governed, named version of the model so it can be
reused and audited.

**Where in Databricks.** The notebook `notebooks/I_optional_deep_dives/26_lab_i2_mlops_glm` (open from
**Workspace**).

> ⚠️ **Pick a recent serverless environment first.** This lab uses the `mlflow` and
> `scikit-learn` libraries, which only ship with a **recent environment version**. Before
> running, open the **Environment** panel (top-right of the notebook) and select the latest
> version. On a very old/default environment this lab fails with `No module named 'mlflow'`.

**Steps.**
1. Open `notebooks/I_optional_deep_dives/26_lab_i2_mlops_glm`, attach **Serverless** compute, and select a recent
   **Environment** version (see the warning above).
2. **Section 1 (given)** — run it. It builds the training table: one row per policy with a
   `claim_count` (how many claims that policy had) joined on, and prints the overall claim
   frequency.
3. **Section 2 — fit and track the model.** The setup (imports, train/test split, and the
   model "pipeline") is given. Fill the three `# TODO` lines inside the `with
   mlflow.start_run(...)` block:
   - `pipe.fit(X_train, y_train)` — trains the model.
   - compute the error and log it:
     `mae = mean_absolute_error(y_test, pipe.predict(X_test))` then
     `mlflow.log_metric("mae", mae)`.
   - log and register the trained model:
     ```
     info = mlflow.sklearn.log_model(pipe, artifact_path="model",
              signature=infer_signature(X_test, pipe.predict(X_test)),
              registered_model_name=MODEL_NAME)
     ```
     `MODEL_NAME` comes from `00_config`. Run the cell — this records the run in MLflow and
     saves a versioned model in Unity Catalog (the governance layer).
4. **Section 3 — mark it "champion."** Fill the `# TODO` to tag the new version as the
   current best:
   `MlflowClient(registry_uri="databricks-uc").set_registered_model_alias(MODEL_NAME, "champion", info.registered_model_version)`.
   An *alias* like `@champion` is a friendly pointer to a specific version, so downstream
   code doesn't hard-code a number.
5. **Section 4 — use the model.** Fill the `# TODO` to load the champion and score a few
   rows:
   `champion = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@champion")`, then predict on
   `X_test.head(5)`. Run it.

**You should see.** A printed run id with an error metric (`mae`), a message confirming the
version was registered as `@champion`, and a small table of five policies each with an
`expected_frequency` prediction. You can also open **Machine Learning → Experiments** in the
left sidebar to see the logged run.

**💡 Genie Code.** You can prompt Genie Code — "fit a Poisson GLM for claim_count on
driver_age, engine_cc, penalty_points, ncd_years, cover_type and region, log it to MLflow
and register it" — and refine what it generates instead of filling the TODOs by hand.
