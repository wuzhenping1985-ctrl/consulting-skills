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

Read the JSON job file, then follow its `prompt` field exactly. Use the selected image backend and the recorded sample generation method only.
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
Do not edit slide job files, origin_image, speech.md, or assemble the PPT.

Before returning, visually check:
- Chinese text is readable and not garbled
- style matches the approved sample slide
- if the job uses 中智蓝色咨询模板风, it keeps only the blue/pale-blue/white/charcoal/small orange-red color system and does not copy template footers, page markers, logos, city motifs, or bottom slogan bands unless explicitly requested
- if the job is a consulting/report content slide, the main body is text-rich and logic-led with labelled boxes, matrices, flows, comparison frames, or conclusion callouts, not icon-heavy decoration
- if the job is a consulting/report content slide, it is framework-led rather than table-led: the body should visibly encode the job's logic archetype, reasoning path, and framework mapping, such as house/pillar, layered architecture, process lane, causal chain, responsibility boundary, funnel, loop, value chain, interpreted matrix, or comparison columns with convergence
- the slide is not merely a plain table, uniform grid, or set of independent cards; if it could be converted into a Word table without losing meaning, treat it as failed unless the job explicitly asks to preserve source data/table structure
- if the job names a business-blue framework template module, the slide uses that module as structure grammar only, remaps all fills/strokes/labels/backgrounds/emphasis marks to the confirmed deck palette, and does not copy template placeholder text, QR codes, logos, instruction pages, copyright notices, page numbers, unrelated example claims, or original template color styling
- if the job is an ordinary consulting/report content slide, it has medium-high information density and does not leave broad empty whitespace around a small amount of content
- if the job is an ordinary consulting/report content slide, the top slide title/headline is the page storyline and there is no separate visible storyline/core-viewpoint row or prefix
- the slide does not include bottom takeaway boxes, paired bottom text boxes, bottom evidence boxes, bottom conclusion callouts, or a bottom full-width orange-red block plus deep-blue background plus large white-text conclusion strip unless the job explicitly asks for it
- if the slide has a summary viewpoint, it appears in the top headline or in a compact insight band between the title and main body; it is a source-grounded logical judgement rather than a slogan
- there are no unsupported slogans, motivational phrases, decorative golden sentences, empty catchphrases, or bottom-of-page "takeaway" sentences
- if the deck is based on a Word/PDF/text report, all visible claims, labels, recommendations, numbers, and title/headline text are grounded in the job's source basis/evidence; no unsupported external facts or invented content
- if the deck is based on a Word/PDF/text report, visible labels and key points use original report wording wherever feasible; no polished but self-created consulting slogans or source-detached summary claims
- if the deck is based on a Word/PDF/text report, the slide preserves the job's approved source framework. Explicit top-level and sub-level labels such as `一是 / 二是 / 三是`, `中央层面 / 地方层面`, named subsections, and table row groups must remain visible or clearly nested under their original parent section
- the slide does not add a visible extra module, diagnostic panel, matrix, or invented framework that is not present in the job's source framework unless the job explicitly says the user approved that restructure
- required source images are visibly included and not replaced by a similar redraw
- no overlapping or truncated important content

Return only:
backend_used=<built-in image tool OR scripts/image_gen.py>
selected_source=/absolute/path/to/$CODEX_HOME/generated_images/.../ig_*.png
qa_note=<one sentence>
```
