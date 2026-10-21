---
name: original-pic-ppt
description: Generate visually unified image-based PPT/PPTX decks from articles, reports, papers, notes, or outlines when full-slide images are acceptable. Preserve original wording, all source levels, item counts, order, parent-child relations, scope, numbers, and meaning. Use artistic non-tabular compositions, purposeful whitespace, complete explanations, Microsoft YaHei, and the CIIC blue palette by default. Speaker notes are opt-in. Use other presentation skills when separate native editability is required.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    primaryEnv: OPENAI_API_KEY
    envVars:
      - name: OPENAI_API_KEY
        required: false
        description: API key for CLI fallback.
      - name: OPENAI_BASE_URL
        required: false
        description: API base URL.
      - name: CODEX_PPT_IMAGE_MODEL
        required: false
        description: Image model, defaults to gpt-image-2.
      - name: CODEX_PPT_HOME
        required: false
        description: Runtime home override.
    homepage: https://github.com/ningzimu/codex-ppt-skill
---

# Codex PPT

## 管理咨询与国企汇报模式

用于管理咨询或国企汇报时，先读[认可样本设计方法](/Users/shampwu/.codex/skills/ppt-layout-library/references/approved-consulting-design.md)和[设计参数](/Users/shampwu/.codex/skills/ppt-layout-library/references/consulting-tokens.json)，按来源关系选择整页结构与组件，在制作记录中注明借鉴文件、页码和适配方式。

- 默认16:9、Microsoft YaHei、原生可编辑、无阴影；当前任务明确指定的模板、复刻或其他样式要求优先。
- 标题表达有依据的核心观点，同时保留来源要求的分类名称与归属。新写同层条目通常不超过6项；已有来源的项数、顺序、父子关系及完整表达优先。
- 先核对来源，再渲染全部页面；按设计方法逐页验收，并检查原生对象、字体、配色和无阴影。已知偏好直接沿用，内部样页由制作方检验。

本技能仅在用户明确接受整页图片时承接图像制作；需要原生可编辑对象时，直接转用 ciic-style-ppt 或 mck-ppt-design，并沿用上述参考，不进入本技能的大纲、样页或图像审批流程。整页图片不能通过可编辑性验收。

## 艺术构图与原文措辞（长期要求）

新建、改版、规划及审稿时，必须执行[PPT艺术构图与展示要求](/Users/shampwu/.codex/skills/ppt-art-direction.md)。默认采用更具艺术感的非表格整页构图，优先沿用原文完整句子，以有意义的曲线、几何、局部色面和留白组织阅读。用户明确指定模板、原样复刻或表格保留范围时按其要求处理。

该共享要求优先于本技能及其 agents、references、docs、提示模板中的表格首选、均匀卡片、固定密度、占用率、留白比例、图形份额及默认文字压缩建议。原文项数、顺序、归属与完整解释保持；技术密度诊断仅作审图提示，不能据此填充装饰或删改原文。

## 文字与原文结构（强制）

每次制作、改写或审稿前，必须完整阅读并执行 [PPT文字与原文结构要求](/Users/shampwu/.codex/skills/ppt-content-rules.md)。本节及共享规则优先于本技能中关于字数、短标签、内容密度和模板项数的建议。

1. 原文每一层级的同层项数、顺序和父子关系必须原样保留。原文两点就保留两点，不能拆成三点、合成一点，也不能把下级说明提升为同级分支。模板必须适应原文结构。
2. 正文须表达完整、清楚，让读者只看页面就能理解对象、动作、关系和适用条件。不得为版面删去因果、比较、限定或责任关系，不以名词堆砌、缩略标签和斜杠串联替代说明；放不下时先调整版式和容器，必要时在保留原层级的前提下续页。
3. 先按原文逐项核对各层级、项数、顺序及父子关系，再由独立审稿者只看实际渲染页面检查文字是否自然、意思是否完整。记录两轮审查结果；任一未通过，修正后重审，不得交付。

## Overview

This skill creates image-based PowerPoint decks from source material. Each slide is a complete 16:9 generated image. Final images are assembled into `.pptx` with `scripts/assemble_ppt.py`.

Speaker notes are opt-in. By default, do not create `speech.md`, do not write notes into the `.pptx`, and do not treat notes as a completion requirement. Create and embed speaker notes only when the user explicitly requests presentation notes, narration, a speech script, or PPT remarks.

Microsoft YaHei (微软雅黑) is the default font family for all generated text, including titles, body text, labels, annotations, captions, citations, charts, tables, Chinese, Latin letters, numbers, and punctuation. Regular and bold weights are allowed. The current task's explicit font or strict-reproduction requirement takes precedence; reusable style briefs and samples do not silently replace the confirmed font. Preserve text already baked into a strict supplied image. Apply the confirmed font to speaker notes only when notes are requested.

Use this when the user wants a visually unified presentation and accepts full-slide image pages. Do not use it when every textbox, chart, or shape must remain separately editable.

When the source material is a Word/PDF/text report, preserve its original wording and complete argument structure by default. Arrange complete sentences near source-grounded diagrams or in open body areas. Long original passages may remain visible when needed; adjust the layout or continue the same item across pages. Rewriting or faithful compression requires an explicit user request and a recorded mapping. Do not add unsupported facts, cases, data, recommendations, causes, risks, management judgements, or inferred points.

For source-report decks, the report's visible framework is part of the source content. Preserve explicit top-level and sub-level structure such as `一是 / 二是 / 三是`, chapter titles, paragraph order, `中央层面 / 地方层面 / 因此`, table row groups, and named subsections. Visual design may make that framework more readable, but must not replace it with a new consultant-invented framework.

Treat every explicitly enumerated source structure at any level as a cardinality-locked content group. If one argument has four stated elements, preserve exactly those four elements as four distinct visible content modules in the same source order and under the same parent argument. Do not add a fifth element, merge the four elements into three, split one element into multiple peer elements, omit or duplicate an element, change an element's core meaning, or move an element to another parent. Visible labels use original wording by default. A changed label requires explicit user authorization for rewriting and a mapping that records the authorization, faithful wording and required terms. A layout or framework template must adapt to the source count.

Use one sequence signal per item. When visible wording already carries order through expressions such as `一是 / 二是`, `首先 / 其次`, `第一 / 第二`, `其一 / 其二`, `（一）/（二）`, `1. / 2.`, or `A. / B.`, do not add a separate numeric, alphabetic, badge, circle, tab, or step marker. When an external marker is needed for composition, remove the corresponding sequence expression from the approved visible wording and record the change in `source_item_mapping`. Never render combinations such as `1. 一是坚持……` or `A. 一是坚持……`.

For source-report decks, preserve the report's terminology and semantic anchors while writing for presentation readability. Retain named concepts, policy terms, numbers, causal direction, conditions, scope, polarity, and stated conclusions exactly. Keep original headings, labels, judgement questions, and complete statements unless the user explicitly authorizes a faithful wording change. Keep each visible module focused on one source item. Retain the explanation needed to understand its object, action, relationship, and conditions; adapt the container or use a clearly linked continuation instead of cutting meaning. Do not replace source meaning with self-created consulting slogans, bottom-line claims, or summary labels. If a visible conclusion is a source sentence such as `归纳起来...`, keep it connected to the original parent structure so the reader can see which source level it summarizes.

Keep audience-facing deliverables source-neutral. Use reference materials as the factual basis, but present their content directly rather than narrating the production process. Do not write phrases such as `根据你提供的资料`, `基于用户提供的附件`, `从Excel中可以看出`, `结合原报告`, `附件显示`, or equivalent wording in visible slides, handouts, delivery-facing summaries, or explicitly requested speaker notes. Keep filenames, attachment labels, and `source_basis` / `source_evidence` details in internal project metadata only. If the user explicitly requests citations or source disclosure, use a formal source label such as document title, issuing organization, and date; never describe it as material "provided by the user".

Default style: unless the user explicitly requests another visual style, always use the bundled `中智蓝色咨询模板风` reference as the color-only style guide for decks generated by this skill. Treat this default visual style as pre-approved; do not stop to ask the user to confirm the style each time. Retain the CIIC/中智 blue, pale blue, white, charcoal, and small orange-red accent palette, but do not preserve template-specific page structures, footers, page-number blocks, city motifs, logos, bottom conclusion bands, or bottom takeaway/callout boxes unless the user explicitly asks to replicate the template layout. For consulting content pages, favor readable argument text and logic demonstration frameworks such as house/pillar structures, layered architectures, process lanes, comparison columns with convergence, interpreted matrices, causal chains, responsibility-boundary frames, funnels, loops, and compact in-body callouts. When the user asks to use framework templates or the source logic matches a bundled module, use `references/商务纯蓝框架模板库.md` and the copied assets under `assets/business-blue-framework-templates/` as structure references only. Borrow the template's structural grammar, not its visible color system: remap all fills, lines, labels, emphasis marks, and background colors to the confirmed deck palette, defaulting to `中智蓝色咨询模板风`; the original template's blue, gradients, accent allocation, and decorative color choices are not authoritative unless the user explicitly asks to reproduce them. Omit decorative icons by default; do not use icon cards, icon rows, repeated pictograms, or simple table-like grids as a substitute for analysis. Ordinary content pages should feel like management consulting pages: the body zone should show how ideas support, cause, constrain, sequence, or transform one another, not just list points in boxes.

Prefer the built-in image generation/editing tool. Use `scripts/image_gen.py` only when the built-in backend is unavailable, lacks a required capability, or the user explicitly asks for API/CLI mode.

## Hard Constraints

- Read the relevant `Reference Map` files before each phase. This file is the orchestration contract; detailed rules live in `docs/` and worker prompts in `prompts/`.
- Use the confirmed font family for all generated text, defaulting to Microsoft YaHei (微软雅黑). Apply it consistently to Chinese, Latin letters, numbers, punctuation, titles, body text, labels, annotations, captions, citations, and chart/table text. The current task's explicit font instruction takes precedence. Preserve text already baked into a strict supplied image.
- For every Word/PDF/text report deck, read `docs/source-fidelity-and-structure-conservation.md` before outlining, writing `deck_spec.json`, preparing prompts, generating slides, or performing QA. Apply its speaker-note rules only when notes were explicitly requested.
- Respect approval gates. Do not create final `deck_spec.json`, prompt jobs, slide images, or `.pptx` before the approvals in `docs/workflow-gates-and-progress.md`. Apply the same gate to `speech.md` only in an explicit speaker-notes workflow.
- After the user approves the sample slide and authorizes full-deck generation, every remaining slide image job must be dispatched to a slide subagent whenever subagents are available.
- The main agent owns orchestration, prompt jobs, state recording, QA, and assembly. It owns `speech.md` only when speaker notes were explicitly requested. Do not silently replace available slide subagents with sequential production.
- Every final `origin_image/slide_XX.png` must be generated by the selected image backend: built-in image generation/editing tool or `scripts/image_gen.py`.
- Local drawing, Pillow, SVG, HTML/CSS/canvas screenshots, python-pptx/PptxGenJS layouts, and manual overlays are failure modes, not fallbacks.
- When the user provides a Word/PDF/text report as source content, every slide title/headline, key point, label, recommendation, and explicitly requested speaker note must be grounded in that report. Do not invent missing facts, external cases, data, citations, conclusions, risks, suggestions, or inferred points. Add an inference only after explicit user approval and record that approval in the source-fidelity metadata.
- When the user provides a Word/PDF/text report as source content, prefer the original wording. Preserve required terms, numbered structure, causal direction, conditions, scope, polarity, numerical meaning, conclusions and complete explanations. Record any user-authorized wording change; layout improvement does not authorize compression.
- When the user provides a Word/PDF/text report as source content, preserve source-framework fidelity. Before outlining, reconstruct a `source_structure_map` that records top-level sections, nested subheadings, paragraph order, and table/figure groupings. Every slide outline and prompt must inherit that map. A different visual framework may change presentation form while retaining the complete source map. Do not flatten nested source logic into arbitrary peer bullets; for example, if a paragraph separates `中央层面` and `地方层面`, the slide must keep those as visible sub-level labels or as clearly nested content inside the same parent section.
- Before outlining a Word/PDF/text report deck, record viewpoints and all supporting items in their original hierarchy. Numbered or named subpoints, examples, conditions, and evidence retain their original parent and order. The schema names `core_viewpoint` and `core_meaning` do not limit preservation to top-level or important items: include every explicit source level in the ledger and mapping. Only genuinely repeated wording may be removed without removing an item or its meaning.
- Build a `source_structure_ledger` for every countable group at any source level. Record a stable `group_id`, exact parent label, `core_viewpoint`, `source_count`, and ordered items with stable `item_id`, source label, `core_meaning`, `required_terms`, order, and source basis. Mark a whole source group as excluded only with explicit user approval and an approval note.
- For every included source group, maintain a one-to-one `source_item_mapping` from each ledger item to exactly one visible content module across the deck. Preserve exact item count, core meaning, parent-child relations, order, and required terms. Adding, merging, splitting, omitting, duplicating, semantic drift, reparenting, or reordering a source item is a hard failure.
- For every mapped source item, record `sequence_marker_mode` as `embedded_text`, `external_marker`, or `none`. Use one consistent mode across the source group. `embedded_text` requires sequence wording in the approved visible text and forbids `external_sequence_marker`; `external_marker` requires unique external markers, removes sequence wording from the visible text, and records the removal in `sequence_edit_note`; `none` forbids both forms. Treat `visible_order` as internal validation metadata and never render it.
- Faithful compression within an existing source item is available only when the user explicitly requests rewriting or text simplification. Record that request in compression_note together with the wording change, retain all required_terms and full core_meaning, and keep every supporting item under its original parent. Default to original phrases and complete sentences; increase space or use a faithful continuation when necessary.
- Run `scripts/prepare_slide_prompts.py` as the deterministic source-structure gate. For report-grounded decks, it must reject missing ledgers, count mismatches, incomplete mappings, duplicate mappings, unrecorded label compression, missing required terms, parent changes, order changes, mapped text exceeding the configured layout capacity without a recorded text-length exception, mixed sequence-marker modes, reused external markers, and simultaneous embedded and external sequence signals before prompt jobs are written.
- For source-report decks, each outline slide and each `deck_spec.json` slide should include `source_basis`, `source_evidence`, or equivalent local context identifying the report section, paragraph, table, figure, or user-provided asset that supports the slide. If a slide cannot be supported by the report, remove it or ask the user before adding it.
- Treat provenance as internal metadata unless the user explicitly requests source disclosure. Never render filenames, attachment names, file types, prompt terminology, or production-process phrases such as `根据你提供的资料`, `基于附件`, `从Excel可见`, `结合原报告`, or `用户提供` in slides, handouts, delivery-facing summaries, or explicitly requested speaker notes. State the supported business content directly. When formal citations are requested, cite the document, organization, or date neutrally without referring to the user as the provider.
- Do not create extra visible modules that are not present in the source framework just because they look useful. If the source has three stated points, the slide may use a three-part flow, layered stack, or other visual treatment, but must not add a fourth visible module such as an independent diagnostic map, matrix, or "检审切入点" section. Source-supported details may be shown only under their original parent section.
- Do not reduce visible modules by combining peer source items. Each mapped source item must occupy its own visible content module; connecting arrows, parent headers, evidence labels, and decorative separators do not count as peer content modules.
- For Chinese consulting/report decks, content slides must be text-rich and logic-led: use labelled diagram boxes, matrices, process arrows, responsibility-boundary frames, and summary callouts before using decorative icons. Avoid icon rows, icon-only cards, and clusters of small pictogram elements unless the user explicitly requests an icon-led visual style.
- Interpret text-rich as multiple concise, readable argument units distributed through a logic framework. It does not permit copying long report paragraphs into boxes or filling slides with dense prose.
- For Chinese consulting/report decks, content slides must be framework-led rather than table-led. Before generating a slide, choose a source-grounded logic archetype such as house/pillar framework, layered architecture, process lane, causal chain, responsibility boundary, evidence-to-insight funnel, closed loop, value chain, interpreted matrix, or comparison columns with convergence. The visible layout must encode hierarchy, causality, sequence, dependency, boundary, or transformation; a plain grid of boxes is a failure unless the source itself is a table that must be preserved.
- When using the bundled business-blue framework templates, treat them as visual grammar references only: select the matching module such as 屋顶图, 多层平台, 中心发散, 循环逻辑, 业务流程, or 时间轴流程; map report content to the module's structural roles; recolor the module to the confirmed deck style, defaulting to 中智 blue / pale blue / white / charcoal with small orange-red accents; do not copy placeholder text, logos, QR codes, copyright/instruction slides, page numbers, claims, or original template color choices.
- For Chinese consulting/report decks, omit decorative icons by default. Functional icons may identify source-grounded roles, business objects, stages, or states; use a coherent family, retain the text labels, and let the actual source objects determine their count. Repeated icons that only decorate bullet rows do not substitute for analysis. Keep sequence markers consistent with the sequence-marker single-source rule.
- For consulting/report content slides, let the complete source content determine density. Keep explanations readable and use alignment and spacing to organize the original items; do not add, split, combine, omit, or shorten items merely to fill the page. The source determines the number and nesting of text units; do not create or split points to meet a density quota. Use complete, readable explanations rather than noun labels. Whitespace is acceptable when it supports readability without losing any source content.
- For source-report decks, do not merely pour paragraphs into equal-sized boxes, generic tables, or card grids. The outline, `deck_spec.json`, and slide prompt should name the slide's `logic_archetype`, `reasoning_path`, `framework_mapping`, and a brief `why_not_table` note, unless the slide is intentionally preserving a source table/figure.
- Every normal consulting/report content slide must use the page's topmost title/headline as the storyline. The storyline is not a separate visible line and must not be rendered with the literal label `STORYLINE` or `STORYLINE：`. The top title/headline should be content-bearing and reflect the page's core topic or viewpoint, for example `华润案例：价值创造型总部与分层分类授权`.
- Do not add bottom-of-page takeaway boxes, paired bottom text boxes, bottom evidence boxes, bottom conclusion callouts, or bottom full-width conclusion slogan bands by default. If a summary viewpoint is needed, put it in the top headline or in a compact insight band between the title and the main body, then use the body to prove it.
- Summary viewpoints must be source-grounded, logically meaningful conclusions, implications, cause-effect judgements, or decision criteria. Do not add generic slogans, motivational phrases, empty catchphrases, or decorative "金句" that are not supported by the source.
- The selected image backend must stay fixed after backend confirmation. Do not let subagents switch backend for convenience.
- After sample approval, record how the approved sample was generated and pass that exact method to every slide subagent.
- When the default or confirmed style is `中智蓝色咨询模板风`, read `references/中智蓝色咨询模板风.md` as a color-only guide. Do not include template footer/page-number rules or assemble with the bundled PPTX template unless the user explicitly asks to reproduce the template layout.
- Slide dispatch and result state must be recorded with the bundled scripts. Chat messages alone do not make a slide dispatched or complete.
- If a required subagent, image backend, or required-image path is unavailable, stop and report a blocker with the slide id and evidence. Do not create a lower-quality replacement.

## Visible Progress

For non-trivial decks, keep a user-visible checklist with one active step. Canonical completion evidence is in `docs/workflow-gates-and-progress.md`.

Default visible steps:

1. Prepare source, outline, style, and backend decisions.
2. Generate and approve one sample slide.
3. Prepare slide jobs and slide state.
4. Dispatch slide subagents.
5. Record generated slide results.
6. QA, repair, and PPT assembly.

Do not mark a step complete from chat alone; use real files or script-recorded state.

## Default Workflow

1. Understand the source content.
   - Identify topic, audience, goal, page count, style/brand constraints, and sections to include or exclude.
   - If the source is a Word/PDF/text report, extract and read the report text before planning. Preserve section headings, tables/figures, named entities, numbers, definitions, stated conclusions, and explicit recommendations as the source of truth.
   - If the source is a Word/PDF/text report, create a source framework inventory and `source_structure_ledger` before any slide outline: record the original heading tree, numbered points, nested labels, paragraph sequence, table/figure groupings, core viewpoints, exact group counts at every source level, stable item ids, source labels, core meanings, required terms, parent ids, and source order. Treat both artifacts as binding. Write complete, natural explanations for supporting items while preserving their count, meaning, parent-child relationships, and order; remove only genuinely repeated wording. Mark every explicit sequence expression so the outline can choose one sequence-marker mode without duplication.
   - Keep source filenames, attachment labels, and provenance wording inside internal framework inventories and traceability fields. Draft all audience-facing titles and body text as standalone content that makes sense without mentioning how the source reached the agent. Apply the same rule to speaker notes only when they were explicitly requested.
   - Do not use general knowledge, industry assumptions, or plausible consulting patterns to fill content gaps unless the user explicitly asks for external enrichment. If the report is too thin for the requested slide count, propose fewer slides or ask for permission to add external analysis.
   - If no page count is specified, choose a practical count. Typical decks are 8-12 slides.

2. Plan the deck outline.
   - Before writing or updating `outline.md`, read `docs/workflow-gates-and-progress.md` and `docs/outline-style-and-sample.md`.
   - Draft slide roles and required source images. Ask for confirmation, then stop before style, backend, sample, or downstream artifacts until approved.
   - For consulting/report decks, map each content slide to a logic structure before visual production: house/pillar framework, layered architecture, process lane, causal chain, responsibility boundary, evidence-to-insight funnel, closed loop, value chain, interpreted matrix, comparison columns with convergence, or other source-grounded framework. Make the slide title itself serve as the page storyline/headline, and arrange all original source text with a clear visual protagonist and purposeful whitespace; do not impose a text-unit or density quota.
   - For text-report decks, read `references/框架演绎版式规则.md` before finalizing the outline. Each normal content slide should include `logic_archetype`, `reasoning_path`, `framework_mapping`, and `why_not_table`. Use tables only within an explicit user request for tabular display or source-table preservation; do not convert viewpoints into repeated rows and columns.
   - If the user mentions the attached framework templates, 商务纯蓝模板, 屋顶图, 多层平台, 中心发散, 循环逻辑, 业务流程, or 时间轴流程, read `references/商务纯蓝框架模板库.md` before finalizing the outline. For each slide that uses a template module, include `template_reference_module`, `template_reference_asset`, `structure_mapping`, `style_scope`, and `color_mapping`.
   - For decks based on a Word/PDF/text report, record the source basis alongside the title/headline and content in internal metadata. Prefer the original title and complete original wording; record any explicitly user-authorized title revision. Record original visible labels, complete visible messages, required terms, and any authorized wording changes; do not shorten words merely to fit the layout.
   - Mark `source_basis`, `source_evidence`, `Source framework`, filenames, and attachment references as internal-only planning metadata. Do not carry those labels or provenance phrases into visible slide text. Apply the same restriction to speaker notes only when they were explicitly requested.
   - For decks based on a Word/PDF/text report, write a `Source framework` note for each slide showing the original top-level and sub-level structure being represented. The slide's visual logic structure must serve that source framework, not replace it. If a proposed visual structure would hide or scramble the original hierarchy, redesign the slide before asking for approval.
   - For every included countable source group at any level, add a `Source item mapping` to the outline. Map every stable `item_id` to one visible module, record the source label, natural visible label, complete visible explanation, required terms, compression note when applicable, source order, `sequence_marker_mode`, `external_sequence_marker`, and `sequence_edit_note`, and show the expected module count. If a group continues across slides, keep the parent label and group id visible in planning metadata, preserve source order across the slide sequence, and use one sequence-marker mode across the complete group.

3. Apply the default visual style.
   - Before offering style options or using files from `references/`, read `docs/outline-style-and-sample.md`.
   - Use `references/中智蓝色咨询模板风.md` as the default color-only style for every deck unless the user explicitly asks for another style or asks to replicate the full template layout.
   - When using `中智蓝色咨询模板风`, restate that only the color system is retained: blue/pale-blue/white/charcoal with small orange-red accents. Body pages should use readable text and a framework that preserves all source levels; the complete content determines density and spacing; the top title/headline is the storyline and no separate storyline/core-viewpoint row should be added; omit decorative icons, avoid icon-card layouts, avoid plain table-like grids, and avoid bottom takeaway/callout boxes by default.
   - Treat the default `中智蓝色咨询模板风` as already approved and do not ask the user to confirm style selection each time. Only discuss style choices if the user explicitly asks for a different style, supplies a style reference, or asks to replicate a full template layout.
   - Use the confirmed font family, defaulting to Microsoft YaHei, for every generated text element. Vary size, weight, color, alignment and spacing within that family. Follow any current explicit font or strict-reproduction instruction; do not infer a font change from a reference alone.

4. Confirm the image backend.
   - Before generating any slide image, read `docs/backend-selection.md`.
   - Check whether a built-in image tool is callable, state what you checked, name the backend, explain fallback status, and wait for confirmation.
   - If CLI/API fallback is selected, read `docs/cli-api-fallback.md`. Read `docs/image-model-configuration.md` only after config errors or explicit API-setting requests.

5. Generate one sample slide for approval.
   - Before generating or approving the sample slide, read `docs/outline-style-and-sample.md`.
   - Generate exactly one representative sample after outline approval, default style application, and backend confirmation. Do not generate the full deck until approved.
   - After approval, record `sample_generation_method` in `deck_spec.json` so jobs and subagents inherit the same path.

6. Create the project directory.
   - Before initializing folders or assembling files, read `docs/project-assembly-and-reporting.md`.
   - If no destination is specified, use the current working directory or the source file directory.

7. Prepare user-supplied assets.
   - Before using paper figures, charts, screenshots, logos, or other required assets, read `docs/user-supplied-assets.md`.
   - Treat required assets as strict inputs and confirm slide-to-asset mapping before generation.

8. Generate all slide images.
   - Before full-deck image generation, read `docs/slide-generation-and-subagents.md`.
   - Create per-slide jobs with `scripts/prepare_slide_prompts.py` or saved `prompts/slide_XX.json` files.
   - Every final image must come from the selected backend and be recorded with bundled state scripts.

9. Dispatch slide subagents.
   - Before dispatching or replacing slide workers, read `docs/slide-generation-and-subagents.md` and `prompts/slide-worker.md`.
   - Use one subagent per remaining slide job whenever possible. If required subagents cannot be spawned, stop and report a blocker unless the user changes the workflow.

10. Quality check and repair.
    - Before QA or assembly, read `docs/project-assembly-and-reporting.md`.
    - Inspect every slide before assembly: text, outline match, truncation, style, unwanted page numbers, overlaps, and required assets.
    - Reject or regenerate slides whose generated text visibly uses an unauthorized font or a fallback font. The confirmed family defaults to Microsoft YaHei; current explicit font and strict-reproduction requirements take precedence. Text baked into a strict supplied image is exempt from re-typesetting.
    - For consulting content pages, also check that the page uses readable text and a source-grounded framework as the main body, not decorative icon clusters, repeated icon cards, or a plain table/grid of boxes; the layout should reveal hierarchy, causality, sequence, dependency, boundary, or transformation. It should let complete content determine spacing and use the top title/headline as the page storyline without a separate storyline/core-viewpoint row, and should not add bottom takeaway/callout boxes or the removed bottom deep-blue conclusion band.
    - When a slide uses a bundled framework template module, also check that its colors have been remapped to the confirmed deck style. If the slide visibly keeps the template's original palette, gradients, accent allocation, or decorative color treatment instead of the 中智 color system, regenerate it with a stricter color-mapping prompt.
    - Treat repeated decorative icons, icon-led rows that merely repeat labels, table-like uniform grids, independent cards with no visible reasoning path, label-only diagrams that leave meaning unclear, bottom paired text boxes, bottom conclusion callouts, or unsupported slogan-like takeaways as failed samples. A coherent set of functional icons tied to actual source objects may repeat. Repair the failed design and render it again before delivery.
    - For Word/PDF/text report sources, also check that slide content is traceable to the approved outline and source basis. Regenerate or rewrite any slide that adds unsupported claims, external facts, recommendations not present in the report, or self-created summary wording that weakens or replaces the original report's terms.
    - For Word/PDF/text report sources, also check source-framework fidelity: top-level points, nested labels, and paragraph groupings from the approved outline must remain visible or clearly nested in the slide. Regenerate or rewrite any slide that arbitrarily re-groups source content, invents an extra module, erases an explicit subheading such as `中央层面 / 地方层面`, or turns nested source logic into unrelated peer bullets.
    - For Word/PDF/text report sources, count the mapped visible content modules on every slide and reconcile them against `source_structure_ledger` and `source_item_mapping`. Verify core meaning, causal direction, scope, polarity, conclusions, numbers, and required terms. Regenerate any slide with an added, merged, split, omitted, duplicated, semantically altered, reparented, or reordered source item, or with wording that omits a necessary relationship or condition to fit a label or character limit. Do not record the slide result or assemble the deck until this audit passes.
    - For Word/PDF/text report sources, inspect every ordered group for duplicate sequence signals. If approved visible text contains sequence wording, reject any added number, letter, badge, circle, tab, or step marker. If the mapping uses `external_marker`, reject any restored sequence wording and verify that the approved external marker appears exactly once.
    - Check source-neutrality across slide images. If speaker notes were explicitly requested, check them under the same rule. Regenerate or rewrite any audience-facing text that mentions the user supplying material, an attachment or file type, a filename, the prompt, `source_basis`, or the production process. Allow source labels only when the user explicitly requested citations, and then use formal document/organization/date attribution.
    - Regenerate severe failures with a tighter prompt. Use backend editing for localized issues when available.
    - For CLI/API fallback edit commands, read `docs/cli-api-fallback.md`. Replace the final slide only after validating the edited output.

11. Assemble the PPT; add speaker notes only on explicit request.
    - Before running assembly, read `docs/project-assembly-and-reporting.md`.
    - Make sure `outline.md` reflects the final confirmed deck outline. By default, do not create `speech.md` and run assembly without `--include-speaker-notes`.
    - If the user explicitly requests speaker notes, create `speech.md` with headings that map to `Slide N`, validate it against the source ledger, and run assembly with `--include-speaker-notes`.
    - Before assembly, ensure `slide_jobs.json` shows generated slides as `recorded` and approved samples as `accepted`. If any slide is `pending`, `dispatched`, or `blocked`, stop.
    - If using `中智蓝色咨询模板风`, assemble normally without `--template` unless the user explicitly asks to preserve the original PPT template layout or master/theme metadata.

12. Report the result.
    - Use the final report checklist in `docs/project-assembly-and-reporting.md`.
    - Include paths, slide count, backend used, recorded-result status, and any limitations or blockers.

13. Save reusable styles when requested.
    - If asked to save the current deck style or a supplied image/PDF/PPT/PPTX style, read `docs/style-library.md`.

## Subagent Dispatch

Slide subagents are mandatory after sample approval whenever the runtime can spawn them. The main agent prepares jobs and records state; each worker handles exactly one `prompts/slide_XX.json` job and returns only selected image path, backend, and QA note.

Use `docs/slide-generation-and-subagents.md` for dispatch, commands, result recording, blockers, and backend provenance. Use `prompts/slide-worker.md` as the handoff template.

Subagents must not edit `outline.md`, `deck_spec.json`, other slide jobs, `origin_image/`, an opt-in `speech.md`, or the final `.pptx`. The parent records outputs and assembles.

## Acceptance Criteria

- Output is a valid `.pptx`.
- Every generated text element uses the confirmed font family, defaulting to Microsoft YaHei (微软雅黑), across titles, body text, labels, annotations, captions, citations, charts, tables, Chinese, Latin letters, numbers and punctuation. Regular and bold weights may vary. Unauthorized font substitutions and fallback glyphs fail QA; current explicit font or strict-reproduction requirements take precedence. Text baked into a strict supplied image remains unchanged. Explicitly requested speaker notes use the confirmed font.
- Each expected final slide image exists under `origin_image/slide_XX.png`.
- Every final slide image was generated by the confirmed backend and recorded through `record_slide_result.py`, except an approved sample marked accepted by run state.
- `outline.md` reflects the approved deck outline.
- When the deck is based on a Word/PDF/text report, `outline.md`, `deck_spec.json`, prompts, and visible slide content stay grounded in the provided report. Unsupported claims, invented data, invented cases, and unrequested external recommendations are failures.
- When the deck is based on a Word/PDF/text report, `outline.md`, `deck_spec.json`, prompts, and visible slide content preserve the report's own framework and hierarchy. Missing explicit subheadings, arbitrary re-grouping, or extra visible modules not present in the source are failures.
- When the deck is based on a Word/PDF/text report, every included source group has a valid `source_structure_ledger` entry and complete one-to-one `source_item_mapping`. Source count, core meaning, parent-child relations, order, numbers, and required terms remain unchanged across `outline.md`, `deck_spec.json`, prompt jobs, and slide images; user-authorized faithful wording changes are allowed when the authorization and change are recorded, and any addition, merge, split, omission, duplication, semantic drift, reparenting, or reordering is a failure. Apply the same source-fidelity contract to `speech.md` only when speaker notes were explicitly requested.
- Every ordered source group uses one consistent sequence-marker mode and one sequence signal per item. Visible wording with sequence expressions has no external numeric or alphabetic marker; external-marker layouts remove those expressions and display each approved marker exactly once; `visible_order` never appears as slide text.
- Word/PDF/text report slides default to complete original wording. Use typography, spacing and source-grounded diagrams to organize it; long original passages are allowed. Only an explicit user request activates rewriting or compression, and each change must be mapped without altering source counts, order, terms, scope or meaning.
- Audience-facing slide text, handouts, and delivery summaries are source-neutral: they state grounded content directly and do not mention that the user supplied materials, attachments, filenames, file types, prompt fields, or the production process. Explicitly requested speaker notes follow the same rule. Formal source labels appear only when explicitly requested and use neutral document/organization/date attribution.
- The generated `.pptx` contains no speaker-note content by default. `speech.md` is absent or ignored during default assembly. When the user explicitly requests notes, `speech.md` exists and assembly includes them only through `--include-speaker-notes`.
- Decks default to `中智蓝色咨询模板风` and visibly retain only the CIIC/中智 blue-orange color style; they do not automatically preserve the original template layouts, footers, page markers, logos, city motifs, bottom slogan bands, or original framework-template color schemes.
- Consulting/report decks use source-grounded logical frameworks and readable complete explanations. Omit decorative icon-card rows by default. Functional icon groups may repeat when they identify the actual source roles, objects, stages, or states and retain clear labels; do not impose a numeric icon quota.
- Consulting/report decks have visible logical演绎 value: each normal body slide shows how source points relate, support, cause, constrain, sequence, or transform one another. Preserve parallel source items as parallel items. A table or matrix is used only when the user explicitly requests that form or preservation of the source table; open comparison remains available when it faithfully expresses the source; do not invent hierarchy or causal links merely to satisfy a framework preference.
- Consulting/report body pages preserve the complete source hierarchy and explanations. Page density follows that content, with no required occupancy ratio or minimum text-unit count; label-only diagrams fail when they leave necessary meaning unclear.
- Normal consulting/report slides use a meaningful top title/headline as the page storyline. They do not render a separate storyline/core-viewpoint label or extra storyline subtitle.
- Slides do not use bottom takeaway boxes, paired bottom text boxes, bottom evidence boxes, bottom conclusion callouts, or the removed bottom orange-red block plus deep-blue white-text conclusion band unless the user explicitly asks for that layout.
- Any summary viewpoint on a slide is source-grounded and logical, and is placed in the title or near the top of the body rather than as a bottom slogan.
- `slide_jobs.json` and `slide_run_state.json` reflect the final state.
- Required source images are visibly represented, or a blocker is reported.
- If blocked, the final response identifies phase, slide id, evidence path, and unfinished reason; do not call the deck complete.

## Reference Map

- `docs/source-fidelity-and-structure-conservation.md`: mandatory source ledger, one-to-one mapping, allowed compression, change approval, deterministic validation, and visual QA rules for Word/PDF/text report decks.
- `docs/workflow-gates-and-progress.md`: approval gates, progress, completion evidence.
- `docs/backend-selection.md`: backend decision rules and confirmation text.
- `docs/outline-style-and-sample.md`: outline, style, sample rules, prompt examples.
- `docs/user-supplied-assets.md`: strict handling for required source assets.
- `docs/slide-generation-and-subagents.md`: jobs, dispatch, result recording, blockers, provenance.
- `docs/cli-api-fallback.md`: fallback runtime, generation/edit commands, image limits, troubleshooting.
- `docs/image-model-configuration.md`: API key, base URL, model, `.env`; read only when config is needed.
- `docs/project-assembly-and-reporting.md`: project directory, opt-in speaker notes, assembly, final report, prompting principles.
- `prompts/slide-worker.md`: slide subagent handoff template.
- `references/中智蓝色咨询模板风.md`: bundled CIIC/中智咨询 color-only consulting style, prompt brief, and layout exclusions.
- `references/框架演绎版式规则.md`: source-grounded framework archetypes and anti-table rules for text-report consulting decks.
- `references/商务纯蓝框架模板库.md`: copied business-blue framework template assets, preview contact sheets, module selection rules, and template-use QA checks.
- `assets/ciic-consulting-2024-template/`: source PPTX template and rendered preview images for color extraction only; do not replicate layout unless explicitly requested.
- `assets/business-blue-framework-templates/`: copied framework PPTX templates and rendered previews for structure reference only.
- `references/*.md`: visual style references.

## Documentation and Updates

For source, docs, install, config, and examples, see [ningzimu/codex-ppt-skill](https://github.com/ningzimu/codex-ppt-skill).
