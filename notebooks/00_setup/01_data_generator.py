# Databricks notebook source
# MAGIC %md
# MAGIC # 01 — Data generator: the Keystone multi-tenant book
# MAGIC
# MAGIC Generates a synthetic **multi-tenant** insurance book (three fictional client
# MAGIC insurers) with **real signal** — younger drivers, penalty points, bigger engines and
# MAGIC higher-risk areas genuinely drive claims and premium — then writes everything the
# MAGIC labs need:
# MAGIC
# MAGIC - **Messy motor CSVs** (`policies.csv`, `claims.csv`) into the `raw` volume — Track B/D clean these
# MAGIC - **An Auto Loader batch**: `landing/claims/claims_batch_01.csv` already landed, plus
# MAGIC   `raw/claims_batch_02.csv` waiting for you to drop in during lab B2
# MAGIC - **`2_silver_complaints`** — free-text complaint notes (for the AI-functions lab E3)
# MAGIC - **`2_silver_property_policies`** — a small, clean second line of business (property)
# MAGIC - **Claim documents** as text files in the `docs` volume (for `ai_extract` / `ai_summarize`)
# MAGIC - Optionally (`build_all = yes`) the silver + gold motor tables the pipeline labs build —
# MAGIC   use this for an instructor-led run, or so people who jump ahead have tables to query
# MAGIC
# MAGIC Every row carries a **`tenant`** column, which is what powers the isolation, security
# MAGIC and sharing labs. Idempotent and seeded: rerunning rebuilds identical data.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

dbutils.widgets.dropdown("build_all", "no", ["no", "yes"], "Also build silver/gold (skip Track B/D)")
BUILD_ALL = dbutils.widgets.get("build_all") == "yes"

N_POLICIES = 30_000   # motor, across all tenants
N_PROPERTY = 6_000    # property line
SEED = 42

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Tenants carry different sizes and baseline risk, so cross-tenant comparisons are interesting.
tenants = [  # (tenant, share_of_book, risk_multiplier)
    ("bricksurance_se", 0.50, 1.00),
    ("northwind_mutual", 0.32, 1.12),
    ("helios_re", 0.18, 0.90),
]
regions = [  # (region, weight, risk_factor) — generic, not tied to any real geography
    ("Metro North", 0.28, 1.25), ("Metro South", 0.14, 1.10), ("Coastal", 0.12, 1.05),
    ("Central", 0.12, 1.00), ("Highland", 0.09, 0.92), ("Lakes", 0.09, 0.95),
    ("Border", 0.08, 0.98), ("Western", 0.08, 0.90),
]
makes = ["Toyota", "Volkswagen", "Hyundai", "Ford", "Skoda", "Kia", "Nissan", "BMW", "Audi", "Dacia"]

def weighted_case(col, items):
    """CASE expression picking from (value, weight, ...) tuples using a uniform [0,1) column."""
    expr, cum = "CASE", 0.0
    for val, w, *_ in items:
        cum += w
        expr += f" WHEN {col} < {cum:.4f} THEN '{val}'"
    return expr + f" ELSE '{items[-1][0]}' END"

region_risk = "CASE " + " ".join(f"WHEN region = '{r}' THEN {rf}" for r, w, rf in regions) + " ELSE 1.0 END"
tenant_risk = "CASE " + " ".join(f"WHEN tenant = '{t}' THEN {m}" for t, s, m in tenants) + " ELSE 1.0 END"

# COMMAND ----------

# MAGIC %md ## Motor policies — premium and claim probability share the same drivers

# COMMAND ----------

pol = (
    spark.range(N_POLICIES)
    .withColumn("policy_id", F.format_string("POL-%07d", F.col("id")))
    .withColumn("t", F.rand(SEED))
    .withColumn("tenant", F.expr(weighted_case("t", tenants)))
    .withColumn("u1", F.rand(SEED + 1)).withColumn("u2", F.rand(SEED + 2))
    .withColumn("u3", F.rand(SEED + 3)).withColumn("u4", F.rand(SEED + 4))
    .withColumn("u5", F.rand(SEED + 5)).withColumn("u6", F.rand(SEED + 6))
    .withColumn("region", F.expr(weighted_case("u1", regions)))
    .withColumn("driver_age", (18 + F.pow(F.col("u2"), 0.9) * 60).cast("int"))
    .withColumn("ncd_years", F.least(F.floor(F.col("u3") * 10), F.lit(9)).cast("int"))
    .withColumn("penalty_points", F.floor(F.pow(F.col("u4"), 3) * 9).cast("int"))
    .withColumn("vehicle_make", F.expr(f"element_at(array({','.join(repr(m) for m in makes)}), cast(u5 * {len(makes)} as int) + 1)"))
    .withColumn("engine_cc", (1000 + F.floor(F.col("u6") * 15) * 100).cast("int"))
    .withColumn("cover_type", F.expr("CASE WHEN u6 < 0.70 THEN 'comprehensive' WHEN u6 < 0.90 THEN 'tpft' ELSE 'tpo' END"))
    .withColumn("start_date", F.date_sub(F.current_date(), (F.rand(SEED + 7) * 730).cast("int")))
    .withColumn("age_factor", F.expr("CASE WHEN driver_age < 25 THEN 1.8 WHEN driver_age < 30 THEN 1.3 WHEN driver_age >= 70 THEN 1.2 ELSE 1.0 END"))
    .withColumn("region_factor", F.expr(region_risk))
    .withColumn("tenant_factor", F.expr(tenant_risk))
    .withColumn(
        "annual_premium",
        F.round(
            F.lit(380) * F.col("age_factor") * F.col("region_factor") * F.col("tenant_factor")
            * (1 + F.col("penalty_points") * 0.05)
            * (1 - F.least(F.col("ncd_years"), F.lit(5)) * 0.05)
            * (1 + (F.col("engine_cc") - 1000) / 8000)
            * F.expr("CASE cover_type WHEN 'comprehensive' THEN 1.0 WHEN 'tpft' THEN 0.85 ELSE 0.75 END")
            * (0.9 + F.rand(SEED + 8) * 0.2),
            2,
        ),
    )
    .withColumn(
        "claim_prob",
        F.lit(0.045) * F.col("age_factor") * F.col("region_factor") * F.col("tenant_factor")
        * (1 + F.col("penalty_points") * 0.12)
        * (1 - F.least(F.col("ncd_years"), F.lit(5)) * 0.04)
        * (1 + (F.col("engine_cc") - 1000) / 6000),
    )
    .withColumn("has_claim", F.rand(SEED + 9) < F.col("claim_prob"))
    .select(
        "policy_id", "tenant", "region", "driver_age", "ncd_years", "penalty_points",
        "vehicle_make", "engine_cc", "cover_type", "start_date", "annual_premium", "has_claim",
    )
)
print(f"motor policies: {pol.count():,}  |  overall claim frequency: {pol.filter('has_claim').count() / N_POLICIES:.1%}")

# COMMAND ----------

# MAGIC %md ## Motor claims — type mix and severities that look like a real book

# COMMAND ----------

claim_types = [("windscreen", 0.40), ("damage", 0.35), ("theft", 0.10), ("injury", 0.15)]

claims = (
    pol.filter("has_claim")
    .withColumn("u", F.rand(SEED + 10))
    .withColumn("claim_seq", F.row_number().over(Window.orderBy("policy_id")))
    .withColumn("claim_id", F.format_string("CLM-%07d", F.col("claim_seq")))
    .withColumn("claim_type", F.expr(weighted_case("u", claim_types)))
    .withColumn("claim_date", F.date_add(F.col("start_date"), (F.rand(SEED + 11) * 330).cast("int") + 15))
    .withColumn("sev_u", F.rand(SEED + 12))
    .withColumn(
        "incurred_amount",
        F.round(
            F.expr("""
                CASE claim_type
                    WHEN 'windscreen' THEN 250 + sev_u * 550
                    WHEN 'damage'     THEN 800 + pow(sev_u, 2) * 9000
                    WHEN 'theft'      THEN 3000 + sev_u * 15000
                    WHEN 'injury'     THEN 8000 + pow(sev_u, 2) * 90000
                END
            """),
            2,
        ),
    )
    .withColumn("status", F.expr("CASE WHEN sev_u < 0.75 THEN 'settled' WHEN sev_u < 0.92 THEN 'open' ELSE 'in_review' END"))
    .select("claim_id", "policy_id", "tenant", "claim_type", "claim_date", "incurred_amount", "status")
)
print(f"motor claims: {claims.count():,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Messy raw CSVs for Track B / D
# MAGIC Planted problems the pipeline must handle:
# MAGIC - ~1.5% duplicated policy rows
# MAGIC - ~1% of `start_date` corrupted to `31/02/2025`
# MAGIC - ~0.5% negative `annual_premium`
# MAGIC - some claims with `incurred_amount` = `-1` (unset placeholder from the "legacy system")

# COMMAND ----------

pol_raw = pol.drop("has_claim")
dupes = pol_raw.sample(fraction=0.015, seed=SEED)
pol_messy = (
    pol_raw.unionAll(dupes)
    .withColumn("corrupt", F.rand(SEED + 13))
    .withColumn("start_date", F.expr("CASE WHEN corrupt < 0.01 THEN '31/02/2025' ELSE cast(start_date as string) END"))
    .withColumn("annual_premium", F.expr("CASE WHEN corrupt > 0.995 THEN -annual_premium ELSE annual_premium END"))
    .drop("corrupt")
)
claims_messy = claims.withColumn(
    "incurred_amount", F.expr(f"CASE WHEN rand({SEED + 14}) < 0.01 THEN -1 ELSE incurred_amount END")
)

pol_messy.toPandas().to_csv(f"{RAW_VOLUME}/policies.csv", index=False)
claims_messy.toPandas().to_csv(f"{RAW_VOLUME}/claims.csv", index=False)
print(f"wrote messy CSVs to {RAW_VOLUME}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## An Auto Loader batch (lab B2)
# MAGIC A fresh set of "newly reported" claims, split into two files. The first has already
# MAGIC landed in `landing/claims/`; the second waits in the `raw` volume for you to drop into
# MAGIC the landing folder mid-lab and watch Auto Loader pick up **only the new file**.

# COMMAND ----------

dbutils.fs.mkdirs(f"{LANDING_VOLUME}/claims")

incremental = (
    pol.filter("has_claim").limit(2000)
    .withColumn("claim_seq", F.row_number().over(Window.orderBy(F.desc("policy_id"))))
    .withColumn("claim_id", F.format_string("CLM-9%06d", F.col("claim_seq")))
    .withColumn("claim_type", F.expr(weighted_case(f"rand({SEED + 15})", claim_types)))
    .withColumn("claim_date", F.current_date())
    .withColumn("incurred_amount", F.round(300 + F.rand(SEED + 16) * 12000, 2))
    .withColumn("status", F.lit("open"))
    .select("claim_id", "policy_id", "tenant", "claim_type", "claim_date", "incurred_amount", "status")
)
inc = incremental.toPandas()
half = len(inc) // 2
inc.iloc[:half].to_csv(f"{LANDING_VOLUME}/claims/claims_batch_01.csv", index=False)
inc.iloc[half:].to_csv(f"{RAW_VOLUME}/claims_batch_02.csv", index=False)
print(f"landed claims_batch_01.csv ({half} rows) in {LANDING_VOLUME}/claims/")
print(f"staged claims_batch_02.csv ({len(inc) - half} rows) in {RAW_VOLUME} (you drop it in during lab B2)")

# COMMAND ----------

# MAGIC %md ## Free-text complaint notes (lab E3 — AI functions)

# COMMAND ----------

# Sentiment lives in the wording, so ai_analyze_sentiment has something real to find.
neg = [
    "Absolutely appalling service, three weeks and still no callback about my claim.",
    "I am furious. The assessor never showed up and no one answers the phone.",
    "Worst experience ever, my payout was slashed with no explanation.",
    "Completely unacceptable delays, I am considering leaving after ten years.",
]
neu = [
    "Following up on claim status, please advise expected timeline.",
    "Requesting a copy of my policy schedule for my records.",
    "Can you confirm whether the windscreen repair is covered under my cover type?",
    "Please update my contact number on the policy.",
]
pos = [
    "Really impressed, the claim was settled within two days, thank you.",
    "The agent was extremely helpful and explained everything clearly.",
    "Fantastic service, quick payout and friendly staff throughout.",
    "Very happy with how smoothly the whole process went.",
]
notes_expr = (
    "CASE WHEN s < 0.45 THEN element_at(array(" + ",".join(repr(x) for x in neg) + f"), cast(rand({SEED+18})*{len(neg)} as int)+1) "
    "WHEN s < 0.75 THEN element_at(array(" + ",".join(repr(x) for x in neu) + f"), cast(rand({SEED+19})*{len(neu)} as int)+1) "
    "ELSE element_at(array(" + ",".join(repr(x) for x in pos) + f"), cast(rand({SEED+20})*{len(pos)} as int)+1) END"
)
complaints = (
    claims.select("claim_id", "policy_id", "tenant")
    .withColumn("s", F.rand(SEED + 17))
    .withColumn("received_date", F.current_date())
    .withColumn("note", F.expr(notes_expr))
    .drop("s")
    .sample(fraction=0.25, seed=SEED)
)
complaints.write.mode("overwrite").saveAsTable("2_silver_complaints")
print(f"2_silver_complaints: {complaints.count():,} rows")

# COMMAND ----------

# MAGIC %md ## Claim documents as text files (lab E3 — ai_extract / ai_summarize)

# COMMAND ----------

import os
os.makedirs(DOCS_VOLUME, exist_ok=True)
doc_rows = claims.limit(15).collect()
tmpl = (
    "KEYSTONE CLAIMS — FIRST NOTIFICATION OF LOSS\n"
    "Claim reference: {claim_id}\n"
    "Policy reference: {policy_id}\n"
    "Insurer: {tenant}\n"
    "Date of loss: {claim_date}\n"
    "Claim type: {claim_type}\n"
    "Reserve estimate: EUR {incurred_amount}\n\n"
    "Description of incident:\n"
    "The policyholder reported a {claim_type} incident on {claim_date}. An assessor has "
    "been assigned and the current reserve estimate is EUR {incurred_amount}. Status of "
    "the claim is '{status}'. Further documentation has been requested from the "
    "policyholder to progress settlement.\n"
)
for r in doc_rows:
    with open(f"{DOCS_VOLUME}/claim_{r['claim_id']}.txt", "w") as fh:
        fh.write(tmpl.format(**r.asDict()))
print(f"wrote {len(doc_rows)} claim documents to {DOCS_VOLUME}")

# COMMAND ----------

# MAGIC %md ## Property — a small, clean second line of business

# COMMAND ----------

property_pol = (
    spark.range(N_PROPERTY)
    .withColumn("property_policy_id", F.format_string("PRP-%07d", F.col("id")))
    .withColumn("t", F.rand(SEED + 40))
    .withColumn("tenant", F.expr(weighted_case("t", tenants)))
    .withColumn("region", F.expr(weighted_case(f"rand({SEED + 41})", regions)))
    .withColumn("construction_year", (1900 + F.floor(F.rand(SEED + 42) * 125)).cast("int"))
    .withColumn("sum_insured", F.round(120_000 + F.rand(SEED + 43) * 680_000, 0))
    .withColumn("flood_zone", F.expr(f"CASE WHEN rand({SEED + 44}) < 0.15 THEN true ELSE false END"))
    .withColumn(
        "annual_premium",
        F.round(
            F.col("sum_insured") * 0.0025
            * F.expr(region_risk)
            * F.expr("CASE WHEN flood_zone THEN 1.6 ELSE 1.0 END")
            * (0.9 + F.rand(SEED + 45) * 0.2),
            2,
        ),
    )
    .select("property_policy_id", "tenant", "region", "construction_year", "sum_insured", "flood_zone", "annual_premium")
)
property_pol.write.mode("overwrite").saveAsTable("2_silver_property_policies")
print(f"2_silver_property_policies: {property_pol.count():,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Optional: build the silver + gold motor tables (instructor / catch-up mode)
# MAGIC With `build_all = yes`, produces the clean silver and gold tables that Track B/D
# MAGIC build, so anyone jumping ahead to governance, analytics, sharing or the app has
# MAGIC real tables to work on.

# COMMAND ----------

if BUILD_ALL:
    # silver motor policies (typed, deduped, bad rows dropped)
    (pol.drop("has_claim")
        .dropDuplicates(["policy_id"])
        .filter("annual_premium > 0")
        .write.mode("overwrite").saveAsTable("2_silver_policies"))
    (claims.filter("incurred_amount >= 0")
        .write.mode("overwrite").saveAsTable("2_silver_claims"))

    # gold: portfolio summary and monthly loss ratio, per tenant
    spark.sql("""
        CREATE OR REPLACE TABLE 3_gold_portfolio_summary AS
        SELECT p.tenant, p.region, p.cover_type,
               count(*)                         AS policies,
               round(sum(p.annual_premium), 2)  AS gwp,
               count(c.claim_id)                AS claims,
               round(count(c.claim_id) / count(*), 4) AS claim_frequency,
               round(coalesce(sum(c.incurred_amount), 0), 2) AS incurred
        FROM 2_silver_policies p
        LEFT JOIN 2_silver_claims c ON p.policy_id = c.policy_id
        GROUP BY p.tenant, p.region, p.cover_type
    """)
    spark.sql("""
        CREATE OR REPLACE TABLE 3_gold_loss_ratio_monthly AS
        SELECT c.tenant, date_trunc('month', c.claim_date) AS month,
               round(sum(c.incurred_amount), 2) AS incurred,
               count(*)                          AS claims
        FROM 2_silver_claims c
        GROUP BY c.tenant, date_trunc('month', c.claim_date)
    """)
    print("built 2_silver_policies, 2_silver_claims, 3_gold_portfolio_summary, 3_gold_loss_ratio_monthly")
else:
    print("build_all = no — Track B/D attendees build silver/gold themselves")

# COMMAND ----------

# MAGIC %md ## Unity Catalog tour entities (used by lab C0)

# COMMAND ----------

# Small example objects the UC concepts tour (lab C0) walks through — seeded here so they
# exist in the schema even before anyone runs the tour.
spark.sql(f"""
    CREATE OR REPLACE TABLE {FQ}.uc_tour_regions (
        region STRING, risk_factor DOUBLE COMMENT 'relative claim risk vs average')
""")
spark.sql(f"""INSERT OVERWRITE {FQ}.uc_tour_regions VALUES
    ('Metro North',1.25),('Metro South',1.10),('Coastal',1.05),('Central',1.00),
    ('Highland',0.92),('Lakes',0.95),('Border',0.98),('Western',0.90)""")
spark.sql(f"""
    CREATE OR REPLACE FUNCTION {FQ}.premium_band(p DOUBLE) RETURNS STRING
    COMMENT 'Bucket an annual premium into low/medium/high'
    RETURN CASE WHEN p < 400 THEN 'low' WHEN p < 700 THEN 'medium' ELSE 'high' END
""")
print("created uc_tour_regions table + premium_band function")

# COMMAND ----------

# MAGIC %md ✅ **Done.** Data is ready. Start with lab `A1`.
