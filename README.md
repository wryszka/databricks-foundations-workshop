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

## Status

🚧 **Scaffold only.** The use cases are being drafted and reviewed in the workshop
instructions document (link below). Notebooks, data generator and lab content are **not
built yet** — they will be added once the use-case list is signed off.

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
