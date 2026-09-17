## E. Analyse and Apply AI

So far you have moved and governed data. This track is about **getting answers out of it**.
You'll let people ask questions in plain English (Genie), turn one of those questions into
a shareable dashboard, and call artificial-intelligence (AI) models straight from SQL — the
"make it useful" layer that sits on top of a data product. Everything here reads the
finished `3_gold_*` and `2_silver_*` tables you created earlier, so make sure you ran
`01_data_generator` (ideally with the **build_all** widget set to `yes`).

### E1. Ask questions in plain language with Genie

**What this is.** **Genie** is a feature that lets someone ask a question about your data in
ordinary English — "which tenant has the highest claim frequency?" — and it writes and runs
the SQL (Structured Query Language, the language for querying data) for you. It is the
"let a business user ask" surface of a data product. (Its sibling, **Genie Code**, is a
different tool for *building* — it writes notebook and SQL code from a prompt. Same
workspace, different job.)

**Where in Databricks.** Mostly the **Genie** area (left sidebar). There is also a companion
notebook, `notebooks/E_analytics_and_ai/19_lab_e1_genie` (open it from the **Workspace** menu), whose optional
last cell asks Genie from code.

**Steps.**
1. In the **left sidebar**, click **Genie**. (If you don't see it, it may sit under a
   heading like *SQL* or *AI/BI* — look for the word "Genie".)
2. Click **New** (top-right) to start a new **Genie space** (a Genie space is a saved
   question-answering assistant scoped to a chosen set of tables).
3. When asked which data to include, browse to **your own schema** — it is named
   `keystone_<your-username>` inside your catalog (`main` on Free Edition) — and tick these
   tables: `3_gold_portfolio_summary`, `3_gold_loss_ratio_monthly`, `2_silver_policies`,
   `2_silver_claims`. Confirm your selection.
4. Give the space a name, for example *Keystone — Portfolio*, and click **Create**.
5. You'll land in a chat box. In the **sample questions** area (or just the chat), add and
   then ask questions such as:
   - "Which tenant has the highest claim frequency?"
   - "Show gross written premium by region for bricksurance_se."
   - "What is the monthly incurred trend this year?"
6. Ask one. Genie replies with a table or chart. Now click **Show generated code** (or the
   **SQL** toggle on the answer) to reveal the SQL Genie wrote. **Copy that SQL and keep it
   in a scratch note — you reuse it in lab E2.**
7. *(Optional, for the curious.)* Open `notebooks/E_analytics_and_ai/19_lab_e1_genie`. Copy your space's id
   from its web address — the part after `.../genie/rooms/` — and paste it into the
   **space_id** widget at the top of the notebook. Then run the last code cell to ask Genie
   the same question from Python and print both the answer and the SQL.

**You should see.** Genie answering your question with a result table/chart, and — when you
click **Show generated code** — the SQL it generated (a `SELECT ... FROM
3_gold_portfolio_summary ...`).

**💡 Genie Code.** Genie (this lab) *answers* questions; **Genie Code** *writes code*. If
you'd rather build a query in a notebook, open the Genie Code panel there and describe what
you want.

**Needs live infra.** Creating a Genie space is a click-through in the user interface, so
you do it yourself; there is nothing to run headless. Genie's availability can vary on Free
Edition — if you don't have it, watch the instructor's demo.

### E2. Build a dashboard from Genie's SQL

**What this is.** You take the SQL Genie generated in E1 (or the ready-made queries below)
and build a proper **AI/BI dashboard** — a saved, shareable report with a headline number,
a bar chart, and a trend line. This is how a one-off question becomes something a team can
open every morning.

**Where in Databricks.** The **Dashboards** area (left sidebar) for building the report; the
companion notebook `notebooks/E_analytics_and_ai/20_lab_e2_dashboard` (open from **Workspace**) to check the
numbers first.

**Steps.**
1. First, sanity-check the numbers. Open `notebooks/E_analytics_and_ai/20_lab_e2_dashboard` and attach
   **Serverless** compute (top-right), as in Part 0.
2. The first `%sql` cell (the **KPI**, or key-performance-indicator, tile) is given — run it.
   It totals gross written premium (the sum of annual premiums) and the overall claim
   frequency across all tenants.
3. Fill the two `# TODO` cells:
   - **Bar tile** — replace the placeholder query with:
     `SELECT tenant, round(sum(gwp)) AS gwp, sum(claims) AS claims FROM 3_gold_portfolio_summary GROUP BY tenant ORDER BY gwp DESC;`
     This gives premium and claim counts per tenant (per customer insurer).
   - **Line tile** — replace the placeholder with:
     `SELECT tenant, month, round(sum(incurred)) AS incurred FROM 3_gold_loss_ratio_monthly GROUP BY tenant, month ORDER BY month;`
     This is the monthly claims-cost trend per tenant.
   Run both and confirm they return rows.
4. Now build the dashboard. In the **left sidebar** click **Dashboards**, then
   **Create dashboard** (top-right).
5. Click the **Data** tab. Click **Create from SQL** / **Add a dataset**, and paste the KPI
   query from step 2. Give the dataset a name. Repeat, adding a second dataset with the bar
   query and a third with the line query. (These three queries are exactly the kind of SQL
   Genie produces — in E1 you can paste your own copied from **Show generated code**.)
6. Click the **Canvas** tab. Use **Add a widget** (or drag from the toolbar) to place:
   - a **Counter** widget bound to the KPI dataset (shows total gross written premium),
   - a **Bar** widget bound to the by-tenant dataset (tenant on one axis, premium on the
     other),
   - a **Line** widget bound to the monthly dataset (month across the bottom, incurred up
     the side, one line per tenant).
7. Click **Publish** (top-right) so the dashboard is saved and shareable.

**You should see.** A published dashboard with three panels: a big number (around
€12–13 million total gross written premium), a bar chart comparing the three tenants, and a
line chart of monthly claims cost.

**💡 Genie Code.** You can prompt Genie Code to generate a starter dashboard definition and
then tweak it, instead of adding each tile by hand.

**Needs live infra.** Building and publishing the dashboard object is a user-interface
action, so you do it yourself; the notebook only verifies the underlying numbers.

### E3. AI functions in SQL

**What this is.** Real artificial intelligence is a **single SQL function call** on this
platform — there is no model to deploy and no Python needed. You'll classify claims, score
the sentiment (tone) of complaint notes, hide personal data, and extract and summarise claim
documents, all in SQL, right where a data pipeline would.

**Where in Databricks.** The notebook `notebooks/E_analytics_and_ai/21_lab_e3_ai_functions` (open it from the
**Workspace** menu).

**Steps.**
1. Open `notebooks/E_analytics_and_ai/21_lab_e3_ai_functions` and attach **Serverless** compute.
2. **Section 1 — sentiment.** Find the first `%sql` cell. Replace the `note AS
   todo_replace_me` line with `ai_analyze_sentiment(note) AS sentiment`. Run it. This reads
   the free-text complaint notes in `2_silver_complaints` and labels each as positive,
   negative, neutral, or mixed — the tone is genuinely in the wording, so the labels make
   sense.
3. **Section 2 — classify severity.** In the next `%sql` cell, add a `severity` column using
   `ai_classify`, which picks the best-fitting label from a list you supply. Use:
   ```
   ai_classify(
     concat('A ', claim_type, ' motor claim with incurred amount EUR ',
            cast(incurred_amount AS string), ' and status ', status),
     array('minor', 'moderate', 'severe')
   ) AS severity
   ```
   The `concat(...)` builds a short sentence from the structured columns; `ai_classify` reads
   it and returns minor / moderate / severe. Run it.
4. **Section 3 — mask personal data.** In the next `%sql` cell add
   `ai_mask(note, array('person', 'email', 'phone number')) AS masked_note`. Run it: the
   model redacts the named kinds of personal information from each note.
5. **Section 4 — read documents, then extract and summarise.** Run the given Python cell
   first — it reads the text documents from your `docs` volume (the folder of claim
   documents the generator created) into a temporary view called `claim_docs` and prints how
   many it loaded. Then, in the following `%sql` cell, add these two columns:
   ```
   ai_extract(value, array('claim reference', 'policy reference', 'date of loss',
                           'claim type', 'reserve estimate')) AS extracted,
   ai_summarize(value, 40) AS summary
   ```
   `ai_extract` pulls the named fields out of each document; `ai_summarize` writes a short
   (~40-word) summary. Run it.

**You should see.** Four result tables, each with a new AI-generated column: a `sentiment`
label per note; a `severity` label per claim; a `masked_note` with personal details
redacted; and, for each document, an `extracted` set of fields plus a short `summary`.

**💡 Genie Code.** Instead of typing these, you could prompt Genie Code — for example
"score the sentiment of every complaint note and count negatives by tenant" — and it will
write the SQL for you.
