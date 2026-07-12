# Report-To-Deck Checklist

Use this checklist before delivering a PPTX created from a PDF or Word report.

## Routing

- PPT-like PDF inputs that should be converted one-to-one are routed directly to `pdf-to-editable-ppt`.
- Text-heavy Word/PDF/report inputs follow the three-stage route: Codex PPT image deck, image deck PDF export, then `pdf-to-editable-ppt` editable reconstruction.
- If the input type was ambiguous, the source was inspected before choosing the route.
- For the text-heavy route, the intermediate image PPTX and intermediate PDF exist, and the final delivered file is the editable PPTX reconstructed from that PDF.
- For both routes, the final delivered PPTX uses the CIIC consulting template. A Codex PPT image assembly is allowed only as an intermediate artifact or explicitly requested image-only companion, not as the normal final deliverable.

## Content Logic

- The deck is synthesized from the report; it is not a page-by-page dump.
- Slide titles are message-led conclusions or clear content headings.
- The deck outline has a cover, catalog, sections, body slides, and closing/back cover where appropriate.
- Executive summary captures the report's key findings, conclusions, and recommendations.
- Key facts, numbers, dates, and names match the source.
- Claims not supported by the source are removed or marked as assumptions.
- Dense source tables are summarized on body slides and preserved in appendix/notes when useful.
- For substantial decks, the outline identifies each slide's number, action title, 3-5 key points, role, visual idea, candidate layout/model, required source assets, and speaker-note intent.
- Required source figures, screenshots, charts, or tables are mapped to specific slides before building.

## Template And Style

- The deck is based on `assets/base-ciic-yuexiu-template.pptx` unless the user supplied another template.
- The final routed deliverable is template-based even when an intermediate image deck was used.
- `references/yuexiu-style-guide.md` has been followed.
- The cover is formal and uncluttered: title, subtitle/topic/client/project, date/team/source line where available, and template brand/background only.
- The cover does not contain body-slide analysis objects such as "core thesis" labels, executive-summary claims, KPI cards, diagnostic boxes, evidence tables, charts, or model-library framework diagrams unless the user explicitly requested an analytical cover.
- Content-page titles are 24pt by default, with 22pt/20pt only for fit.
- Key-point leads are about 16pt; normal body text is about 14pt; dense support/table text is 12pt+ where possible.
- Main content stays between the upper and lower blue rules.
- Footer, page marker, blue rules, and section decorations are not covered.
- Right-bottom page numbers/page markers come from the base template only; no extra manually drawn duplicate page number or orange marker has been added.
- Colors follow the blue-led CIIC/Yuexiu palette.
- No broad orange fills; orange is only a small accent.
- No shadows.
- The deck has one coherent visual identity: stable palette, typography, spacing, icon/diagram language, and page rhythm.
- Page layouts vary by slide role. Cover, catalog, executive summary, diagnosis, evidence, framework, process, roadmap, recommendation, risk/control, and appendix pages do not all repeat one generic card layout.

## Codex PPT Compatibility

- For text-heavy inputs, `references/codex-ppt-image-workflow.md` was used to create the intermediate image-based deck.
- The intermediate image deck follows Codex PPT rules: outline, style/backend confirmation where required, sample slide, slide generation, QA, and notes.
- The intermediate image deck was exported to PDF by PowerPoint/LibreOffice or by `scripts/codex_ppt_images_to_pdf.py` from `origin_image/slide_XX.png`.
- The final editable PPTX was produced by applying `pdf-to-editable-ppt` to that intermediate PDF.
- Full-slide images are allowed only in the intermediate image deck/PDF. They are not acceptable as the final editable consulting PPT body.

## Model Library Use

- Model-library page structures are used for content slides, not for cover/catalog/back-cover decoration unless explicitly requested.
- A suitable model-library page has been considered for each正文/content slide before using a plain base-template layout.
- A model was selected because its logic fits the report content.
- Generic page models from `page-design-collection-20160624.pptx` are used for layout/composition reference when no dedicated business framework model fits.
- Instruction/copyright/QR/font/color tutorial pages from the model decks are not included.
- All model placeholder text has been replaced with source-specific text.
- No model-library example business content remains accidentally.
- Copied/adapted diagrams remain editable where feasible.
- The selected model has been restyled to match the base CIIC/Yuexiu deck.

## Editability

- Text is editable text, not raster screenshots.
- Tables are native PowerPoint tables where practical.
- Diagrams are native shapes/connectors where practical.
- Text lives inside its shape or table cell.
- Text boxes, shape text frames, and table cells have automatic text wrapping enabled.
- Connectors attach to shapes when the diagram shows relationships.
- Images are used only for source photos, screenshots, logos, complex figures, or non-editable source artwork.
- No full-slide generated image or full-slide screenshot remains as the main content of the final editable consulting slide.

## Chart And Data QA

- Every numeric visual has a declared or inferable scale that matches the comparison being made.
- Directly comparable values share one absolute scale; a larger value never appears as a shorter/smaller bar, line position, segment, bubble, or gauge mark than a smaller value in the same comparison set.
- Normalized, indexed, or separately scaled charts are explicitly labeled as such and are not placed where viewers will read them as absolute comparisons.
- Manually drawn charts have been checked after render against the source numbers, including bar lengths, segment widths, line points, ranks, percentages, labels, and callout values.
- Axis labels, units, and scale notes are readable and do not contradict the visual geometry.

## Visual QA

- No text spills outside shapes or table cells.
- No text overlaps another object.
- Wrapped text remains readable, with intentional line breaks only where they improve meaning or visual rhythm.
- No objects exceed the slide canvas.
-正文/content pages use the body area actively and do not leave excessive unused blank space. Sparse pages are enlarged, combined, or rebuilt with a richer model layout.
- Dense slides are split or simplified rather than shrinking text below 10pt.
- Slides are visually balanced and not crowded against the top rule.
- Section dividers, catalog pages, and back cover are consistent with the base template.
- Body pages have only the template-provided right-bottom page number/page marker.
- Speaker notes are included when requested or useful for delivery, and they match the final slide order/messages.
- The final output is `.pptx`.
- `scripts/audit_pptx.py <deck.pptx>` has been run and warnings have been reviewed.
