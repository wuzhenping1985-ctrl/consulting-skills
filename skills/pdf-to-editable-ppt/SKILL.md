---
name: pdf-to-editable-ppt
description: Convert PPT-style PDF files into fully editable native PowerPoint decks using the bundled CIIC/Yuexiu-style corporate PPT template. Use when a user provides a slide-like PDF and asks to rebuild it as a PPT/PPTX with editable text, native tables, shapes, connectors, diagrams, template content pages, optional cover/catalog/section/back-cover layouts only when present in the source or explicitly requested, 16:9 layout, Microsoft YaHei typography, CIIC/Yuexiu blue styling, no shadows, no NotebookLM footer, direct text inside shapes/cells, 0.1 cm left inset, faithful diagram topology, balanced composition, and readable 10pt+ text. Never satisfy the conversion by placing full-page screenshots or rasterized PDF pages onto slides; image-only PDFs require OCR/visual transcription and native reconstruction. Also includes the merged Codex PPT image-based workflow for explicit requests to create visually unified full-slide-image PPTX decks from articles, reports, papers, notes, or outlines.
---

# PDF to Editable PPT

## Goal

Rebuild a PPT-style PDF as a native, editable `.pptx`, preserving the source reading order, structure, layout, charts, tables, and hierarchy as closely as practical while applying the bundled PPT template as the final visual system.

The delivered PPTX must be editable. Full-page screenshots, page images, or rasterized PDF pages are not acceptable final slide content, even when the source PDF has no text layer. Use rendered PDF pages only as temporary visual references. If the source PDF is image-only, perform OCR and visual transcription, then rebuild the page with native PowerPoint text boxes, shapes, tables, connectors, lines, icons, and editable charts/diagrams.

Use bitmap images only for source elements that are inherently raster and not reasonably reconstructable as native PPT objects, such as photos, logos, screenshots, complex illustrations, or texture/background fragments. Crop those raster elements to the smallest meaningful region; never place an entire PDF page as a single picture. If time, tooling, or source quality prevents an editable reconstruction, stop and tell the user the conversion cannot meet the editable-output requirement instead of delivering a screenshot-based deck.

## Optional Codex PPT Image Workflow

This skill also carries the merged `codex-ppt` workflow for requests that explicitly ask for an image-based deck where each slide is a full-slide generated image. This is a separate companion mode, not a replacement for the editable PDF reconstruction contract above.

Use the companion workflow only when the user clearly asks to generate an image-based PPT/PPTX from an article, report, paper, note, or outline, or explicitly accepts full-slide image slides. In that mode, read and follow `references/codex-ppt-workflow.md` and use the bundled Codex PPT scripts copied into this skill's `scripts/` directory.

When this skill is used as either a direct PPT-like PDF route or as the final reconstruction route after report synthesis, the final user-facing PPTX must be built on the CIIC consulting template in `assets/default-template.pptx` unless the user supplies a newer template in the same request. The image-based companion workflow may produce an intermediate or explicitly requested image-only companion deck, but it must not replace the template-based final deliverable for normal conversion requests.

Do not use the image-based workflow to satisfy a normal PPT-style PDF reconstruction request. For this skill's default PDF conversion task, the existing editable-output rules remain mandatory: no full-page PDF screenshots, no rasterized source pages as final slide content, OCR/visual transcription for image-only PDFs, and native editable PowerPoint objects wherever feasible. If the user asks for both faithful editable PDF reconstruction and full-slide generated-image output, explain that those are different deliverables and ask which output should take priority.

## Required Template Contract

Always build the final deck on top of `assets/default-template.pptx` unless the user supplies a newer template in the same request. Do not start from a blank white presentation when this skill is used.

Default to rebuilding only the source PDF's content pages. Do not add template cover, catalog, section divider, or back-cover pages merely because the template provides those layouts. Add those non-content pages only when the source PDF already contains corresponding pages or when the user explicitly asks for them.

The bundled template is a 16:9 deck with these template layout roles:

- `封面`: use only when the source PDF has a cover page or the user explicitly requests a cover.
- `目录`: use only when the source PDF has an agenda/catalog page or the user explicitly requests one. Put only the main catalog headings in the template's existing catalog text boxes/placeholders; omit small explanatory subtitles unless the user explicitly asks for a detailed agenda. Keep the template catalog text boxes/placeholders at their original position, size, and alignment. Do not move the catalog entry block to a new x/y position. If there are too many catalog entries for the original placeholder, continue on the next line/downward within the template's existing catalog rhythm, or split to another catalog page; do not reposition the first catalog entry.
- `章节`: use only when the source PDF has second-level title/chapter divider pages or the user explicitly requests divider pages.
- `内页版式-基础`: use for standard reconstructed body/content pages.
- `1_内页版式-基础`: use for content pages without a key-point lead.
- `内页版式-左右等分`: use when the source page has two balanced columns.
- `内页版式-左右1:2`: use when the source page has a narrow left column and wider right column.
- `内页版式-左右2:1`: use when the source page has a wider left column and narrow right column.
- `内页版式-左中右三分`: use when the source page has three parallel columns.
- `内页布局-右侧强调` / `1_内页布局-右侧强调`: use when the source page has a right-hand summary, conclusion, quote, KPI, or visual emphasis rail.
- `内页布局-左侧强调`: use when the source page has a left-hand blue emphasis rail and right-side content columns.
- `封底`: use only when the source PDF has a back-cover page or the user explicitly requests one.

Use the template's master/layouts, color system, typography hierarchy, page decorations, title placement, footer logic, and overall visual rhythm. The visible source PDF content should be adapted into the template's content area rather than copied onto blank pages. If the source PDF has no cover/catalog/back-cover, do not create them by default; the deliverable may consist entirely of reconstructed content pages.

Template color family to preserve: blue-led CIIC/Yuexiu corporate palette. Use `#1C55FE` as the primary blue, `#547FFE` as secondary blue, `#8DAAFE`, `#B3D4FE`, and `#CFDBFF` as supporting light blues, `#126BF7` / `#0042FF` for rules and links, `#383838` for dark text, `#E7E6E6` / `#DCDCDC` for neutral fills, and white backgrounds. Use `#FF4200` only as a small warning/page-marker/emphasis accent, not as a broad fill.

## CIIC/Yuexiu Style Contract

The reference deck is 33.87 cm x 19.05 cm (16:9). Match these visual rules unless the user explicitly supplies a different template:

- Content-page title area: `x=1.83 cm`, `y=0.00 cm`, `w=30.16 cm`, `h=2.86 cm`; title text is Microsoft YaHei/微软雅黑, bold, dark `#383838`/theme text, 24pt. Reduce to 22pt or 20pt only when a long title cannot fit. Do not use the old 20pt default as the normal title size.
- Content-page rules: upper blue rule at about `y=3.14 cm` from `x=1.86 cm` to `x=32.00 cm`; lower blue rule at about `y=17.95 cm`; use rule color `#0042FF` or theme accent blue. Keep all main content between these rules.
- Key-point lead placeholders: start at `y=3.52 cm`, use 16pt Microsoft YaHei, usually dark text; preserve the template's column widths for one, two, or three key-point columns.
- Main body text: use 14pt Microsoft YaHei as the normal body size. Use 12pt for dense tables, notes, footers, or packed labels. Use 10-11pt only when unavoidable after reflow.
- Large KPI numerals: use Impact for prominent standalone numbers/percentages when matching the reference deck; pair with Microsoft YaHei for Chinese units and labels. Keep ordinary numbers in Microsoft YaHei.
- English template labels such as `CONTENTS` may remain Arial when inherited from the template.
- Cover: title uses the cover title placeholder at about `x=1.82 cm`, `y=4.24 cm`, `w=15.53 cm`, `h=3.98 cm`, about 34pt; subtitle/tagline uses about 24pt; speaker/date line uses about 12pt.
- Catalog: use the `目录` layout title at about `x=1.83 cm`, `y=2.35 cm`, and the `CONTENTS` placeholder at about `x=5.53 cm`, `y=2.27 cm`; keep entries aligned to the template rhythm rather than inventing a new catalog grid.
- Section divider: use `章节` with title at about `x=9.92 cm`, `y=5.51 cm`, `w=13.65 cm`, `h=1.52 cm`; chapter number sits large on the right. Keep the left/bottom decorative blue bands.
- Footer/page marker: preserve the orange page marker near `x=31.10 cm`, `y=17.29 cm`, and the footer URL near `x=29.43 cm`, `y=17.97 cm` when the template provides them. Do not place content over these elements.

## Management Consulting PPT Design Rules

When reconstructing or adapting pages for management consulting, strategy, organization, SOE reform, technology innovation planning, research, proposal, or executive briefing decks, apply these design rules in addition to source fidelity and editability requirements:

- Overall positioning: prioritize clear logic, scan-friendly hierarchy, professional credibility, and systematic structure over decoration. Use a white canvas, blue-led brand system, light-gray/blue modules, and a small orange accent.
- Page system: use 16:9 widescreen. Content pages should be white-based; reserve full blue/visual backgrounds for cover, chapter, summary, or back-cover pages. Preserve stable footer/logo/URL/page-marker placement.
- Typography: use Microsoft YaHei/微软雅黑 for Chinese and Arial for English/numbers unless a user template overrides it. Use bold action titles, regular body copy, and bold/color only for keywords.
- Font hierarchy: cover title 28-36pt; body-page title 20-24pt, with this skill's CIIC default at 24pt; module title 16-18pt; secondary label 14-16pt; body 12-14pt; notes and footnotes 8-10pt; large numbers/step ids 28-36pt.
- Color use: primary blue for titles, navigation, main flows, arrows, icons, and key labels; pale blue/light gray for module backgrounds and grouping; dark gray `#383838` for normal text; orange `#FF4200` only as small page markers, nodes, tags, or highlights. Use red only for risks, pain points, or strong warnings.
- Layout grammar: each content slide should have one message-led title, an optional one-sentence lead, and one dominant visual structure. Prefer frameworks, matrices, processes, cycles, roadmaps, issue trees, comparison grids, KPI cards, and architecture diagrams over plain bullet lists.
- Action titles: rewrite generic source headings into conclusion-oriented titles when the task is adaptation/redesign. Preserve original headings only when strict one-to-one fidelity is required.
- Diagram and frame rules: use rectangles, low-radius rounded rectangles, arrows, dotted boundary boxes, circular step ids, and native-looking line icons. Same-level cards must share size, fill, border, and typography. Important relationships use solid lines; auxiliary boundaries use dotted lines.
- Line rules: use 0.5-0.75pt for ordinary borders, 1.0-1.5pt for emphasized borders, and 1.5-3pt for main process arrows. Do not mix many line styles on one page.
- Density rules: one core message per slide; 3-6 major modules per content page; 2-4 short lines per module. If there are more than six modules, group them or split the slide. Keep dense slides structured, not text-stacked.
- Emphasis rules: highlight 1-3 keywords per text block. Use blue bold for strategic keywords, red/orange only for pain points or alerts, and large numerals for steps or metrics. Do not duplicate text objects to create emphasis.
- Navigation rules: for full consulting decks, use a top or side chapter navigation when the source/template includes it or when redesigning a full report deck. Keep section names short, gray for inactive sections, and primary blue for the current section.
- Avoid: decorative gradients, heavy shadows, large dark navy panels on body pages, generic stock imagery, repeated same-card layouts on every slide, centered body paragraphs, text outside frames, duplicated text overlays, leftover placeholders such as `Sample`, and final slides made from full-page screenshots.

## Workflow

1. Inspect the input PDF.
   - Determine page count, page aspect ratio, dominant theme, recurring masters, headers/footers, title styles, table styles, and chart styles.
   - Render each PDF page to a high-resolution PNG for visual reference.
   - Extract text and images when available; if extraction is poor or absent, use OCR plus visual reading. Treat an image-only PDF as a reconstruction task, not as permission to embed page images.

2. Create the deck from the template.
   - Open/copy `assets/default-template.pptx` as the base file and add/rebuild slides using its layouts.
   - Set slide size to widescreen 16:9 only if the template or user-supplied template is not already 16:9.
   - Use Microsoft YaHei/微软雅黑 for normal Chinese text runs, including table cells and chart labels. Use Impact only for large standalone KPI numerals when matching the reference style.
   - Reuse the template colors, line weights, title placements, page numbers, logos, recurring bands, and section/page roles where applicable to the source pages being rebuilt.
   - On body/content pages, keep the headline at 24pt. If the headline cannot fit cleanly in the template title area, reduce to 22pt, then 20pt only if needed. Do not use 18pt body-page headlines unless the user explicitly overrides this rule or the title is exceptionally long.
   - Place all main body content inside the template's central blank area between the blue rule directly under the headline and the blue rule near the bottom of the slide. Treat both rules as hard boundaries. The main content block must be vertically centered in that blank area with balanced top and bottom padding; do not place it tight against the upper blue rule. Do not let diagrams, tables, text boxes, or main content touch or overlap either rule, the footer, or the page marker.

3. Reconstruct each slide with editable objects.
   - Recreate the primary visible content as native editable PowerPoint objects. A final slide must not contain one large picture that represents the whole source page or most of the source page.
   - Prefer complete PowerPoint shapes over traced line fragments. If the source shows a box, card, process block, table cell, swimlane, or boundary container, create one native shape or table cell for that object; do not reconstruct its border with four separate lines.
   - Group OCR text semantically before placing it. Do not create a separate text box for every OCR word, phrase, or short line when the source shows one sentence, paragraph, bullet group, label, or card. Same-sentence text should live in one text box or in the same containing shape/table cell; same-card text should normally live in that card's text frame.
   - Place text directly inside the containing shape or table cell whenever the visible object is a labeled box, node, banner, callout, or table cell.
   - Do not draw a box and then place a separate text box on top when the text can live inside that box.
   - Treat blue fills, bold percentages, colored words, larger type, and other highlights as emphasis applied to the same text, not as additional content. If the PDF visually highlights a phrase that appears only once semantically, recreate it once with local run styling, cell shading, bold, color, or size changes.
   - Do not overlay a second copy of the same word, percentage, title, or label just to simulate a highlight. Avoid duplicated labels such as a blue shape with `30%` placed on top of a table cell that already contains `30%`.
   - Use native PowerPoint tables for tabular content, including merged cells, header rows, gridlines, fills, and cell-level formatting.
   - Use native PowerPoint shapes for process diagrams, matrices, timelines, arrows, labels, rectangles, connectors, and simple charts.
   - Preserve the source corner style: if the PDF uses straight-corner rectangles, use straight-corner PowerPoint rectangles; use rounded rectangles only when the source uses rounded corners or the template clearly requires them.
   - Black outlines and black table borders are allowed when they match the PDF or improve fidelity. Do not force every line to the template blue.
   - Rebuild simple diagrams faithfully. If the source diagram is a pyramid, hierarchy tree, organization triangle, timeline, or connected box system, preserve the same topology, relative shape, connection logic, and role labels. Resize to fit the template content area, but do not simplify it into a different diagram.
   - For simple source diagrams, "similar idea" is not enough. Copy the source geometry: same number of boxes, same tiers, same outer boundary lines, same connector directions, same support/footer boxes, and same relative alignment. If exact native reconstruction is not yet reliable, use the source page crop only as a temporary reference while iterating; do not deliver a wrong topology.
   - Do not rely on automatic line tracing as the main reconstruction method. Arbitrary detected line segments often create visual noise. Use full shapes, native tables, and typed connectors first; use independent lines only for clear separators, axes, simple underlines, or connectors that cannot reasonably be represented by a container shape.
   - Use PowerPoint elbow connectors for box-to-box relationships. Connectors must attach to shape connection points. Do not fake an elbow connector by stitching together multiple independent straight line segments.
   - When the source uses icon-like graphical elements, use suitable built-in/common PowerPoint-style icons or simple native vector shapes with comparable meaning and visual scale. Keep icons proportionate to the source, not tiny decoration.
   - Use extracted or recreated images only for logos, photos, screenshots, complex illustrations, or elements that are not reasonably editable. Crop raster content tightly and keep it subordinate to editable slide structure; do not use a source page render as a background or full-slide picture.

4. Apply mandatory formatting.
   - Set every text-containing shape and every table cell to a 0.1 cm left inset before text. Use an actual shape/table margin, not leading spaces.
   - Set vertical alignment to middle for all text-containing shapes, text boxes, and table cells unless the template layout clearly requires another alignment.
   - Choose horizontal alignment by content density: center-align short labels, headings, single numbers, percentages, and compact phrases; left-align multi-line sentences, lists, dense descriptions, and long table cells.
   - Remove shadows from all text, text boxes, shapes, pictures, tables, and graphic frames.
   - Remove any visible `NotebookLM`, `NOTEBOOKLM`, or similar source watermark/footer text from the final deck.
   - Keep text readable and contained inside its object; manually adjust font size, line spacing, or object size when needed.
   - Merge OCR fragments into readable sentences and paragraphs before finalizing. Check that editing a sentence in PowerPoint does not require selecting many tiny adjacent text boxes.
   - Match the PDF's content structure, but use the template's visual system and favor editability over pixel-perfect raster tracing.
   - Keep body text generally at 12pt or above. Use 10pt only when dense source content truly cannot fit after layout optimization. Never use text below 10pt.
   - Font size has a minimum, not a target. When the content area has room, enlarge text and shapes so the slide does not look sparse or leave excessive blank space.
   - Balance the page: keep the main content optically and vertically centered in the template content area, avoid large accidental blank zones, and resize/reflow diagrams or tables so text does not run outside shapes or crowd the upper blue rule.
   - Keep every object inside the slide canvas and inside its intended content area. No text, shape, table, line, icon, or connector may protrude beyond the page boundary. If content approaches an edge, shrink, wrap, split, or reposition it.
   - Avoid text overlap by resizing and aligning the underlying shapes first. For connected hierarchy diagrams, child boxes in the same role should normally match the width of their parent or sibling boxes when the source implies equal role/level.
   - Text must never be hidden by another text box, shape, table, or diagram element. After reconstruction, inspect rendered slides for collisions between neighboring labels, titles, and callouts; if any text is obscured or overlaps another text area, reposition, resize, reflow, or split the content before delivery.

5. Verify before delivery.
   - Render the PPTX to images or PDF and compare it with the original page-by-page.
   - Inspect the PPTX object structure and reject any slide whose main content is a full-page or near-full-page picture of the source PDF. A large image is acceptable only when the original slide itself is a photo/screenshot-centric page and the text/labels around it remain editable.
   - Run `scripts/audit_pptx.py` on the generated `.pptx`.
   - Read `references/reconstruction-checklist.md` when the request has strict fidelity requirements or Chinese consulting/proposal deck styling.

## Single-Slide Repair Loop

When the user reports that a specific slide is wrong, treat that slide as a fidelity defect, not as a styling preference. Rebuild only the affected slide unless the fix requires shared assets or masters.

For each repaired slide:

- Open the corresponding rendered PDF page at full size and map the source geometry before editing: title position, major containers, arrows, callouts, table grid, chart/funnel/timeline boundaries, and bottom objects.
- Recreate the page from large structural objects first, then place text inside those objects. Do not approximate a complex page with a generic layout merely because the text content is present.
- Preserve the source topology and visual hierarchy. For funnel, pyramid, timeline, matrix, and process pages, match the number of tiers/segments, relative widths, arrow directions, side callouts, and bottom result boxes before polishing typography.
- After each repair, run `scripts/audit_pptx.py` and inspect object structure for the repaired slide: no full-page pictures, no hidden source page screenshot, no text below 10pt, no obvious text overlap, no `NotebookLM` text, and all key text editable.
- If PowerPoint, LibreOffice, or another renderer is available, export the repaired slide to an image and compare it directly against the source PDF page. Iterate until the rendered slide visually matches the source page's overall structure and spacing.
- If no renderer is available, do a stricter coordinate/object review and explicitly tell the user that visual render comparison could not be performed. Do not claim pixel-level or complete visual match without an actual rendered-slide comparison.
- Keep the final response honest about validation. Static audit proves style/editability constraints, but it does not prove visual fidelity.

## PowerPoint Object Rules

- Shape labels: use the shape's own text frame.
- Shape borders: draw each source card/box/container as one native PowerPoint shape with its own border, not as separate border lines. Use table cells for repeated grid-like boxes.
- Text grouping: one visible sentence, paragraph, bullet group, card label, table-cell value, or diagram-node label should normally be one editable text object or one run/paragraph inside the containing shape. OCR fragments must be merged before placement; avoid many adjacent text boxes that together form one sentence.
- Tables: use real PowerPoint tables, not grouped rectangles, unless the source is decorative and non-tabular.
- Table-like layouts: use tables when rows/columns are aligned, even if some borders are hidden.
- Diagrams: use shapes/connectors for editable logic; group only when it helps user movement/editing. Preserve the source diagram's topology and geometry for simple diagrams.
- Diagram reconstruction should be shape-led, not line-traced. Avoid delivering a diagram made from many ungrouped short lines when it should be editable blocks, cards, arrows, or table cells.
- Connectors: use actual PowerPoint elbow connectors for right-angle box-to-box connections, attached to shape connection points; do not simulate them with separate line segments.
- Corner style: straight-corner source boxes remain straight-corner boxes. Rounded corners are not a default style.
- Line color: black outlines/borders are permitted when they match the PDF; use template blue only when it serves hierarchy or template consistency.
- Shadows: do not apply any shadow effect. If a theme or copied element introduces one, remove it.
- Text margin: set left inset to 0.1 cm for text frames and cells. Also use small top/right/bottom margins when needed, but keep the left inset exact unless matching the source requires a larger inset.
- Alignment: use middle vertical alignment for table cells, text boxes, and shape text frames. Use horizontal center alignment for short/simple content; use left alignment for longer paragraphs, lists, or dense cells.
- Emphasis: represent highlighted source text by styling the original text run or original table cell. Never create duplicate text objects merely to mimic a colored background or visual callout.
- Template hierarchy: use the appropriate template content layout for each content page. Use cover, catalog, section, and back-cover slide types only when the source PDF contains those page roles or the user explicitly requests them; do not flatten distinct source page types into one generic body layout.
- Catalog pages: when creating a catalog page, use the template's existing catalog text boxes/placeholders and include only the major catalog headings. Do not add extra small descriptive agenda text by default.
- Catalog positioning: when creating a catalog page, preserve the original template catalog placeholder positions, dimensions, and alignment. The first catalog entry must stay where the template places it. If entries are numerous, continue on the next line/downward in the existing placeholder rhythm or split to another catalog page; do not shift the whole catalog block.
- Body content area: on content pages, main content must sit between the headline-underbar blue rule and the bottom blue rule. Leave both rules, footer, and page marker unobstructed.
- Body content vertical placement: the main body block should sit in the vertical middle of the blank area between the two blue rules, with clear breathing room above and below. It must not hug the upper blue rule merely because that is the top boundary.
- Watermark cleanup: delete `NotebookLM` footer marks from reconstructed content. Do not recreate source watermarks unless the user explicitly asks.
- Headline size: content-page HEADLINE text must be 24pt, with 22pt or 20pt allowed only when 24pt cannot fit.
- Font size: body text should normally be 12pt+. Dense notes may go to 10pt, but anything below 10pt is a failure.
- Body hierarchy: use 16pt for key-point lead text, 14pt for normal body text, 12pt for dense supporting text/table text, and 10-11pt only for unavoidable dense labels or notes.
- Font scaling: use larger text when the available space permits; avoid underfilled slides caused by treating 12pt as a default instead of a minimum.
- Composition: no text may spill beyond its shape/table cell; the main content block should sit in a visually balanced and vertically centered position inside the template page.
- Text collision: no text box, shape, table, or connector may cover or overlap readable text from another object. This is a delivery failure, not a minor style issue.
- Page bounds: no object or text may exceed the slide boundaries.

## Suggested Implementation Notes

When using Python:

```python
from pptx.util import Cm

TEXT_INSET = Cm(0.1)

shape.text_frame.margin_left = TEXT_INSET
cell.margin_left = TEXT_INSET
```

Set the font for every run:

```python
run.font.name = "Microsoft YaHei"
```

If editing OOXML directly, `0.1 cm` is approximately `36000` EMUs for DrawingML text insets.

## Quality Gate

Before final response, confirm:

- Output is a `.pptx`, not only a PDF or images.
- Final user-facing PPTX is based on the CIIC consulting template in `assets/default-template.pptx` or a newer user-supplied replacement template. Do not accept a blank-deck assembly as the final output for either supported conversion route.
- The deck is genuinely editable: visible text is PowerPoint text, tables are native tables where tabular, diagrams are native shapes/connectors where practical, and page-level raster images are not used as slide content.
- No slide uses a full-page or near-full-page screenshot/render of the source PDF as its primary content. Any raster image is tightly cropped to an inherently raster source element such as a logo, photo, screenshot, or complex illustration.
- Deck is based on `assets/default-template.pptx` or the user-supplied replacement template.
- No cover, catalog, section divider, or back-cover pages were added unless the source PDF includes those page roles or the user explicitly requested them.
- Any source/requested cover, catalog, section, or back-cover page uses the corresponding template layout.
- Any catalog page uses existing template catalog placeholders/text boxes at their original template positions and contains only major directory headings unless detailed descriptions are requested.
- Any catalog entries keep the template's original first-entry position. Extra entries continue downward/onto the next line in the same placeholder rhythm or move to another catalog page; the whole catalog block is not repositioned.
- Deck is 16:9 landscape.
- Content-page headlines are 24pt, or 22pt/20pt only where needed to fit.
- Key-point lead text is 16pt, normal body text is generally 14pt, dense support/table text is 12pt+, and no text is below 10pt.
- Main content on body pages is fully inside the blank area between the headline-underbar blue rule and bottom blue rule, vertically centered in that blank area, and does not touch or cover either rule.
- No object or text breaks the slide boundary.
- No readable text is hidden behind or overlapped by another text box, shape, table, connector, or diagram element.
- All visible text is editable PowerPoint text unless it is embedded inside an inherently raster source element such as a logo, photo, or screenshot.
- Tables are native tables wherever feasible.
- Text in boxes lives directly inside the boxes.
- OCR-derived text is grouped into coherent sentences/paragraphs/cards rather than scattered into many small text boxes.
- Boxes/cards/process nodes are native shapes or table cells, not borders assembled from multiple independent lines.
- Text in tables/text boxes/shapes is vertically middle-aligned; short content is horizontally centered and dense content is left-aligned.
- Highlighted words, percentages, and labels are not duplicated; each semantic item appears once unless the source truly repeats it as separate content.
- Straight-corner source boxes are straight-corner boxes in PPT; rounded corners are used only when present in the source/template.
- Elbow connections use actual PowerPoint elbow connectors attached to boxes, not stitched line segments.
- Simple diagrams match the source topology and geometry, especially hierarchy trees, organization triangles, pyramids, and timelines. Same number of boxes/tiers/boundaries/connectors must be preserved unless the user asks to redesign.
- Icon-like source elements are represented by suitable PPT/native icons at comparable visual scale.
- All fonts are Microsoft YaHei.
- Body text is generally 12pt+, with 10pt as the minimum only for unavoidable dense content; no text is below 10pt.
- Text-containing shapes and table cells use a 0.1 cm left inset.
- No shadows remain on text, boxes, shapes, tables, pictures, or graphic frames.
- No `NotebookLM`/`NOTEBOOKLM` source footer text remains.
- Page composition is visually balanced: no accidental bottom-heavy blank space, off-center main content, content hugging the upper blue rule, text overflowing outside boxes, or overlapping text/text-box collisions.
- Rendered output has been visually compared against the source PDF.

## Resources

- `references/reconstruction-checklist.md`: detailed slide reconstruction and QA checklist.
- `references/yuexiu-style-guide.md`: extracted CIIC/Yuexiu template measurements, typography, palette, and layout-use guide.
- `references/codex-ppt-workflow.md`: merged Codex PPT full-slide-image deck workflow. Read only for explicit image-based deck requests.
- `references/codex-ppt-styles/`: optional Codex PPT visual style references for image-based deck generation.
- `docs/image-model-configuration.md`: Codex PPT CLI/API fallback image-model configuration guide, used only after selecting the image-based workflow and encountering configuration/authentication issues.
- `scripts/audit_pptx.py`: static PPTX audit for shadows, non-YaHei fonts, and common text inset problems.
- `scripts/assemble_ppt.py`, `scripts/image_gen.py`, `scripts/prepare_slide_prompts.py`, `scripts/record_slide_dispatch.py`, `scripts/record_slide_result.py`, `scripts/record_slide_blocker.py`, `scripts/slide_job_status.py`, `scripts/slide_run_state.py`, `scripts/remove_chroma_key.py`, and `scripts/codex_ppt_runtime.py`: merged Codex PPT runtime and assembly helpers for explicit image-based deck workflows.
- `assets/default-template.pptx`: required base template for final generated decks.
- `requirements.txt`: dependency list for the merged Codex PPT image-based workflow helpers.
