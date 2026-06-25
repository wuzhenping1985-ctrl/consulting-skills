# Outline, Style, And Sample

Read this before writing or updating `outline.md`, offering visual styles, using files from `references/`, or generating/approving the sample slide.

If the user asks to save a finished deck style or a user-supplied image/PDF/PPT/PPTX style for future reuse, read `style-library.md`.

## Plan The Deck Outline

Create a concise `outline.md` draft before generating images. For each slide, define:

- Slide number
- Slide title / headline, which is the page storyline shown at the top of the slide
- 3-5 key points
- Source basis for Word/PDF/text report decks: the report section, paragraph, table, figure, or user-provided asset that supports the slide
- Source framework for Word/PDF/text report decks: the original top-level section and sub-level labels that the slide must preserve, such as `一是 > 中央层面 / 地方层面 / 因此`
- Optional visual idea
- Layout role and intent, such as cover, agenda, section divider, concept explanation, process, comparison, timeline, data evidence, architecture, case study, summary, or Q&A
- Logic archetype for every normal consulting/report content slide, such as house/pillar framework, layered architecture, process lane, causal chain, responsibility boundary, evidence-to-insight funnel, closed loop, value chain, interpreted matrix, or comparison columns with convergence
- Reasoning path for every normal consulting/report content slide, showing the source-grounded logic the reader should follow
- Framework mapping for every normal consulting/report content slide, explaining how source points map to visual roles such as roof, pillars, foundation, lanes, stages, axes, boundary zones, loop nodes, or convergence points
- Why-not-table note for every normal consulting/report content slide, unless the slide is intentionally preserving a source table or exact data
- Content density for ordinary consulting/report pages, including enough short text units or labelled cells to avoid a sparse body page
- Required source images, if any, including the image path or attachment name, its role on the slide, and whether it is a strict input asset or only a style/layout reference

For Chinese consulting/report decks, also assign each content slide a logic display type before generation. Prefer framework-style logical exposition: house/pillar frameworks, layered architectures, process lanes, causal chains, responsibility-boundary frames, evidence-to-insight funnels, closed loops, value chains, interpreted matrices, and comparison columns with convergence. Read `references/框架演绎版式规则.md` when planning from a Word/PDF/text report. Normal content slides should be medium-high to high density, with the body zone mostly occupied by readable argument text inside a structure that makes hierarchy, causality, sequence, dependency, boundary, or transformation visible. Plan 10-16 readable Chinese text units or an equivalent source-grounded framework/matrix when the source supports it, and include compact explanatory sentences rather than only noun labels. The page storyline is the top slide title/headline itself, such as `华润案例：价值创造型总部与分层分类授权`; do not plan or render a separate visible line labelled `STORYLINE` or `STORYLINE：`. If a slide needs a summary viewpoint, place it in the title or a compact insight band immediately below the title and above the main body; the viewpoint must be a source-grounded logical conclusion, implication, cause-effect judgement, or decision criterion. Avoid planning pages whose main body is a simple table, plain 2x2/2x3 grid, repeated equal-weight cards, icon row, icon-only card set, repeated icon bullet rows, sparse single-card composition, bottom slogan band, bottom takeaway/callout boxes, paired bottom text boxes, unsupported slogan-like "金句", or scattered small pictogram elements unless the user explicitly asks for that style.

For text-report decks, simple tables are not the default answer. Use a table only when the source contains exact rows/columns, data, or a true comparison that would be distorted by another structure. Otherwise, turn source points into a framework with visible roles: roof/foundation/pillars, levels, lanes, gates, loop nodes, boundary zones, axes, or convergence points. The transformation must remain faithful to the report; do not invent dimensions, conclusions, causes, or recommendations to make a framework look richer.

If the user asks to use the attached business-blue framework templates, read `references/商务纯蓝框架模板库.md` and choose a template module only when it matches the source logic. Add these fields to the affected slide outline:

- Template reference module: 屋顶图 / 多层平台 / 中心发散 / 循环逻辑 / 业务流程 / 时间轴流程 / 页面整理库
- Template reference asset: relevant contact sheet or preview path under `assets/business-blue-framework-templates/previews/`
- Structure mapping: source-grounded mapping to roof/pillars/foundation, platform layers, center/outer nodes, loop nodes, process steps, or timeline stages
- Style scope: structure reference only; do not copy template content, logos, QR codes, instruction pages, non-source claims, or original template color styling
- Color mapping: remap all template fills, strokes, labels, backgrounds, and emphasis marks to the confirmed deck palette; default to 中智 blue / pale-blue / white / charcoal with small orange-red accents, not the source template's original colors

When the source is a Word/PDF/text report, the outline must be source-grounded. Read and extract the report before outlining. Use the report's wording, stated findings, tables, figures, numbers, definitions, named entities, and explicit recommendations as the only content source unless the user explicitly requests external enrichment. The outline may summarize, group, reorder, deduplicate, or translate prose into consulting logic structures, but it must not invent facts, cases, benchmarks, management diagnoses, risks, or recommendations that are not in the report. Prefer original source phrases for slide titles, level labels, node labels, judgement questions, and conclusion phrases. Paraphrase only when needed for length, and keep the original terms and hierarchy visible. When translating prose into a framework, document how each source point maps into the visual structure so the framework is analytical rather than decorative.

The outline must also be source-framework-faithful. Before drafting slide roles, reconstruct the source document's hierarchy as a `source_structure_map`: headings, numbered points, named sub-sections, paragraph order, and table/figure row groups. Preserve that hierarchy in the slide plan unless the user explicitly approves a different framework. Treat explicit labels such as `一是 / 二是 / 三是`, `中央层面 / 地方层面`, `首先 / 其次 / 因此`, table row categories, and named subheadings as structural content, not disposable wording.

Do not convert nested source logic into arbitrary peer bullets. If the source says one top-level point contains `中央层面` and `地方层面`, the slide must show those two sub-levels under that same point, not replace them with a flat list of six self-invented bullets. If the source has three stated points, do not add a fourth visible module, diagnostic matrix, "检审切入点" panel, or root-cause map unless that module is explicitly present in the source or the user has approved the addition. Source-supported details must remain under their original parent section.

Do not create attractive but disconnected summary sentences. If the report has a `归纳起来` sentence, it may appear only as the source's own summary and must be visibly connected back to the sections it summarizes. If the report does not contain the summary wording, do not place it as a headline, bottom slogan, or conclusion band.

For report-grounded decks, every slide in `outline.md` should include a short `Source basis` line, such as:

```markdown
Slide 4: 模式框架：组织形态与管控力度共同决定管控模式
- Source basis: 第2章“组织管控模式分类”第3-6段；表2“管控模式比较”
- Logic archetype: house/pillar framework
- Reasoning path: 组织形态差异 -> 管控力度选择 -> 管控模式形成 -> 授权边界判断
- Framework mapping: roof=管控模式判断；pillars=组织形态、管控力度、业务复杂度；foundation=制度与授权基础
- Why not table: 原文要表达支撑关系和边界形成逻辑，简单表格无法体现从条件到模式的演绎路径
- Key points: ...
```

If the report does not support a proposed slide or storyline, remove that slide, merge it into a supported page, or ask the user whether to add external analysis. Do not silently fill gaps with general consulting knowledge.

If the proposed slide structure does not match the source framework, redesign before showing the outline. Visual devices such as flows, matrices, triangles, funnels, or radial maps are permitted only as containers for the source hierarchy. They must not become a new visible logic system that competes with or overwrites the report's own framework.

Save the draft to `{base_dir}/{deck_name}/outline.md` once the project directory is known. If the output directory is not known yet, show the outline in chat first and write it to `outline.md` immediately after creating the project directory.

Show the outline to the user for confirmation and wait for approval before moving to backend confirmation or image generation, unless the user explicitly asked you to skip confirmation. The default visual style is `中智蓝色咨询模板风` and does not require a separate style-selection approval. If any slide lists required source images, explicitly ask the user to verify that each image is assigned to the correct slide and role before generation. If the user requests changes, update `outline.md` and ask for confirmation again.

Stop after writing the outline draft. At this point, report the `outline.md` path, slide count, required source images and their slide mapping, and that no slide images or PPTX have been generated yet. Do not proceed to `deck_spec.json`, `speech.md`, prompt preparation, backend selection, or sample generation until the user approves the outline.

If the user approved a sample slide, record that approved `slide_XX.png` path as the deck-level style reference. Later slide prompts and subagent handoffs should include it as a style-only reference so each page keeps the same palette, typography mood, density, texture, and visual identity without copying the sample's exact layout.

Recommended structure:

```text
Slide 1: Cover
Slide 2: Context / problem
Slide 3-7: Main argument or sections
Slide 8: Summary / recommendation / closing
```

For slides that use source images, add lines like:

```markdown
Slide 5: Experiment Results
- Key points: ...
- Required images:
  - Main evidence figure; strict input asset; preserve data, axes, labels, legends, colors, and values

    ![Result 01](assets/figures/result_01.png)

  - Supporting model architecture; strict input asset; preserve labels and arrows

    ![Model Architecture](assets/figures/model_architecture.png)
```

Use Markdown image syntax inside the `Required images` list whenever the asset is local and renderable in the outline. This lets the user visually verify the exact asset mapping during outline review. Keep the descriptive text next to each image so `prepare_slide_prompts.py` can convert the same asset into structured prompt input later.

## Apply The Default Visual Style

Before generating slide images, apply `中智蓝色咨询模板风` as the default color-only style unless the user explicitly asks for another visual style, supplies a style reference, or asks to replicate a full template layout. This default style is pre-approved; do not stop to ask the user to confirm it each time.

If the user has specified a different style, provided a style image, or provided a PDF/PPT/PPTX to use as style reference, do not force a 2-3 option style selection. Extract the usable style rules, briefly restate them, then proceed to backend confirmation and sample generation.

For PDF/PPT/PPTX style references, do not infer the visual system from document structure, outline text, XML, file metadata, or slide object hierarchy alone. First render or export representative pages/slides into real page images, inspect those rendered images, and derive the style from what is actually visible on the pages. If the file has multiple visual sections, inspect enough representative pages to capture the shared style and any section-specific variations.

When extracting style from reference material, separate content reuse from style reuse. Unless the user explicitly asks to reuse the source content, treat the provided image/PDF/PPT/PPTX as a style reference only.

Default local template-derived style: this skill includes the CIIC Consulting 2024 16:9 template at `assets/ciic-consulting-2024-template/ciic-consulting-2024-template-16x9.pptx` and the extracted reusable color-only style `references/中智蓝色咨询模板风.md`. For every deck, read `references/中智蓝色咨询模板风.md` and use it as the default **color-only** style without offering unrelated alternatives, unless the user explicitly requests another style. Briefly restate the applied style rules, including that only the 中智 blue/pale-blue/white/charcoal/small orange-red palette is retained; any referenced framework template is recolored into this palette rather than inheriting its original colors; the top title/headline is the page storyline and no separate storyline/core-viewpoint row should be added; content pages should use medium-high to high information density, more readable text, no decorative icons by default, more logic demonstration boxes, no large blank body areas, no bottom takeaway/callout boxes, and no bottom deep-blue conclusion slogan band. Do not inspect or copy the bundled template layouts unless the user explicitly asks for full template replication.

Only if the user explicitly asks for a different style and has not provided a clear direction, offer 2-3 concrete style directions and mark one as your recommendation. Each style option should briefly specify:

- Color palette
- Layout system
- Typography direction
- Illustration or image treatment
- Decorative elements
- Density and whitespace rules

After applying the default style or after the user chooses a different style, create one final style direction and keep the visual identity consistent across all slide prompts. Keep color palette, typography, texture, icon/illustration language, and overall mood stable. Do not reuse the same layout on every page.

For consulting decks, "density and whitespace rules" should normally mean medium-high to high information density with purposeful spacing, not minimalist whitespace. The main body should be carried by text, arrows, labelled boxes, matrices, process flows, comparison frames, and compact top/body insight callouts rather than decorative icons. Treat a normal content slide with repeated icon cards, icon-led bullet rows, a small central diagram, broad empty surrounding space, too few Chinese text units, label-only sparse diagrams, a weak top title/headline, an added separate title-summary label, bottom takeaway/callout boxes, paired bottom text boxes, unsupported slogan-like "金句", or a bottom full-width slogan band as a failed sample unless the user explicitly asked for that layout.

The `references/` directory contains optional style references. Use them as inspiration, not as rigid templates. Adapt the style to the topic and audience.

Important: a deck should have one coherent visual identity, not one repeated composition. Treat each reference as a style system: stable palette, typography, icon language, texture, and visual mood; variable page layout chosen from the slide's content role. `layout_blueprints` are candidate starting points only. Do not apply the same blueprint to every slide.

Available references:

- `references/中智蓝色咨询模板风.md`
- `references/框架演绎版式规则.md`
- `references/商务纯蓝框架模板库.md`
- `references/清爽专业风.md`
- `references/创意杂志风.md`
- `references/电子墨水杂志风.md`
- `references/数据仪表盘风.md`
- `references/科研答辩风.md`
- `references/复古扁平插画风.md`
- `references/手绘技术解释风.md`
- `references/手绘白板风.md`
- `references/温暖手工风.md`

When adding a reusable style to the library, also add its `references/{style_name}.md` file to this list.

Example alternative style confirmation:

```text
我建议用 A，因为它最适合这份内容的受众和表达目标。

A. 清爽专业风（推荐）：浅色背景、蓝绿强调色、结构清晰，适合汇报、答辩和技术分享。
B. 创意杂志风：大标题、强图片、留白更大胆，适合分享和传播。
C. 数据仪表盘风：指标卡、图表感布局，适合数据密集型报告。

你选哪个？也可以指定要调整的配色、布局或插画方向，或者上传一张喜欢的 PPT 风格图片让我参考。
```

## Generate One Sample Slide For Approval

After the outline is approved, the default style is applied, and the image backend is confirmed, generate exactly one sample slide image before full production.

Sample slide requirements:

- Use the applied default style description, or the user-confirmed alternative style description if the user requested another style.
- Prefer a representative content slide over the cover when possible.
- Demonstrate the intended deck rhythm: the sample should show how the chosen style adapts to a real content page, not just a generic fixed template.
- If the sample uses a bundled framework template module, it must show the template's structural logic recolored into the confirmed deck palette. Keeping the template's original colors is a failed sample unless the user explicitly requested full template replication.
- For consulting/report samples, demonstrate medium-high to high information density and framework-style logical exposition: the page should contain enough readable Chinese text in a source-grounded framework to look like a real management consulting page, without excessive blank body areas. The sample should make hierarchy, causality, sequence, dependency, boundary, or transformation visible, rather than simply arranging bullets into a table or grid. When the source supports it, use 10-16 meaningful Chinese text units or an equivalent interpreted matrix/framework, including compact explanatory sentences rather than only noun labels.
- If the sample slide is generated from a text report, include the selected logic archetype in the prompt, such as house/pillar, layered architecture, process lane, causal chain, responsibility boundary, funnel, loop, value chain, interpreted matrix, or comparison columns with convergence. The visual body should show the reasoning path, not just independent boxes.
- Do not use decorative icons, repeated icon cards, or icon-led bullet rows in a normal consulting/report sample unless the user explicitly requested an icon-led style.
- Do not use a plain table, spreadsheet-like grid, or repeated equal-weight card set as the main body unless the approved outline says the source table must be preserved.
- Use the top slide title/headline as the page storyline. Do not add a separate visible storyline/core-viewpoint row or prefix.
- If a sample slide needs a summary viewpoint, put it in the top headline or a compact insight band between the title and main body. Do not put summary, evidence, or takeaway text boxes at the bottom of the page.
- The summary viewpoint must be a source-grounded logical conclusion, implication, cause-effect judgement, or decision criterion. Do not add generic slogans, motivational phrases, decorative "金句", or unsupported catchphrases.
- If the source is a Word/PDF/text report, all sample-slide text must be traceable to the slide's source basis. Do not add external facts, labels, cases, or recommendations just to make the page look richer.
- If the source is a Word/PDF/text report, the sample should use original report wording wherever feasible. Treat self-created consulting labels, invented summary phrases, and source-detached bottom conclusions as failures even if they sound polished.
- If the source is a Word/PDF/text report, the sample slide must preserve the approved `Source framework`. Reject and regenerate any sample that hides an explicit subheading, flattens parent-child logic into unrelated peer bullets, or adds a visible module not present in the source framework.
- Do not include bottom takeaway/callout boxes, paired bottom text boxes, bottom evidence boxes, or a bottom full-width orange-red block plus deep-blue background plus white-text conclusion strip.
- Save it directly as the intended final slide filename, such as `{base_dir}/{deck_name}/origin_image/slide_08.png`. In CLI/API fallback mode, use `scripts/image_gen.py generate --out` for that exact path.
- Show the sample image to the user.
- Ask the user to confirm the visual style, typography, layout density, and Chinese text quality.

Do not generate the full deck until the user approves the sample slide. If the user requests changes, revise the style description and regenerate that same `slide_XX.png` file first. Once approved, keep that file as the final slide for its page. Do not create `sample_slide.png` in `origin_image/`, because the assembly step is designed around final `slide_XX` filenames.

After the sample slide is approved, record the sample generation method in `deck_spec.json` before preparing full-deck jobs. This is the contract the parent passes to subagents so they use the same image-generation path as the sample, not a cheaper local rendering path. Include at least:

- `backend_used`: the confirmed backend label, such as `built-in image tool` or `scripts/image_gen.py`.
- `tool_name`: the actual tool or command used, such as `image_gen`, `image_generate`, or `scripts/image_gen.py`.
- `mode`: `generate` or `edit`.
- `prompt_source`: where the approved sample prompt came from.
- `size`, `quality`, and model/config details when the backend exposes them.
- `approved_sample_path`: the approved `origin_image/slide_XX.png` path.
- `input_context_preparation`: how local source/style images were made available, such as `view_image` for built-in mode.
- `handoff_rule`: subagents must use the same backend/tool/mode and return a blocker if that path is unavailable.
