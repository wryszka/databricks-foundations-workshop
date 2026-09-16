## Track F — Share it back out

A data platform is only useful if the results can leave your walls safely. Track F is
about **Delta Sharing**: an open way to hand a live table to someone in a *different*
Databricks workspace or organisation — a client insurer, an auditor, a reinsurer —
**without copying any files** and **without giving them a login to your workspace**. They
always see the current data, and you can scope exactly what they get (even down to a single
tenant's rows). This is how Keystone would deliver each insurer *their* results and no one
else's.

### F1. Delta Sharing, attendee to attendee

**What this is.** You will publish one tenant's results table as a read-only "share", grant
it to a recipient, and then — paired with the person next to you — actually query each
other's shared data. It shows how governed results move between organisations with no file
copying.

**Where in Databricks.** Notebook `notebooks/22_lab_f1_delta_sharing` (open it from the
**Workspace** menu on the left). You will run its cells; the person you pair with runs a
couple of SQL statements in **their** workspace's **SQL Editor**.

**Steps.**
1. In the **Workspace** file browser on the left, open your `databricks-foundations-workshop`
   Git folder, then `notebooks/`, and click `22_lab_f1_delta_sharing` to open it. Make sure
   **Serverless** compute is selected in the top-right (as in Part 0).
2. **Pair up with a neighbour now.** One of you will publish first while the other adds it;
   then swap. You each need the other's *sharing identifier* (you'll fetch it in step 6).
3. Run the first code cell (**Shift+Enter**). It is `%run ./00_config` — it loads your
   catalog, schema and the `TENANTS` list so the notebook knows where your data is. Wait for
   it to finish (a small green tick appears).
4. Run the **"0. Make sure there is something to share"** cell. It checks that the table
   `3_gold_portfolio_summary` exists. If it errors, go back and run `01_data_generator` with
   the **build_all** widget set to `yes`, then return here.
   - *You should see:* `shareable table ready`.
5. Fill in **TODO 1 and TODO 2** in the *"1. Create a share and add ONE tenant's slice"*
   cell. A **share** is a named, read-only bundle of tables you offer to others. Type:
   ```python
   spark.sql(f"CREATE SHARE IF NOT EXISTS {SHARE} COMMENT 'Keystone gold portfolio share'")
   spark.sql(f"ALTER SHARE {SHARE} ADD TABLE {FQ}.`3_gold_portfolio_summary` "
             f"PARTITION (tenant = '{SHARE_TENANT}') AS keystone.portfolio_{SHARE_TENANT}")
   ```
   The `PARTITION (tenant = ...)` line is the important bit: it adds **only one tenant's
   rows**, so the recipient can never see the other insurers. Run the cell.
   - *If you get a `PERMISSION_DENIED` message*, creating shares needs a metastore-admin
     privilege you may not have — that's expected on a locked-down or Free Edition workspace.
     Read the "Needs…" note below and watch the instructor instead; the rest still teaches.
6. **Get your partner's sharing identifier.** Your partner runs, in *their* notebook or SQL
   Editor, `SELECT current_metastore()` and reads you the value. At the top of your notebook
   find the **partner_sharing_id** widget (a small text box) and paste their value in. (Leave
   it blank if you want "open sharing", which instead produces an activation link you can
   send to anyone.)
7. Fill in **TODO 3 and TODO 4** in the *"2. Create a recipient and grant the share"* cell.
   A **recipient** is who you're sharing with. Type:
   ```python
   spark.sql(f"CREATE RECIPIENT IF NOT EXISTS {RECIPIENT} USING ID '{partner}'")   # if partner set
   spark.sql(f"GRANT SELECT ON SHARE {SHARE} TO RECIPIENT {RECIPIENT}")
   ```
   (If `partner` is blank, create the recipient without `USING ID '...'` — that's the
   open-sharing path.) Run the cell.
8. Fill in **TODO 5** in the *"3. Inspect what you published"* cell and run it:
   ```python
   display(spark.sql(f"SHOW SHARES LIKE '{SHARE}'"))
   display(spark.sql(f"SHOW ALL IN SHARE {SHARE}"))
   display(spark.sql(f"DESCRIBE RECIPIENT {RECIPIENT}"))
   ```
   For open sharing, the activation link appears in the `DESCRIBE RECIPIENT` output — hand
   that to your partner.
9. **The partner side.** Now your partner mounts *your* share in their own **SQL Editor**
   (left menu → **SQL Editor**) and queries it — no copy, always live:
   ```sql
   CREATE CATALOG IF NOT EXISTS from_keystone USING SHARE <your_provider_name>.<share_name>;
   SELECT * FROM from_keystone.keystone.portfolio_bricksurance_se;
   ```
10. **Swap roles** and repeat so you each publish and each query the other's share.

**You should see.** `SHOW ALL IN SHARE` lists your one shared table, and your partner's
`SELECT` returns rows for a single tenant only (never the others) — proving the share is
live and correctly scoped.

**💡 Genie Code.** In the notebook's Genie Code panel you could type "create a Delta share
called keystone_share and add only the bricksurance_se rows of 3_gold_portfolio_summary"
and let it draft the `CREATE SHARE` / `ALTER SHARE` statements for you.

**Needs the instructor / a partner / live infra.** This lab genuinely needs **two people
in two workspaces**, and creating shares/recipients needs **metastore-admin** privilege.
On **Databricks Free Edition**, confirm with your instructor whether Delta Sharing is
available to you — if not, the instructor demonstrates the publish-and-query round-trip and
you follow along.
