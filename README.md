# Databricks Foundations Workshop

A hands-on, full-day Databricks workshop for engineers and architects who are **new to
the platform** and want to learn how to build a **data product on top of it** — bringing
data in, transforming it, governing it across multiple tenants, and sharing it back out.

It is built around one small synthetic insurance book (fictional insurers), but the
skills are general-purpose: the insurance flavour is just a backdrop for platform
concepts. Nothing here is client-specific and the material is intended to be reusable.

> **About this demo / workshop**
> All data is synthetic and generated on the fly. All company names are fictional.
> Nothing here is real customer, policy, or claims data.

## The scenario

You work at **Keystone**, a fictional company that runs a shared data platform for
insurers. Three client insurers — **Bricksurance SE**, **Northwind Mutual**, and
**Helios Re** — are your *tenants*. Across the day you build the platform underneath them:
bring their data in, transform it, keep each tenant isolated, share results, and put a
small app in front. Every row carries a `tenant` column, which is what powers the
isolation, security, and sharing labs.

## Status

🏗️ **Foundation built and tested; labs in progress.**

- ✅ `notebooks/00_config.py` — sets catalog/schema/volumes/tenants (auto-detects catalog; defaults to `main` on Free Edition).
- ✅ `notebooks/01_data_generator.py` — synthetic multi-tenant book with real signal; verified on serverless.
- ⏳ Lab notebooks (solve + solved) — being added track by track.

### Data the generator produces

| Asset | Contents |
|---|---|
| Volume `raw/` | `policies.csv`, `claims.csv` (deliberately messy), `claims_batch_02.csv` (staged for lab B2) |
| Volume `landing/claims/` | `claims_batch_01.csv` — an arrived Auto Loader batch |
| Volume `docs/` | ~15 claim documents as text (for `ai_extract` / `ai_summarize`) |
| `2_silver_complaints` | free-text complaint notes with real sentiment (for `ai_analyze_sentiment`) |
| `2_silver_property_policies` | a small, clean second line of business |
| `build_all=yes` also builds | `2_silver_policies`, `2_silver_claims`, `3_gold_portfolio_summary`, `3_gold_loss_ratio_monthly` |

Quick start: import this repo (Workspace → Git folder), open `00_config`, set your
catalog/schema, run `01_data_generator`, then follow the labs.

## Use-case list & instructions

The living list of use cases (what each lab teaches, hands-on vs. demo, Free Edition
feasibility) lives in the workshop instructions document. This is the source of truth we
add to as the workshop takes shape:

**[Workshop instructions & use-case list (Google Doc)](https://docs.google.com/document/d/1SHEQdec3DxwWHbeUCWGQzPRU7kH5pjzpwNnsflBhFTg/edit)** — under review.

## Portability & Free Edition

- Designed to run on any Databricks workspace, including **Databricks Free Edition**
  (serverless-only, Databricks-managed storage, catalog `main`).
- Plain notebooks, config-driven catalog/schema, no external data dependencies for the
  core hands-on labs.
- Some platform capabilities (cross-organisation sharing, bring-your-own storage,
  federation to external databases) are constrained on Free Edition and are run as
  instructor-led demonstrations rather than attendee hands-on. The instructions document
  marks each case accordingly.

## Layout

```
notebooks/    workshop notebooks (to be added)
```
