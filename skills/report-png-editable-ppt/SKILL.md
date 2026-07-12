---
name: report-png-editable-ppt
description: Use when converting text-heavy reports, Word/PDF reports, consulting reports, research reports, proposal text, or strategy documents into editable PowerPoint decks through the required CODEX-PPT image deck to local PNG extraction to Presentations editable rebuild workflow with explicit user approval gates.
---

# Report PNG Editable PPT

## Purpose

Convert a text-heavy report into an editable PPTX without skipping the visual design stage:

1. Use `codex-ppt` / CODEX-PPT to generate a high-quality image-based PPT.
2. Extract or save every slide as local PNG files named `slide_XX.png`.
3. Visually decompose those PNG pages into editable elements and rebuild the final PPTX with `presentations`.

This skill is mandatory for “文字报告转可编辑 PPT” requests unless the user explicitly asks for a different route in the same request.

## Hard Rules

- Do not directly build the final editable deck from the source report.
- Do not use the old `image PPT -> PDF -> pdf-to-editable-ppt` route unless the user explicitly asks for it.
- Do not deliver the CODEX-PPT image deck as the final editable deliverable.
- Do not place full-slide PNGs as final slide content. Full-slide PNGs are visual references only.
- Use local PNG crops only for inherently raster elements such as photos, complex textures, screenshots, logos, or detailed image fragments.
- Rebuild text as editable text boxes, tables as native tables, diagrams as editable shapes/connectors/icons, and charts as native charts or editable shape-based charts where practical.
- On Windows, set `HOME` to the user profile directory before running Presentations artifact-tool scripts, for example `HOME=C:\Users\A`.
- Keep intermediate artifacts: image PPTX, `origin_image/slide_XX.png`, extracted/cropped PNGs, preview/contact sheet, and final editable PPTX.

## Management Consulting PPT Design Rules

Use these rules for both the CODEX-PPT image stage and the final editable rebuild when the source is a management consulting report, strategy document, proposal, research report, operating diagnosis, SOE reform plan, or technology innovation plan:

- Overall positioning: prioritize clear logic, scan-friendly hierarchy, professional credibility, and systematic structure over decoration. Use a white canvas, blue-led brand system, light-gray/blue modules, and a small orange accent.
- Page system: use 16:9 widescreen. Content pages should be white-based; reserve full blue/visual backgrounds for cover, chapter, summary, or back-cover pages. Keep footer/logo/URL/page-marker placement stable.
- Typography: use Microsoft YaHei/微软雅黑 for Chinese and Arial for English/numbers unless a user template overrides it. Use bold action titles, regular body copy, and bold/color only for keywords.
- Font hierarchy: cover title 28-36pt; body-page title 20-24pt; module title 16-18pt; secondary label 14-16pt; body 12-14pt; notes and footnotes 8-10pt; large numbers/step ids 28-36pt.
- Color use: primary blue for titles, navigation, main flows, arrows, icons, and key labels; pale blue/light gray for module backgrounds and grouping; dark gray `#383838` for normal text; orange `#FF4200` only as small page markers, nodes, tags, or highlights. Use red only for risks, pain points, or strong warnings.
- Layout grammar: each content slide should have one message-led title, an optional one-sentence lead, and one dominant visual structure. Prefer frameworks, matrices, processes, cycles, roadmaps, issue trees, comparison grids, KPI cards, and architecture diagrams over plain bullet lists.
- Action titles: convert source headings into conclusion-oriented titles. The title should state the page's judgment, implication, or recommendation, not merely name the topic.
- Diagram and frame rules: use rectangles, low-radius rounded rectangles, arrows, dotted boundary boxes, circular step ids, and native-looking line icons. Same-level cards must share size, fill, border, and typography. Important relationships use solid lines; auxiliary boundaries use dotted lines.
- Line rules: use 0.5-0.75pt for ordinary borders, 1.0-1.5pt for emphasized borders, and 1.5-3pt for main process arrows. Do not mix many line styles on one page.
- Density rules: one core message per slide; 3-6 major modules per content page; 2-4 short lines per module. If there are more than six modules, group them or split the slide. Keep dense slides structured, not text-stacked.
- Emphasis rules: highlight 1-3 keywords per text block. Use blue bold for strategic keywords, red/orange only for pain points or alerts, and large numerals for steps or metrics. Do not duplicate text overlays when rebuilding editable slides.
- Navigation rules: for full consulting decks, use a top or side chapter navigation when useful. Keep section names short, gray for inactive sections, and primary blue for the current section.
- Avoid: decorative gradients, heavy shadows, large dark navy panels on body pages, generic stock imagery, repeated same-card layouts on every slide, centered body paragraphs, text outside frames, leftover placeholders such as `Sample`, and full-slide PNGs as final editable slide content.

## Required Approval Gates

Do not move past these gates without explicit user approval. A user saying “继续”, “确认”, “可以”, “按这个做”, or equivalent is sufficient.

1. **Outline Gate**: after reading the source, present the slide outline and wait.
2. **Style Gate**: present 2-3 visual style directions and the selected image backend; wait.
3. **Image Sample Gate**: generate one CODEX-PPT-style sample slide image; wait for approval or revision.
4. **PNG Contact Sheet Gate**: after full image deck generation and PNG extraction, show or report the PNG contact sheet/page list; wait.
5. **Editable Reconstruction Gate**: present the decomposition plan or one editable sample slide showing how PNG elements become editable PPT objects; wait.
6. **Final Delivery Gate**: only after full rebuild, QA, and render/audit checks deliver the final editable PPTX.

If the user explicitly asks to skip approvals, still require at least the Image Sample Gate and Editable Reconstruction Gate unless the user separately confirms they accept fully autonomous production.

## Workflow

### 1. Source Intake

- Extract report headings, paragraphs, tables, images, and appendices.
- Identify the audience, deck purpose, implied page count, and required tone.
- Build a concise deck storyline. Do not create one slide per source page by default.
- Save a draft outline when useful, then ask for Outline Gate approval.

### 2. CODEX-PPT Image Deck

- Use the `codex-ppt` skill workflow.
- Prefer the built-in image generation tool when available. In Codex, generated images are saved under `C:\Users\A\.codex\generated_images\...`; copy those images into the deck project `origin_image` folder and leave originals in place.
- Use CLI/API fallback only when needed and after checking configuration.
- Generate one sample slide first and ask for Image Sample Gate approval.
- After approval, generate the full image deck. For multi-slide production, follow CODEX-PPT dispatch/state recording rules where applicable.
- Assemble the image deck with `codex-ppt/scripts/assemble_ppt.py`.

### 3. PNG Extraction

- Use existing CODEX-PPT `origin_image/slide_XX.png` files directly when they are the generated slide images.
- If only an image PPTX exists, export or extract each slide to PNG in strict page order.
- Verify:
  - every expected `slide_XX.png` exists,
  - images are readable,
  - page count matches the approved outline,
  - pages are 16:9,
  - order matches the image PPT.
- Create a PNG contact sheet or page list and ask for PNG Contact Sheet Gate approval.

### 4. Visual Decomposition

For each PNG page, map the visual into editable elements:

- **Text**: recreate as editable text boxes, not OCR word fragments.
- **Tables**: rebuild as native PPT tables where feasible.
- **Diagrams**: rebuild with native shapes, connectors, icons, and grouped objects.
- **Charts**: use native charts where data is available; otherwise use editable shape-based chart approximations with truthful visual proportions.
- **Raster regions**: crop only the smallest meaningful PNG fragments for visual textures, screenshots, illustrations, or hard-to-recreate image areas.

Prepare a concise decomposition plan or one editable sample slide, then ask for Editable Reconstruction Gate approval.

### 5. Presentations Rebuild

- Use the `presentations` skill/runtime and artifact-tool presentation JSX.
- Build final slides from editable objects, using the approved PNGs as visual references.
- Keep output under the Presentations workspace pattern when practical:
  - `outputs/<thread-id>/presentations/<task-slug>/slides`
  - `preview`
  - `layout`
  - `assets`
  - `output`
- On Windows PowerShell, set:

```powershell
$env:HOME = 'C:\Users\A'
$env:PYTHON = 'C:\Users\A\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
```

- Run the Presentations build script and require exit code `0`.
- If artifact-tool cannot locate `@oai/artifact-tool`, check `HOME` first.

### 6. QA And Delivery

Before final delivery:

- Render previews/contact sheet for the final editable PPTX.
- Inspect object structure: final slides must not be full-slide screenshots.
- Verify text is editable and grouped semantically.
- Run a PPTX audit for fonts, shadows, small text, insets, and text overlap when available.
- Confirm the final output is `.pptx`.
- Report:
  - final editable PPTX path,
  - image PPTX path,
  - PNG directory path,
  - preview/contact sheet path,
  - any residual limitations.

## Known Environment Fixes

- `codex-ppt/scripts/assemble_ppt.py` must avoid non-ASCII status symbols such as `✓` on Windows GBK consoles; use `[OK]`.
- Presentations artifact-tool scripts may need an explicit successful `process.exit(0)` after awaited file generation on Windows to avoid native canvas teardown faults after outputs are written.
