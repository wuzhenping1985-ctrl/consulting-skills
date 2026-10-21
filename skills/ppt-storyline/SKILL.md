---
name: ppt-storyline
description: Build consulting-style PowerPoint storylines and slide logic. Use when turning analysis, interview notes, financial data, industry research, strategy recommendations, project proposals, or rough materials into executive decks with title messages, page flow, evidence chains, chart recommendations, appendix structure, and board/CEO-ready narrative.
---

# PPT Storyline

## 管理咨询与国企汇报模式

用于管理咨询或国企汇报时，先读[认可样本设计方法](/Users/shampwu/.codex/skills/ppt-layout-library/references/approved-consulting-design.md)和[设计参数](/Users/shampwu/.codex/skills/ppt-layout-library/references/consulting-tokens.json)，按来源关系选择整页结构与组件，在制作记录中注明借鉴文件、页码和适配方式。

- 默认16:9、Microsoft YaHei、原生可编辑、无阴影；当前任务明确指定的模板、复刻或其他样式要求优先。
- 标题表达有依据的核心观点，同时保留来源要求的分类名称与归属。新写同层条目通常不超过6项；已有来源的项数、顺序、父子关系及完整表达优先。
- 先核对来源。制作或改版PPT时渲染全部页面；仅编写提纲时记录来源映射及预期视觉，不额外生成文件。已知偏好直接沿用。

## 艺术构图与原文措辞（长期要求）

新建、改版、规划及审稿时，必须执行[PPT艺术构图与展示要求](/Users/shampwu/.codex/skills/ppt-art-direction.md)。默认采用更具艺术感的非表格整页构图，优先沿用原文完整句子，以有意义的曲线、几何、局部色面和留白组织阅读。用户明确指定模板、原样复刻或表格保留范围时按其要求处理。

该共享要求优先于本技能及其 agents、references、docs、提示模板中的表格首选、均匀卡片、固定密度、占用率、留白比例、图形份额及默认文字压缩建议。原文项数、顺序、归属与完整解释保持；技术密度诊断仅作审图提示，不能据此填充装饰或删改原文。

## 必须先读：文字与原文结构

执行本技能前，必须阅读并遵守[PPT文字与原文结构要求](/Users/shampwu/.codex/skills/ppt-content-rules.md)。这些要求优先于下文及本技能 agents、references 中的字数、标题、叙事和版式建议。

- 以文章、报告、提纲或已有PPT作为内容来源时，先记录每层项目的名称、项数、顺序和父子关系，并逐项映射到页面。原文两点仍为两点，不拆成三点，不合成一点，不将子项提升为同层主项。
- 只有用户明确授权重构，才可在授权范围内调整原文框架；制作、精简、美化、重设计或采用咨询风格均不自动构成重构授权。续页可以改变承载页数，但须保留原层级、编号和归属。
- 标题和正文要讲人话，表达完整。正文保留必要的主体、动作、关系、条件和限定；短标签仅用于含义明确的导航或对象名称。字数、卡片尺寸和留白要求不得导致删改意思，也不得把理解正文所需的信息藏入备注。
- 交付前依次完成两项审核：先对照原文核查结构与内容，再脱离原文独立阅读每张图及页面，检查是否能仅凭可见文字和关系读懂。任何一项失败均须修改、重审，未通过不得交付。

## Core Workflow

1. Identify the audience, decision, and task scope. Establish whether content is supplied and whether the user has explicitly authorized restructuring.
2. For supplied content, map its hierarchy before planning pages: source node, parent, order, sibling count, full meaning, and destination page. Keep each level intact. For a new topic without a prescribed structure, develop a suitable outline.
3. Write clear, natural text that preserves subjects, actions, logical relations, scope, and qualifications. Use the space needed to make each point understandable; remove repetition without removing meaning.
4. Plan pages around the source groups. A page may contain several related subpoints. If it continues onto another page, retain its parent heading, item identities, and order. An answer-first storyline or reordered evidence sequence requires explicit authorization when it changes supplied structure.
5. Choose an exhibit that represents the stated relationship. Parallel items remain parallel; arrows show only supported sequence, dependency, or causation. Keep numbers, labels, definitions, and source scope accurate.
6. Review in order: compare every level with the source, then independently read the rendered pages without using the source to fill gaps. Fix and repeat any failed check before delivery.

## Slide-Level Standard

- Title: clearly identify the source section or state a supported point. Preserve source headings and their relationships; conclusion titles are optional and must not replace required category names or reorder the argument.
- Body: express a complete point with sufficient context. Do not impose a word limit, a fixed number of bullets, or one conclusion per page at the expense of source meaning.
- Exhibit: artistic whole-page composition, chart, open parallel arrangement, relationship map, hierarchy, source-supported path or other non-tabular form that faithfully represents the source. Tables and matrices require an explicit user request for that display or source preservation. Counts, order and complete original wording follow the source.
- Evidence and qualification: keep the source, date, unit, scope, and important conditions next to the relevant claim. Include an implication or requested action only when the material or authorized task supports it.

## Reference Loading

- Read `references/deck-structures.md` when developing a new outline or an explicitly authorized restructuring. Its examples do not replace supplied structure.
- Read `references/slide-patterns.md` when selecting exhibits and reviewing page text.

## Guardrails

- Fit the register to the task; management and consulting materials should be direct, professional, and understandable.
- Audience seniority does not authorize moving the conclusion, deleting framework pages, or changing the source's argument order.
- If content does not fit, first adjust layout and text areas or use a clearly marked continuation. Do not remove subjects, actions, relationships, or qualifications to fit a template.
- For PPTX creation, use the available Presentations skill/plugin and carry the source map and these review requirements into production.
