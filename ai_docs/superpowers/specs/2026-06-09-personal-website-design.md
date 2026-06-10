# Personal Website — Design Spec

**Date:** 2026-06-09
**Status:** Approved design, pending implementation plan

## Purpose

A personal website for blogging, technical tutorials, posts, and project showcases.
Mostly static, cheap to run, trivial to deploy, with the option of distill-style
interactive "explorables" inside posts. Substack remains the newsletter channel,
fed from the site.

## Requirements

- Static site: blog with listings + RSS, tutorials, projects page, about page.
- Authoring fits the owner's daily stack: Python, marimo, polars, DuckDB, some TS/JS.
- Interactive explorables inside posts (sliders, brushes, linked views) without
  servers — including Mosaic/vgplot, which is a hard interest.
- Substack stays as the newsletter; the site is the canonical home.
- Minimal build/host/CI complexity. KISS; no second framework, no servers.

## Decision

**Quarto website, hosted on GitHub Pages, deployed by one GitHub Action.**
Interactivity is a per-post ladder built on the Observable runtime and
DuckDB-WASM inside Quarto — not a separate site framework.

### Alternatives considered and rejected

- **React app bundling Quarto HTML output** — two toolchains plus routing/hydration
  glue to wrap content Quarto already renders as a site. Rejected as overengineering.
- **Observable Framework as the site** — best-in-class reactive data apps, built-in
  `vg` (Mosaic), but: no blog machinery (no listings, no RSS — both hand-rolled),
  Python demoted to build-time data loaders (posts can't show Python as content),
  and feature development has been frozen since v1.13.0 (Nov 2024).
- **Observable Notebook Kit as the site** — open vanilla-JS notebook format, very
  active development, but it is a Technology Preview, notebook-shaped rather than
  website-shaped, and posts would be JS-first. Kept as an embed target (tier 5),
  not the foundation.

The deciding observation: Quarto embeds the Observable runtime natively, so the
OJS ecosystem's interactivity is available *inside* Quarto posts, while the
reverse (Quarto's publishing machinery inside Framework/Notebook Kit) cannot be
bolted on. Mosaic in particular needs no integration work at all (see below).

## Repo structure

```
website/
├── _quarto.yml                  # site config: nav, theme, RSS, code tools
├── index.qmd                    # home / landing
├── about.qmd
├── blog/
│   ├── index.qmd                # listing page (generates feed.xml)
│   └── posts/<date>-<slug>/
│       ├── index.qmd            # the post
│       └── data.parquet         # only for explorable posts
├── projects/index.qmd           # project cards (Quarto listing, yaml-driven)
├── (explorable posts inline a 6-line vg bootstrap cell — a shared
│    _includes setup file trips Quarto's OJS block-count warning;
│    revisit as an include-in-header partial at explorable post #2)
├── _extensions/                 # quarto-marimo, vendored via `quarto add`
├── pyproject.toml + uv.lock     # python env for build-time execution
├── _freeze/                     # committed render cache
└── .github/workflows/publish.yml
```

## Interactivity ladder (chosen per post, nothing global)

1. **Static (default).** polars/DuckDB execute at render time on the author's
   machine; `freeze: auto` means CI never re-executes old posts.
2. **Explorable — Mosaic/vgplot + DuckDB-WASM.** Build-time Python writes a
   parquet next to the post; a shared include imports `@uwdata/vgplot` from CDN
   (standard dynamic ESM import) and wires `vg.wasmConnector()`; the post declares
   vgplot marks/inputs with crossfilter selections. Proven pattern at 10M-row
   scale in static Quarto pages (cscheid's flights example). Plain OJS +
   Observable Plot remains the lighter option for one-slider posts.
   Mosaic brings its own reactivity (Selections/Params via DuckDB), so Quarto's
   older OJS dialect is irrelevant to it — the vgplot code is vanilla JS.
3. **Runnable Python — marimo islands** via the quarto-marimo engine extension
   (officially maintained by the marimo team; requires Quarto ≥ 1.9.20).
   Readers edit and re-run Python in the browser (Pyodide). Reserved for posts
   where that is the point: first load is multi-second and package availability
   is constrained (DuckDB has a Pyodide build; verify polars-in-WASM before a
   post depends on it).
4. **Full notebook — marimo WASM HTML export**, iframed, for "open the whole
   thing" tutorials.
5. **App-grade pieces — Observable Notebook Kit**, built standalone and iframed.
   Upgrade path: a Quarto pre-render hook running `notebook kit build` the first
   time one of these actually exists. A custom Quarto engine extension for
   Notebook Kit was evaluated and rejected for now (preview-status API, dual
   Observable runtimes on one page, sole-maintainer burden).

### Mosaic authoring workflow

Explore in marimo/Jupyter against polars/DuckDB (the official Mosaic Jupyter
widget works in a live kernel). Publish as: parquet + vgplot cell, or a
mosaic-spec YAML (generatable from Python) parsed in the browser. No live kernel
exists on the static site; DuckDB-WASM serves the published page.

## Build / CI / hosting

- `quarto render` locally; `_freeze/` committed, so CI renders markdown and
  bundles assets without reproducing the Python environment.
- One GitHub Action: checkout → install Quarto (+ uv only if needed for
  marimo-island posts) → render → deploy to GitHub Pages.
- Custom domain on GitHub Pages later; placeholder `<username>.github.io` first.

## Substack integration (feasibility audited 2026-06)

Confirmed facts, from primary sources:

- **No official publishing API.** Substack's Developer API is read-only profile
  lookup. Reverse-engineered private APIs exist but are unsupported and fragile —
  not used.
- **Importer:** official, manual, accepts URL/RSS; suitable for one-time backfill.
  Imported posts are never emailed to subscribers, so import cannot power the
  newsletter.
- **No canonical-URL setting on Substack.** Mitigation: publish on the site
  first; the Substack copy links back ("originally published at…"). Same-author
  cross-posting carries no meaningful SEO penalty per current guidance.
- **Official subscribe-form embed** (iframe) exists and goes on the site.

Workflow per post: publish on the site → paste into Substack editor → send.
Explorable posts go out as teaser + screenshot + link to the interactive
version. Optional one-time RSS backfill of the archive when the Substack is set
up.

## Verification

- CI fails if `quarto render` fails (broken code, bad links with link checking
  enabled).
- Explorable posts are checked in a browser before publishing.
- Any custom build scripts get tests (TDD); site content itself is verified by
  render + manual browser check. Nothing more — YAGNI.

## Out of scope (deliberately)

Comments, analytics, search beyond Quarto's built-in, tag taxonomy beyond Quarto
categories, custom React components, any Substack automation. All addable later
without rework.

## Risks / caveats

- Pyodide tiers (3–4) have heavy first loads; default explorables to tier 2.
- polars availability in Pyodide unverified; check before any post depends on it.
- Quarto's OJS cells use the pre-2.0 Observable dialect; cosmetic for tier 2
  (Mosaic code is vanilla JS), revisit only if it becomes a real constraint.
- Notebook Kit is a Technology Preview; it is isolated behind iframes so its
  churn cannot affect the site.
