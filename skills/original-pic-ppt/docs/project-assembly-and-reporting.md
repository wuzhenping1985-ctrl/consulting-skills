# Project Assembly And Reporting

Read this before initializing the project directory, assembling the PPT, handling an explicit speaker-notes request, or sending the final report.

For every Word/PDF/text report deck, also read `source-fidelity-and-structure-conservation.md` before QA or assembly. Apply its speaker-note rules only when notes were explicitly requested.

## Project Directory

Use this output structure:

```text
{base_dir}/{deck_name}/
├── origin_image/
│   ├── slide_01.png
│   ├── slide_02.png
│   └── ...
├── prompts/
│   ├── slide_01.json
│   └── ...
├── slide_jobs.json
├── slide_run_state.json
├── deck_spec.json
├── outline.md
├── speech.md               # optional; create only after an explicit speaker-notes request
└── {deck_name}.pptx
```

If the user did not specify a destination, use the current working directory or the directory that contains the source file.

You may initialize the directory structure with:

```bash
~/.codex-ppt-skill/.venv/bin/python {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx --init
```

## Quality Check And Repair

Before assembling the PPT, inspect every slide image. Check:

- Text is readable and not garbled.
- Every generated title, body text, label, annotation, caption, citation, chart/table label, Latin string, number, and punctuation mark uses Microsoft YaHei. Reject generated serif, handwritten, display, monospace, calligraphic, decorative, or fallback type. Text already baked into a strict supplied image remains unchanged.
- Slide content matches the outline.
- Title and key points are not truncated.
- Visual style is consistent across slides.
- No page number appears unless the user requested one.
- Important elements do not overlap.
- Consulting/report content pages are not icon-heavy or table-led; the main body uses readable text in source-grounded logical frameworks such as house/pillar structures, layered architectures, process lanes, causal chains, responsibility boundaries, funnels, loops, value chains, interpreted matrices, comparison frames, or conclusion callouts.
- Consulting/report content pages show logical演绎 value: the body reveals hierarchy, causality, sequence, dependency, boundary, convergence, or transformation. A slide that is merely a uniform grid, simple table, or set of independent cards fails unless the outline explicitly preserves a source table.
- Consulting/report content pages are not sparse; ordinary body pages have medium-high information density and do not leave large unused blank areas around a small amount of content.
- Consulting/report content pages use the top slide title/headline as the page storyline and do not add a separate visible storyline/core-viewpoint row or prefix.
- Slides do not include bottom takeaway boxes, paired bottom text boxes, bottom evidence boxes, bottom conclusion callouts, or the removed bottom full-width orange-red block plus deep-blue background plus white-text conclusion strip unless the user explicitly requested that layout.
- If a slide has a summary viewpoint, it appears in the top headline or a compact insight band between the title and main body, and the body supports it. Unsupported slogans, motivational phrases, decorative "金句", or empty catchphrases are failures.
- For Word/PDF/text report sources, slide titles/headlines, key points, labels, recommendations, and numbers are traceable to the approved outline and source basis. If speaker notes were explicitly requested, apply the same traceability check to them. Unsupported external facts or invented conclusions are severe failures.
- For Word/PDF/text report sources, visible wording should be concise and semantically faithful. Regenerate slides that change core meaning, causal direction, conditions, scope, polarity, conclusions, numbers, or required terms; also regenerate slides that copy long report paragraphs when a shorter faithful statement or diagram can carry the same point.
- For Word/PDF/text report sources, check mapped visible labels and messages against `presentation_text_limits`. Accept longer wording only when the mapping contains an approved `text_length_override_note` for required exact text.
- For Word/PDF/text report sources, the slide preserves the approved source framework. Explicit source levels such as `一是 / 二是 / 三是`, `中央层面 / 地方层面`, named subsections, and table row groups remain visible or clearly nested under their original parent section. Missing subheadings, arbitrary regrouping, or extra visible modules not present in the source are severe failures.
- For Word/PDF/text report sources, reconcile every slide against its `source_fidelity_contract`. Count visible peer content modules and verify parent labels, core meaning, required terms, and order. Any added, merged, split, omitted, duplicated, semantically altered, reparented, or reordered source item is a severe failure.
- For Word/PDF/text report sources, reconcile every ordered group against its sequence-marker mode. In `embedded_text` mode, visible sequence wording is the sole sequence signal and any added number, letter, badge, circle, tab, or step marker is a severe failure. In `external_marker` mode, each approved external marker appears exactly once and the visible text contains no sequence wording. In `none` mode, no sequence signal appears. Never render `visible_order`.
- For Word/PDF/text report sources, check that `logic_archetype`, `reasoning_path`, and `framework_mapping` from the outline or job prompt are visible in the slide. If the page could be converted into a Word table without losing meaning, regenerate it with a more explicit framework prompt unless it is intentionally preserving exact source data.
- Audience-facing slide text is source-neutral. If speaker notes were explicitly requested, apply the same check to them. Regenerate or rewrite any wording that says the user supplied material, refers to an attachment, filename, file type, prompt, `source_basis`, `source_evidence`, or describes the production process. If the user explicitly requested citations, use a neutral document title, organization, and/or date instead.
- If a slide uses `assets/business-blue-framework-templates/`, check that the template is used only as a structure reference. Regenerate if placeholder text, QR codes, logo marks, copyright/instruction content, page numbers, unrelated template claims, or original template color styling appear in the slide.

If a slide has severe text or layout issues, regenerate it with a more constrained prompt. If a slide is mostly correct but has a localized issue, use the selected backend's edit capability when available. In CLI/API fallback mode, use `scripts/image_gen.py edit --image {slide_path} --prompt ... --out {new_slide_path}` and replace the final slide only after validating the edited output.

## Speaker Notes: Explicit Request Only

Default behavior:

- Do not create `speech.md`.
- Do not infer that the user wants notes from the presence of a report or outline. Keep necessary supporting explanation visible; notes do not replace it.
- Do not write notes into the `.pptx`.
- Do not include note creation or note QA in completion evidence.
- Ignore an existing `speech.md` during default assembly.

Only when the user explicitly requests speaker notes, presentation notes, narration, a speech script, or PPT remarks:

- Make sure `outline.md` reflects the final confirmed deck outline.
- Create `speech.md` with 1-3 short paragraphs per slide when useful.
- Write presentation-ready narration and avoid filenames, prompt fields, or production-process wording unless formal source disclosure was explicitly requested.
- For Word/PDF/text report decks, keep the notes within the same `source_structure_ledger` and `source_item_mapping`; preserve core viewpoints, required terms, item count, hierarchy, and order.
- Assemble with `--include-speaker-notes`.
- Use Microsoft YaHei for all note text in the `.pptx`.

Use headings that the assembly script can map back to slide numbers in the explicit-notes workflow:

```markdown
## Slide 1: {Title}

{Speaker notes for slide 1}

## Slide 2: {Title}

{Speaker notes for slide 2}
```

## Assembly

Before running `scripts/assemble_ppt.py` or the CLI/API fallback scripts, make sure the shared runtime exists. If `~/.codex-ppt-skill/.venv/bin/python` is missing, or if importing script dependencies fails, create or refresh the environment:

```bash
python3 {skill_root}/scripts/codex_ppt_runtime.py bootstrap
```

This is an internal setup step for the skill. Do not ask the user to run these commands unless dependency installation fails and user approval or troubleshooting is required.

Run:

```bash
~/.codex-ppt-skill/.venv/bin/python {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx --aspect-ratio 16:9
```

The default command never writes speaker notes, even if `speech.md` exists.

When the user explicitly requests speaker notes, run:

```bash
~/.codex-ppt-skill/.venv/bin/python {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx \
  --aspect-ratio 16:9 \
  --include-speaker-notes
```

When the user explicitly asks to preserve the bundled CIIC/中智 PowerPoint template, assemble with:

```bash
~/.codex-ppt-skill/.venv/bin/python {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx \
  --aspect-ratio 16:9 \
  --template {skill_root}/assets/ciic-consulting-2024-template/ciic-consulting-2024-template-16x9.pptx
```

Important:

- `{base_dir}` is the parent directory of `{deck_name}/`.
- `{deck_name}.pptx` must match the project folder name.
- The script reads images from `{base_dir}/{deck_name}/origin_image/`.
- The script only reads final images named like `slide_01.png`, `slide_02.png`, etc.; drafts and sample files are ignored.
- `--template` preserves the template theme, masters, layouts, and page metadata while still placing each generated `slide_XX.png` as the visible full-slide image.
- Do not pass `--template` merely because the visual style is `中智蓝色咨询模板风`; that style is color-only by default.
- Before running assembly, `slide_jobs.json` should show every generated slide as `recorded` and every approved sample slide as `accepted`. If any slide is `pending`, `dispatched`, or `blocked`, stop and report that state.
- Before running assembly for a Word/PDF/text report deck, confirm that the deterministic deck-spec validation and visual source-fidelity audit passed for every included ledger group. Add the speaker-note source-fidelity audit only when notes were explicitly requested.
- The script ignores `{base_dir}/{deck_name}/speech.md` unless `--include-speaker-notes` is passed.
- `--include-speaker-notes` requires a non-empty `speech.md` with recognized `Slide N` or `第 N 页` headings.
- The script writes `{base_dir}/{deck_name}/{deck_name}.pptx`.

`assemble_ppt.py` supports `16:9` and `4:3`. Use `16:9` unless the user requests otherwise. `image_gen.py` loads `~/.codex-ppt-skill/.env` automatically for `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `CODEX_PPT_IMAGE_MODEL`. Run `python3 {skill_root}/scripts/codex_ppt_runtime.py doctor --check-api` when troubleshooting API access.

## Final Report

Report:

- Project directory
- PPT file path
- Slide image directory
- `outline.md` path
- `slide_jobs.json` path
- Number of slides
- Confirm which image backend was used and that every non-sample slide result was recorded with `record_slide_result.py`.
- Confirm that the global Microsoft YaHei font-family check passed for all generated slide text; include the notes font check only when notes were explicitly requested.
- Confirm which PPT template was used for assembly, if `--template` was passed.
- Include the `speech.md` path and confirm note embedding only when speaker notes were explicitly requested.
- Any slides that were regenerated, blocked, or still have known limitations

## Prompting Principles

- Keep one global visual style fixed across the deck.
- Keep Microsoft YaHei as the sole font family for all generated text across every visual style; express style differences through size, weight, color, alignment, spacing, texture, and composition.
- Vary slide composition by page role; style consistency does not mean repeating the same layout.
- Use `layout_blueprints` as candidate patterns, not mandatory templates.
- Generate one slide per image request.
- Prefer concrete visual direction over generic words like "beautiful" or "professional".
- For dense content, use continuation slides while preserving stable source group and item ids, core meanings, required terms, parent-child relations, and source order.
- Prioritize clarity over decoration.
- For consulting/report decks, prefer text-rich framework demonstration over decorative icons; use icons only as rare functional markers.
- For consulting/report decks, keep text readable and complete in its original hierarchy. Let the source content determine density; do not add, split, merge, omit, or shorten items to fill the usable body area.
- For consulting/report decks, do not default to simple tables or uniform card grids. First identify the source logic, then choose a framework that makes hierarchy, causality, sequence, responsibility boundary, convergence, or transformation visible.
- When using the bundled business-blue framework templates, choose the module that fits the source logic and map source points to its roles. Recolor the module to the confirmed deck palette, defaulting to 中智蓝色咨询模板风; do not force a roof, platform, radial, cycle, process, or timeline layout when the source relationship does not match.
- For consulting/report decks, make the top slide title/headline carry the page storyline and avoid separate storyline/core-viewpoint rows, bottom slogan bands, bottom takeaway boxes, and paired bottom text boxes.
- For consulting/report decks, place any real summary viewpoint in the title or near the top of the body, and make it a source-grounded logical judgement rather than a slogan.
- For decks based on Word/PDF/text reports, treat the report as the content boundary. Improve visual clarity while retaining the source structure at every level; do not add, split, or merge points to fill the page.
- For decks based on Word/PDF/text reports, treat the report's framework as a content boundary too. Keep the source hierarchy and section order unless the user approved a new structure; use visual diagrams to express that hierarchy, not to replace it.
- For decks based on Word/PDF/text reports, preserve exact source group cardinality at every level and one-to-one item mapping. Select or adapt layouts to the source count and reject any layout that adds, merges, splits, omits, duplicates, semantically alters, reparents, or reorders source items.
- For decks based on Word/PDF/text reports, use one sequence signal per mapped item and one sequence-marker mode across each source group. Preserve embedded sequence wording without an external marker, or remove that wording before using an external marker.
- For decks based on Word/PDF/text reports, write natural labels and complete explanations. Retain necessary relations and conditions; use a different layout or a clearly linked continuation when needed. Before delivery, complete a source-by-source structure check followed by an independent review of the rendered wording; any failure requires repair and re-review.
- Keep every delivery-facing artifact source-neutral. Use internal provenance fields for traceability, but do not expose user/attachment/file/process wording in slides, handouts, delivery summaries, or explicitly requested speaker notes. When citations are explicitly requested, attribute the document, organization, or date neutrally.
