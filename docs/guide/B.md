## B. Bring in a Data Source

This track is about getting data *into* the platform and cleaning it up — the everyday
job of onboarding a customer's data. You'll load a deliberately messy file by hand, then
set up a folder that ingests new files automatically as they arrive, then learn the
standard way to apply a batch of changes (updates and inserts) and read back exactly what
changed.

Words we'll use: **bronze/silver/gold** are the common names for data layers — bronze is
the raw file landed as-is, silver is cleaned and typed, gold is the business-ready summary;
a **volume** is a folder for files inside the Catalog; **CSV** is Comma-Separated Values, a
plain-text table format.

---

### B1. File upload to a Delta table

**What this is.** Onboarding a new client's extract. A messy CSV has arrived; you land it
unchanged (bronze), then produce a clean, correctly typed version (silver).

**Where in Databricks.** Notebook `notebooks/B_bring_a_source_in/06_lab_b1_file_upload`. The file lives in your
**raw volume**, which you can also see under **Catalog** → your catalog → schema → Volumes.

**Steps.**
1. Open the notebook and run `%run ./00_config`.
2. Run the cell that lists your `raw` volume — you'll see `policies.csv` (and a couple of
   other files). In real life you'd put a file there via **Catalog → your volume → Upload**;
   here the data generator already placed a deliberately messy one (duplicate rows, a
   corrupted date `31/02/2025`, some negative premiums).
3. **Section 1 — Bronze (land as-is).** Complete the `# TODO`: read `raw/policies.csv` with
   `header=True` and everything as text, add two lineage columns, and save it. For example:
   `bronze = (spark.read.option("header", True).csv(f"{RAW_VOLUME}/policies.csv").withColumn("_ingest_file", F.col("_metadata.file_path")).withColumn("_ingest_ts", F.current_timestamp()))`
   then `bronze.write.mode("overwrite").saveAsTable("1_bronze_policies")`. Reading as text
   means a bad date won't crash the load. Run the cell.
4. **Section 2 — Silver (clean and type).** Complete the `# TODO` to build the clean table
   from bronze: cast the number columns to their proper types; turn the bad date into
   `NULL` safely with `try_cast(start_date AS date)`; drop duplicate `policy_id` rows with
   `.dropDuplicates(["policy_id"])`; and keep only good rows with a filter like
   `start_date IS NOT NULL AND annual_premium > 0`. Save it as `2_silver_policies`. Run it.
5. Compare the row counts printed for bronze versus silver — silver is smaller because the
   duplicates and bad rows were removed.

**You should see.** `1_bronze_policies` with a few hundred more rows than expected (the
planted duplicates), and `2_silver_policies` slightly smaller and clean — every date valid,
no negative premiums.

**💡 Genie Code.** Prompt it: *"read raw/policies.csv, drop duplicates, fix the date, drop
negative premiums, save as 2_silver_policies"* and review what it writes.

---

### B2. Auto Loader — an incremental CSV pipeline

**What this is.** Files don't arrive once — they keep coming. **Auto Loader** watches a
folder and processes **only files it hasn't seen before**. You'll load one batch, drop a
second file in, and watch only the new file get picked up.

**Where in Databricks.** Notebook `notebooks/B_bring_a_source_in/07_lab_b2_autoloader`. The watched folder is
`landing/claims/` in your landing volume.

**Steps.**
1. Open the notebook and run `%run ./00_config`.
2. Run the **reset** cell. It clears any previous run's tracking files so the lab is
   repeatable, and prints what's currently in `landing/claims/` — you should see
   `claims_batch_01.csv`.
3. **Section 1 — point Auto Loader at the folder.** Complete the `run_autoloader()`
   function's `# TODO`s. The read side uses the `cloudFiles` format (that's Auto Loader):
   `stream = (spark.readStream.format("cloudFiles").option("cloudFiles.format", "csv").option("cloudFiles.schemaLocation", SCHEMA_LOC).option("header", "true").option("cloudFiles.inferColumnTypes", "true").load(f"{LANDING_VOLUME}/claims"))`.
   The write side runs once over whatever is present and stops:
   `q = (stream.writeStream.trigger(availableNow=True).option("checkpointLocation", CHK).toTable("1_bronze_incoming_claims"))` then `q.awaitTermination()`. Run the cell; it
   prints the row count after batch 1.
4. **Section 2 — a new file lands.** Run the cell that copies `claims_batch_02.csv` from the
   `raw` volume into `landing/claims/`. It lists the folder so you can see two files now.
5. **Section 3 — run again.** Run the last code cell. It runs Auto Loader a second time and
   prints the before/after counts. Only the second file's rows are added — the first file is
   remembered and skipped.

**You should see.** A row count after batch 1, then a larger count after batch 2, with a
message like `rows 1,000 -> 2,000 (only the new file's rows were added)`.

**💡 Genie Code.** Ask it for *"an Auto Loader stream that reads CSVs from this folder into
a bronze table, processing only new files"*.

---

### B3. Upserts with MERGE (and reading the changes)

**What this is.** A source keeps changing. `MERGE` applies updates to existing rows and
inserts brand-new rows **in a single statement**. With **Change Data Feed** turned on, you
can then read exactly which rows were updated versus inserted.

**Where in Databricks.** Notebook `notebooks/B_bring_a_source_in/08_lab_b3_merge_cdf`.

**Steps.**
1. Open the notebook and run `%run ./00_config`.
2. **Section 1 — a target table with Change Data Feed on.** Complete the `# TODO`: create
   `2_silver_claims_cdf` from 800 rows of `2_silver_claims`, with Change Data Feed enabled.
   The simplest way is to create it, then run
   `ALTER TABLE 2_silver_claims_cdf SET TBLPROPERTIES (delta.enableChangeDataFeed = true)`.
   Change Data Feed makes Delta record the row-level changes so you can query them later. Run it.
3. **Section 2 — prepare a batch of changes.** Just run this cell — it's pre-written. It
   builds `claim_updates`: 100 existing claims marked `settled` with a 10% higher amount,
   plus 50 brand-new claims. This stands in for "a fresh extract from the source system".
4. **Section 3 — one MERGE.** The cell first records the table's current version number.
   Complete the `# TODO` with a `MERGE`:
   `MERGE INTO 2_silver_claims_cdf t USING claim_updates s ON t.claim_id = s.claim_id WHEN MATCHED THEN UPDATE SET status = s.status, incurred_amount = s.incurred_amount WHEN NOT MATCHED THEN INSERT *`.
   Run it — the 100 matches are updated, the 50 new ones inserted.
5. **Section 4 — read exactly what changed.** Complete the `# TODO` to query the changes
   since the version you recorded, grouped by change type:
   `display(spark.sql(f"SELECT _change_type, count(*) AS rows FROM table_changes('2_silver_claims_cdf', {start_v + 1}) GROUP BY _change_type"))`. Run it.

**You should see.** The row count grow by 50 after the MERGE, and a small summary showing
the change types — around 100 `update_postimage` (and matching pre-images) plus 50 `insert`
rows.

**💡 Genie Code.** Prompt it: *"merge these updates and new claims into 2_silver_claims_cdf
on claim_id, then show me what changed using Change Data Feed"*.
