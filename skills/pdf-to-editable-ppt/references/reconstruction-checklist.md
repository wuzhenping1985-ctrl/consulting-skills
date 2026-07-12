# Reconstruction Checklist

Use this checklist when converting a PPT-style PDF into an editable PowerPoint deck.

## Template First

- Build the final PPTX from `assets/default-template.pptx` unless the user supplies a newer template.
- This template requirement applies to both supported conversion routes: direct PPT-like PDF reconstruction and final reconstruction after report-to-PPT synthesis.
- Preserve and use the template content slide roles: `内页版式-基础`, `1_内页版式-基础`, `内页版式-左右等分`, `内页版式-左右1:2`, `内页版式-左右2:1`, `内页版式-左中右三分`, `内页布局-右侧强调`, `1_内页布局-右侧强调`, `内页布局-左侧强调`. Use `封面`, `目录`, `章节`, and `封底` only when the source PDF contains those page roles or the user explicitly requests them.
- Use the template's blue-led corporate palette and layout rhythm instead of recreating a blank black-and-white PDF copy.
- Read `references/yuexiu-style-guide.md` when title size, column proportions, page geometry, or CIIC/Yuexiu proposal style must be matched precisely.
- Adapt each reconstructed PDF page into the template content area. Keep the source logic, but let the template control titles, spacing, colors, headers, footers, and final polish.
- On catalog pages, when present in the source or explicitly requested, use the template's existing catalog text boxes/placeholders at their original positions and sizes. Include only main catalog headings by default; omit small descriptive lines unless the user asks for a detailed agenda. Do not move the first catalog entry or shift the whole catalog block. If entries are numerous, continue on the next line/downward within the original placeholder rhythm or split to another catalog page.
- On content pages, place all main content inside the central blank body area between the blue rule directly below the headline and the blue rule near the slide bottom. Treat both blue rules as hard boundaries. Keep the main content vertically centered in that blank area with balanced top and bottom padding; do not let it hug the upper rule. Do not overlap the upper rule, lower rule, footer, or page marker.
- By default, rebuild only source content pages. Do not add a template cover, agenda/catalog, section divider, or back cover unless the source PDF contains that page role or the user explicitly requests it.

## Source Analysis

- Record PDF page count and rebuild the source content in reading order unless the user asks otherwise.
- Identify repeated layout components: cover, section divider, title slide, content slide, appendix, page number, logo, confidentiality text.
- Build shared slide styles from the template first, then apply them consistently.
- Extract available text, images, and vector elements, but validate against the rendered PDF because extraction order can be wrong.
- Identify and remove source watermarks or generation marks such as `NotebookLM` / `NOTEBOOKLM`.
- Distinguish source emphasis from repeated content. A blue fill, bold percentage, colored word, or larger font may be only a visual highlight, not a second semantic item.
- Identify corner style, connector style, and diagram topology. If source boxes are straight-corner rectangles, keep them straight. If source connections are right-angle elbow connectors, rebuild them with actual elbow connectors.
- For simple diagrams such as organization triangles, pyramids, hierarchy trees, timelines, and connected box systems, map the source topology before drawing and preserve that topology in PPT. Preserve same box count, tier count, outer boundary lines, connector directions, lower support boxes, and relative alignment.

## Fidelity Priorities

1. Correct content and slide order.
2. Editable structure: text, tables, shapes, connectors.
3. Template fit and visual quality: hierarchy, alignment, color, relative spacing, line weight, balanced page composition.
4. Fine positioning and typography.

Do not sacrifice editability just to create a pixel-perfect screenshot deck.

## Mandatory Layout Rules

- Slide size: landscape 16:9.
- Font: Microsoft YaHei/微软雅黑 for all normal Chinese body text, headings, labels, tables, footers, and chart labels. Use Impact only for large standalone KPI numerals when matching the template style.
- Headline: content-page headline is 24pt; reduce to 22pt or 20pt only when 24pt does not fit.
- Body hierarchy: key-point lead text is 16pt, normal body text is 14pt, dense supporting/table text is 12pt preferred, and 10-11pt is allowed only when unavoidable after reflow.
- Shadows: none on any text, text box, shape, picture, table, group, or graphic frame.
- Text inset: use a 0.1 cm left margin before text in every text-containing shape and table cell.
- Alignment: set text vertically to middle in every table cell, text box, and shape text frame unless the template layout clearly requires another alignment. Use horizontal center alignment for short labels, numbers, percentages, and compact phrases; use left alignment for dense descriptions, lists, and multi-line content.
- Template: use the base template layouts and color system; do not output a plain white deck when the template exists.
- Body content area: main body content must not touch or cover the blue rule under the headline or the bottom blue rule. These are hard boundaries, not approximate guides.
- Body content vertical placement: the main content block must sit in the vertical middle of the blank area between the two blue rules. If it appears pinned to the top rule, lower/rebalance it before delivery.
- Page bounds: no body text, shape, table, line, connector, or icon may extend beyond the slide canvas.
- Watermark: remove any `NotebookLM` or similar source footer text.
- Font size: keep body text at 12pt or above whenever possible. Use 10pt only when dense content cannot fit after reflow. Never use text below 10pt.
- Font scale: 12pt is a minimum guideline, not the normal default. Enlarge text and objects when there is enough room so slides do not look sparse.
- Composition: ensure every slide's main content is optically and vertically centered within the template content area. Avoid accidental large blank zones, bottom-heavy pages, content crowded against the upper blue rule, and shapes whose text spills outside.
- Text collision: no text box, shape, table, connector, or diagram element may cover or overlap readable text from another object. Inspect rendered slides for collisions between titles, labels, callouts, and neighboring text areas; fix by repositioning, resizing, reflowing, or splitting content.
- Avoid manual leading spaces for indentation.
- Avoid nesting a separate text box on top of a shape when the shape itself can contain text.
- Avoid duplicated text created only for emphasis. If a label or percentage is highlighted in the source, style the original run/cell/shape instead of adding an overlaid duplicate.

## Tables

- Use native PowerPoint tables for financial tables, project plans, comparison matrices, responsibility matrices, risk lists, calculation grids, and any aligned row/column structure.
- Preserve merged cells, header bands, alternating fills, borders, row heights, column widths, and alignment.
- Put text directly in cells.
- Set cell left margin to 0.1 cm.
- Set table-cell vertical alignment to middle.
- Center-align short table headers, category labels, single numbers, and percentages. Left-align long explanatory cells or cells with multiple lines.
- Table and box outlines may be black when the PDF uses black lines or when black improves fidelity. Do not force table borders to blue.
- Use table cell fill, font color, bold, and size to highlight important cell content. Do not overlay another shape containing the same cell text.
- Do not shrink table text below 10pt. If a table will not fit, split it across slides, simplify wording, or use a template appendix/table layout.
- If a table is too visually complex for one native table, split into a small number of aligned native tables or combine a native table with minimal decorative shapes.

## Shapes And Diagrams

- Use rectangles, rounded rectangles, lines, arrows, connectors, brackets, and callouts as native objects.
- Put labels directly inside shape text frames.
- Set shape/text-box vertical alignment to middle. Center-align compact labels; left-align dense prose.
- Preserve source corner style. Straight-corner source rectangles stay straight; do not convert them to rounded rectangles by default.
- Use actual PowerPoint elbow connectors for right-angle connections. Attach connector endpoints to shape connection points. Do not compose elbow lines from separate straight segments.
- For connected hierarchy diagrams, equal-level or same-role boxes should use consistent width and alignment. Child boxes should match the relevant parent/sibling width when the source implies the same role or column.
- If text overlaps inside a box, widen the box or reflow the layout before reducing font size. Keep related box widths consistent, for example a child description box should align to the box directly above it when the source implies that relationship.
- Match fills, outlines, corner radius, and line weights while staying within the template palette.
- Use groups sparingly; users should still be able to edit meaningful pieces.
- Use images only for logos, photos, screenshots, complex icons, or unavailable source artwork.

## Icons

- Source icon-like elements may be rebuilt with common PPT/native icons or simple editable vector shapes.
- Match icon meaning and relative scale. Icons should be large enough to read and proportionate to the original PDF; do not shrink them into decorative marks.
- Keep icon style consistent across a slide.

## Simple Diagram Fidelity

- For simple diagram pages, prioritize shape/topology fidelity over reinterpretation.
- Organization triangles must preserve the triangle boundaries, top role, middle roles, lower support roles, internal horizontal/vertical lines, and connector structure. Do not substitute a merely similar hierarchy chart.
- Pyramids must preserve tier order, tier widths, and side callout connections.
- Timelines must preserve the main axis, node count, and node-to-label relationships.
- Connected box systems must use attached connectors and visually terminate at the correct source/target shape.
- Funnel or staged-validation pages must preserve the source sequence, outer funnel boundaries, internal colored band, vertical arrow stack, side proof/callout boxes, lower risk-check row, and final result box. Rebuild these from large native shapes first; only then add text.

## Text

- Match hierarchy: title, subtitle, section label, body, note, footnote.
- Content-page headlines: 24pt, or 22pt/20pt only if needed to fit.
- Use 16pt for key-point lead text, 14pt for normal body text, and 12pt+ for dense table/supporting text wherever possible.
- Keep line breaks and bullet hierarchy close to the PDF when it improves comprehension.
- When the source visually emphasizes a word, number, or phrase that appears only once, keep it as one editable text item and apply local styling. Do not repeat it nearby or on top of itself.
- Adjust font size or shape dimensions so text does not overflow.
- Check that text is not hidden behind another text box/shape and does not overlap neighboring text. This is especially important for dense diagrams, title labels, and multi-box layouts.
- Prefer reflowing content, increasing shape height, splitting dense content, or using a second slide before reducing below 12pt.
- If the slide has ample whitespace, increase body text size and object scale rather than leaving the page underfilled.
- If source text is unclear, mark uncertain text in speaker notes or ask for clarification instead of inventing content.

## Verification

- Render the rebuilt PPTX and compare against the PDF page by page.
- Check slide count and page order.
- Check that the final deck uses the template's layouts and color system.
- Check that no cover, catalog, section divider, or back-cover pages were added unless they exist in the source PDF or were explicitly requested by the user.
- Check catalog pages, if present: main directory text is in existing template catalog placeholders/text boxes at the original template position; no unnecessary small explanatory agenda text.
- Check catalog pages, if present: the first catalog entry has not moved from the template's intended position. Extra entries continue downward/onto the next line in the same placeholder rhythm or move to another catalog page.
- Check body pages: all main content sits between the headline-underbar blue rule and the bottom blue rule, is vertically centered in that blank area, and does not collide with either line.
- Check slide bounds: no object, text, table, connector, or icon extends past the page edges.
- Check content-page HEADLINE size: 24pt, or 22pt/20pt only where needed.
- Check body hierarchy: key-point leads are about 16pt, normal body text about 14pt, dense table/support text 12pt+, and no text below 10pt.
- Check that key tables and diagram boxes are editable.
- Check that highlighted words, labels, and percentages are not duplicated. Examples to catch: a repeated `作战单元获取池（55%—60%）` above the same box title, or a blue `30%` overlay on a table cell that already includes `30%`.
- Check text alignment: all table cells/text boxes/shape text frames are vertically middle-aligned; short content is horizontally centered; dense content is left-aligned.
- Check source corner style: straight boxes remain straight; rounded corners are not introduced by default.
- Check connectors: right-angle connections use attached elbow connectors, not stitched line segments.
- Check simple diagrams: organization triangles, pyramids, timelines, and hierarchy diagrams match the source topology and relative shape. For the PDF page 9-style organization triangle, compare against the source at full size; same triangle boundaries, role boxes, support/footer boxes, and connector structure are required.
- Check icons: icon-like elements are present at comparable source scale and are not too small.
- Check whitespace: when a content box has excess whitespace, increase text/object scale rather than leaving a sparse slide.
- Check there is no `NotebookLM` / `NOTEBOOKLM` text.
- Check no text is below 10pt, and review any text below 12pt.
- Check each slide at full size for text overflow and visual balance.
- Check each slide at full size for text/text-box overlap, including cases where a text box covers a nearby title or label.
- Run `scripts/audit_pptx.py <deck.pptx>`.
- Manually inspect any audit warnings; static checks are conservative and cannot prove visual fidelity.

## Single-Slide Repair

Use this loop when the user reports that one slide is wrong or "乱套了":

- Identify the exact source PDF page and rebuilt PPT slide.
- Freeze unrelated slides; do not rewrite the whole deck unless the defect comes from shared master/template logic.
- Reopen the source page at full size and list the major geometry: title, top object, central object, arrows/connectors, side callouts, lower object groups, and final/bottom statement.
- Rebuild the slide by matching geometry first, not by fitting the text into a convenient generic layout.
- Run `scripts/audit_pptx.py` after each repair and reject warnings for text overlap, font below 10pt, non-YaHei fonts, source watermark text, shadows, or missing text margins.
- Inspect repaired slide object counts: page-level pictures should be zero unless the source page is inherently photo/screenshot-based; key text must be editable text.
- If a renderer is available, export the repaired slide and compare it visually against the source PDF page. Iterate until the rendered slide matches the source page's overall structure, object order, and spacing.
- If a renderer is not available, say so. Coordinate and static-object checks are necessary but not sufficient to claim complete visual equivalence.
