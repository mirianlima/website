# Claude Design prompt — personal website

Paste the prompt below into Claude Design (claude.ai/design) **after** the Quarto
scaffold exists. Link the repo as context first, but only the rendered sample
pages and config — exclude `_freeze/`, `.git/`, and any large data files.

Workflow this prompt belongs to:

1. Scaffold the plain Quarto site (spec implementation).
2. Render a representative sample post (prose, code cells, a Mosaic explorable,
   a callout, a table) and a listing page with `embed-resources: true` so each
   is a single self-contained HTML file exposing Quarto's real DOM.
3. Run the Claude Design round with this prompt and the repo linked.
4. Pick one of the three proposed directions, iterate, then export via
   "Send to Claude Code" and port the result into `_brand.yml` + `custom.scss`
   + template partials.

---

```text
PURPOSE
Design a personal website for a senior data scientist / AI engineer. The site
hosts long-form technical writing: a blog, tutorials, project showcases, and
"explorable" posts containing interactive data visualizations (charts with
sliders, brushes, and linked views). Tone: confident, quiet, editorial —
think a beautifully typeset technical journal, not a SaaS landing page.
Content is the hero: typography, whitespace, and reading rhythm matter more
than decoration. It should feel hand-crafted and personal, never template-y.

PAGES TO DESIGN (desktop + mobile for each)
1. Landing page — name, one-line identity, latest writing, selected projects.
   This page may be fully bespoke; go bold here (tasteful motion welcome).
2. Blog listing page — chronological cards: title, date, description, tags,
   optional thumbnail.
3. Article page — THE most important screen. Long-form prose with headings,
   code blocks, tables, figures with captions, callout boxes, footnotes, and
   embedded interactive charts. Design for 60–80 char measure, generous line
   height, clear hierarchy, and code that is as pleasant to read as prose.
4. Projects page — grid of project cards with short descriptions and links.

CRITICAL TECHNICAL CONSTRAINTS — read carefully
- The site is built with Quarto, a static site generator based on Bootstrap 5.
  I have linked the repo: it contains REAL rendered sample pages
  (sample-post.html, sample-listing.html). DO NOT invent your own markup for
  pages 2 and 3 — restyle the existing HTML structure and class names in
  those samples. Your CSS must target those real selectors (e.g. Quarto's
  code cells, .callout blocks, figure captions, the navbar, the title block).
  The landing page (page 1) is exempt: free-form HTML is fine there.
- Output: semantic HTML + plain vanilla CSS + minimal vanilla JS only.
  NO React, NO Tailwind, NO CSS frameworks beyond what the samples already
  include (Bootstrap is already on the page — override it, don't replace it).
- Express the design system as CSS custom properties (design tokens) in one
  block: full color palette (incl. semantic roles: background, foreground,
  primary, link, code-background, border), the complete type scale, spacing
  scale, radii. I will port these tokens into Quarto's _brand.yml and SCSS
  variables, so keep them clean and centralized.
- Both light AND dark mode, driven by those tokens.
- Fonts: max 2 families + 1 monospace, all freely available (Google Fonts or
  similar). Specify exact families, weights, and fallback stacks.
- Charts in articles are rendered by Observable Plot / Mosaic vgplot into
  container divs. Style the containers (background, border, caption, spacing)
  but leave their inner SVG content alone. Include one placeholder chart area
  in the article design so spacing around interactives is defined.
- Performance: this is a static site — no heavy JS, no animation libraries.
  CSS-only effects preferred; total added JS under ~10KB.
- Accessibility: WCAG AA contrast in both modes, visible focus states,
  reduced-motion respected.

DELIVERABLES
- The four designed pages as standalone HTML/CSS.
- A design-tokens.css file (the custom-properties block described above).
- A short README mapping each design decision to where it applies
  (tokens → site-wide, selector overrides → article/listing styling,
  bespoke HTML → landing page only).
- Export via "Send to Claude Code" when done — the handoff will be
  implemented into the Quarto repo from there.

Start by proposing 3 distinct visual directions (mood + landing page + a
fragment of the article typography for each) before fully building anything,
so I can pick one to develop.
```
