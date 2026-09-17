# Section format (for writing the attendee runbook)

Audience: someone who has **never seen Databricks**. Assume nothing. Be verbose. Say
exactly where to click and what to type. Expand every acronym on first use. No marketing
words ("WOW" etc.). Keep insurance framing light — lead with the platform idea.

Each track file (`A.md`, `B.md`, …) starts with:

```
## Track X — <name>

<2–4 sentence plain-English description of what this track is about and why it matters to
someone building a data product.>
```

Then, for **each lab** in the track, use exactly this shape:

```
### <ID>. <Lab name>

**What this is.** 1–3 plain sentences. What you'll do and why it's useful.

**Where in Databricks.** Name the surface(s) a beginner must find, e.g. "Notebook
`notebooks/B_bring_a_source_in/06_lab_b1_file_upload` (open it from the **Workspace** menu on the left)",
or "the **SQL Editor**", "the **Catalog** browser", "**Jobs & Pipelines**".

**Steps.**
1. Verbose, numbered, click-by-click. For every UI action say where the button/menu is
   (which sidebar, which tab, top-right, etc.). For every cell to run, say what it does in
   one line. When the attendee must fill a `# TODO`, quote what to type and explain it.
2. …

**You should see.** The concrete expected result (a number, a table, a chart, a message)
so they know it worked.

**💡 Genie Code.** (Only where relevant) one line on how they could prompt Genie Code to
do the same thing instead of typing it.

**Needs the instructor / a partner / live infra.** (Only where relevant) one honest line
on any step that can't be done solo on Free Edition, and what to watch the instructor do.
```

Read the ACTUAL notebook (`notebooks/NN_lab_*.py` for the attendee-facing gaps, and
`solutions/NN_solution_*.py` for what the finished result is) before writing the steps, so
the instructions match the real cells and TODOs. Reference the lab by opening it from the
Workspace; the attendee runs cells with **Shift+Enter** (or the ▶ at the cell's top-left).
