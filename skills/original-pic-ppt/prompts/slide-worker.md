# Slide Worker Prompt

Use this template when dispatching a slide subagent after the sample slide is approved and full-deck generation is authorized.

```text
Generate slide <N> for this codex-ppt deck.

Deck dir: <absolute deck dir>
Slide job file: <absolute deck dir>/prompts/slide_<NN>.json
Output target owned by parent: <absolute deck dir>/origin_image/slide_<NN>.png
Selected image backend: <built-in image tool OR CLI/API fallback>
Sample generation method copied from the approved sample:
- backend_used: <exact backend label recorded by parent>
- tool_name: <image_gen OR image_generate OR scripts/image_gen.py>
- mode: <generate OR edit>
- model/config: <model, size, quality, or "built-in default" if not exposed>
- prompt_source: <approved sample prompt source>
- input_context_preparation: <how local images were made visible or attached>
- approved_sample_path: <absolute path to approved origin_image/slide_XX.png>
- handoff_rule: use this same backend/tool/mode; return a blocker if unavailable
Input images already prepared by the parent:
- <absolute path> - approved sample slide style reference; match style only, do not copy layout
- <absolute path> - strict input asset; preserve labels/data/arrows/content

Read /Users/shampwu/.codex/skills/ppt-art-direction.md and /Users/shampwu/.codex/skills/ppt-content-rules.md before the JSON job. Apply original wording, artistic whole-page composition and purposeful whitespace; tables or matrices require explicit user authorization. Then follow the approved prompt and source mapping. Use the selected image backend and the recorded sample generation method only.
You must produce the final slide candidate by calling the selected image generation backend:
- Built-in mode: use the built-in image generation/editing tool.
- CLI/API fallback mode: use `scripts/image_gen.py` with the saved job prompt and required image inputs.

Forbidden for final slide image creation:
- local drawing or rendering scripts
- Pillow-generated slides
- SVG, HTML/CSS, or canvas screenshots
- python-pptx/PptxGenJS/native PPT layout screenshots
- manually composited text, card, chart, or image overlays

If you cannot use the selected image backend, stop and return `blocker=<reason>` instead of creating a lower-quality replacement.
If you cannot follow the recorded sample generation method, stop and return `blocker=<reason>` instead of switching tools.
Do not edit slide job files, origin_image, any opt-in speech.md, or assemble the PPT.

Before returning, visually check:
- Chinese text is readable and not garbled
- every generated title, body text, label, annotation, caption, citation, chart/table label, Latin string, number, and punctuation mark uses Microsoft YaHei (微软雅黑); reject serif, handwritten, display, monospace, calligraphic, decorative, or fallback fonts; preserve text already baked into a strict supplied image
- style matches the approved sample slide
- if the job uses 中智蓝色咨询模板风, it keeps only the blue/pale-blue/white/charcoal/small orange-red color system and does not copy template footers, page markers, logos, city motifs, or bottom slogan bands unless explicitly requested
- if the job is a consulting/report content slide, the main body is text-rich and logic-led with labelled boxes, matrices, flows, comparison frames, or conclusion callouts, not icon-heavy decoration
- if the job is a consulting/report content slide, it is framework-led rather than table-led: the body should visibly encode the job's logic archetype, reasoning path, and framework mapping, such as house/pillar, layered architecture, process lane, causal chain, responsibility boundary, funnel, loop, value chain, interpreted matrix, or comparison columns with convergence
- the slide is not merely a plain table, uniform grid, or set of independent cards; if it could be converted into a Word table without losing meaning, treat it as failed unless the job explicitly asks to preserve source data/table structure
- if the job names a business-blue framework template module, the slide uses that module as structure grammar only, remaps all fills/strokes/labels/backgrounds/emphasis marks to the confirmed deck palette, and does not copy template placeholder text, QR codes, logos, instruction pages, copyright notices, page numbers, unrelated example claims, or original template color styling
- the page has a clear whole-page composition and purposeful whitespace determined by complete original text; do not require a density target or fill blank space with decorative objects
- if the job is an ordinary consulting/report content slide, the top slide title/headline is the page storyline and there is no separate visible storyline/core-viewpoint row or prefix
- the slide does not include bottom takeaway boxes, paired bottom text boxes, bottom evidence boxes, bottom conclusion callouts, or a bottom full-width orange-red block plus deep-blue background plus large white-text conclusion strip unless the job explicitly asks for it
- if the slide has a summary viewpoint, it appears in the top headline or in a compact insight band between the title and main body; it is a source-grounded logical judgement rather than a slogan
- there are no unsupported slogans, motivational phrases, decorative golden sentences, empty catchphrases, or bottom-of-page "takeaway" sentences
- if the deck is based on a Word/PDF/text report, all visible claims, labels, recommendations, numbers, and title/headline text are grounded in the job's source basis/evidence; no unsupported external facts or invented content
- if the deck is based on a Word/PDF/text report, use the original complete labels and sentences by default; rewriting requires a recorded explicit user request and must preserve all source meaning, required terms, scope, conditions and numbers
- if the deck is based on a Word/PDF/text report, the slide preserves the job's approved source framework. Explicit top-level and sub-level labels such as `一是 / 二是 / 三是`, `中央层面 / 地方层面`, named subsections, and table row groups must remain visible or clearly nested under their original parent section
- if the job contains `source_fidelity_contract`, count the visible peer content modules and match the contract exactly. Render one distinct visible content module for each mapped source item, preserve the parent, core meaning, required terms, and order, and use the approved original visible label and complete message, or an explicitly user-authorized faithful revision. Any added, merged, split, omitted, duplicated, semantically altered, reparented, or reordered source item is a failed candidate
- if the job contains `source_fidelity_contract`, follow each group's `sequence_marker_mode` exactly. In `embedded_text` mode, the approved visible wording is the sole sequence signal and no numeric or alphabetic marker may be added. In `external_marker` mode, render each `external_sequence_marker` exactly once and do not restore removed sequence wording. In `none` mode, add no sequence signal. Never render `visible_order`
- parent headers, connectors, arrows, evidence captions, and decorative separators do not count as peer content modules. Do not use them to hide a source count mismatch
- ordinary content modules use natural labels and complete explanations. Preserve every source level's item count, order, and parent-child relationships; retain necessary objects, actions, relationships, and conditions, and adjust the layout instead of cutting meaning
- first reconcile each visible source item with the approved mapping, then read the rendered page without the source to check that the wording makes sense on its own; the parent must obtain independent read-the-slide review before delivery
- mapped labels and messages retain complete meaning; configured text limits are layout checks, and `text_length_override_note` may record additional space needed for exact wording or complete explanations. Return a layout issue rather than cutting relationships or conditions
- all audience-facing text is source-neutral: it states the supported content directly and does not mention `用户提供`, `你提供的资料`, attachments, filenames, file types, prompts, `source_basis`, `source_evidence`, or the production process; include a neutral document/organization/date citation only when the job explicitly requires source disclosure
- the slide does not add a visible extra module, diagnostic panel, matrix, or invented framework that is absent from the job's source framework
- required source images are visibly included and not replaced by a similar redraw
- no overlapping or truncated important content

Return only:
backend_used=<built-in image tool OR scripts/image_gen.py>
selected_source=/absolute/path/to/$CODEX_HOME/generated_images/.../ig_*.png
qa_note=<one sentence that confirms the Microsoft YaHei check and includes the source-fidelity count result when source_fidelity_contract is present>
```
