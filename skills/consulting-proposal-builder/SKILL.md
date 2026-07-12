---
name: consulting-proposal-builder
description: Build targeted Chinese management consulting proposals, proposal outlines, demand-understanding sections, and technical方案 sections from new-client interviews, client background, industry context, and stated consulting needs. Use when the user asks for 咨询建议书, 项目建议书, 需求理解, 技术方案, 管理模块拆解, 咨询方案, 标书/比选方案 content, or wants to turn client requirements into a structured consulting proposal with industry judgment, peer benchmarking, client diagnosis, problem modules, objectives, and module-by-module solution design.
---

# Consulting Proposal Builder

## Overview

Use this skill to draft or improve a management consulting proposal in Chinese. The core output has two major parts: `需求理解` and `技术方案`, with every conclusion grounded in the client's situation, current public information, and consulting logic.

## Workflow

1. Confirm the deliverable form: proposal outline, full prose, PPT structure, Word document text, or a specific section. If the user wants final files and does not specify otherwise, output multiple Word documents: one `需求理解` DOCX and one separate `技术方案` DOCX for each management module.
2. Build the fact base from the user's materials: client name, industry, scale, stage, region, ownership, financial/human/organization facts, current pain points, prior reforms, decision-maker concerns, project scope, timeline, and constraints. If the client is listed or has usable datasets, collect at least three years of comparable data for client diagnosis whenever feasible.
3. If important facts are missing, make reasonable assumptions and mark them as `待访谈确认`; ask questions only when the missing fact would change the whole proposal direction.
4. Research current industry and peer information when the proposal depends on external facts. Use public sources, compare dates, cite sources, and distinguish fact, inference, and consultant judgment.
5. Draft `需求理解` before `技术方案`; do not jump into solutions until the management modules and objectives are stated.
6. For each technical module, keep the same three-part logic: overall methodology, external peer practices matching that methodology, and client-specific solution design.
7. For final Word deliverables, keep file boundaries strict: `需求理解` is one document; `技术方案` documents are split by the actual module count and each document covers only one module.
8. End with a short quality check: whether every proposed solution traces back to a diagnosed problem, whether every peer case supports the method, whether unclear client facts are flagged, and whether the DOCX files match the required split.

## Required Proposal Structure

Use `references/proposal-blueprint.md` when drafting a complete proposal or when the user asks for a standardized template.

### Part 1: 需求理解

Write four subsections:

1. `行业发展现状判断`: concise but broad-view industry judgment using longer time horizons, wider product/category boundaries, broader regional/global markets, competitive structure, regulatory/technology/capital/customer changes, and what those changes mean for management capability. Support the trend judgment with at least three years of comparable quantitative evidence where available, such as market size, growth rate, penetration, concentration, price, volume, capacity, investment, profitability, export/import, customer demand, or financing data; do not infer an industry trend from only one year of data unless no multi-year data is available and the limitation is clearly stated.
2. `同行企业解决思路`: benchmark well-known, leading, or scale-comparable companies through named, concrete company cases. State explicitly what `XX公司` did, under what context, using what mechanism or management action, and what lesson is transferable to the client. Do not use generic phrases like `行业领先企业普遍通过...` unless followed by specific company evidence.
3. `客户现状简要剖析`: analyze the client's development stage and relevant finance, people, organization, governance, process, market, product, operations, or digital conditions. Use `references/customer-diagnosis-framework.md` as the preferred method for financial and operating diagnosis, especially the `经营成效` and `经营安全` lenses. For listed companies or clients with available data, use at least three years of comparable data to identify trends, inflection points, and structural issues; avoid drawing conclusions from a single year unless only one year is available and clearly marked as a limitation. Do not merely restate directly visible report figures such as revenue and profit; decompose the drivers behind changes, such as price-volume mix, product/customer/channel structure, cost and expense items, gross margin, operating leverage, asset efficiency, cash conversion, or organization/resource allocation, to identify the client's real management pain points. Use assumptions when facts are incomplete.
4. `管理模块问题及目标`: synthesize the above into several management modules. For each module, state the core problem, why it matters now, and the target state.

### Part 2: 技术方案

For each management module from Part 1, write:

1. `整体方法论`: introduce a common framework if one fits; otherwise create a clear named framework with 3-5 dimensions. The framework must be usable for diagnosis and solution design.
2. `外部同行做法`: present one or more peer practices found from public information. Each practice must map to the methodology dimensions and be transferable to the client.
3. `针对客户的解题设计`: apply the methodology dimension by dimension to the client's actual situation. Give concrete work steps, analysis methods, outputs, decision mechanisms, and initial hypotheses when facts are uncertain.

## Word Deliverable Rules

When producing final files, create multiple `.docx` files by default:

- `01_需求理解_<客户简称>.docx`: include all demand-understanding content, including industry judgment, peer benchmarking, client diagnosis, module problem split, and module objectives.
- `02_技术方案_<模块名称>_<客户简称>.docx`, `03_技术方案_<模块名称>_<客户简称>.docx`, etc.: create one file per management module identified in `需求理解`.
- Do not merge all technical方案 modules into one Word file unless the user explicitly asks for a single combined document.
- Keep each technical方案 document self-contained: start with the module's problem/objective recap, then include methodology, peer practices, client-specific solution design, work steps, expected outputs, and data/interview needs.
- If using the document skill, render and verify the DOCX files according to that skill's workflow.

## Methodology Guidance

Use `references/methodology-library.md` when selecting frameworks for strategy, organization, HR, performance, process, finance, governance, digital transformation, marketing, supply chain, or operating model modules.

When no known framework fits, create a bespoke method with:

- A memorable Chinese name, preferably `X-维`, `X-环`, `X-图谱`, or `X-闭环`.
- 3-5 dimensions that are mutually distinct and collectively cover the problem.
- A diagnostic question, analysis tool, and expected output for each dimension.
- A direct mapping from methodology dimensions to peer practices and client solution steps.

## Research Standards

- Prefer official filings, annual reports, sustainability reports, investor presentations, government/association publications, reputable media, and company websites.
- Use recent sources for industry status, regulation, market size, executive/company facts, and public cases.
- For industry judgment, combine current evidence with longer-cycle context: at least three years of comparable market size/growth, product-category evolution, adjacent/substitute markets, domestic and global market dynamics, policy/technology cycles, and capital-market shifts where data is available.
- Industry trend conclusions must be supported by quantitative data. Use at least one relevant numeric indicator for each major trend claim where data is available, and use at least three years of comparable data to prove direction, speed, volatility, or inflection. Do not use a single-year number to claim a trend.
- If only one or two years of industry data are available, state the data limitation, avoid strong trend language, and frame the conclusion as `初步判断` or `待进一步验证`.
- For listed clients or clients with available internal/external data, prioritize at least three years of comparable data for revenue, profit, margins, cash flow, assets, liabilities, headcount, productivity, business mix, regional mix, customer/channel mix, or other relevant indicators.
- Do not over-interpret a single-year abnormality. Explain whether a change is trend, cycle, one-off event, accounting/caliber change, or data gap.
- For peer practices, use named company cases and concrete practices. If only high-level industry observations are available, label them as background rather than case evidence.
- For client diagnosis, move from reported numbers to business drivers: ask why revenue/profit/cash/headcount/productivity changed, which product, region, channel, customer, cost, expense, price, volume, efficiency, or governance factor caused the change, and what management issue it reveals.
- For financial and operating diagnosis, prefer the `经营成效 + 经营安全` method in `references/customer-diagnosis-framework.md`: first test scale and benefit quality, then test debt, cash flow, and growth-structure sustainability.
- Avoid treating public slogans as proof of management effectiveness. Translate public facts into cautious consulting inferences.
- Do not fabricate peer practices. If evidence is thin, say `公开资料显示有限，可作为初步假设`.
- Cite links or source names in the final output when research was used.

## Writing Standards

- Write in polished Chinese consulting style: structured, evidence-aware, concise, and client-specific.
- Avoid generic statements such as `加强管理能力` unless followed by concrete management object, mechanism, process, metric, or deliverable.
- Use terms like `初步判断`, `可能反映`, and `有待访谈验证` when inferring from incomplete facts.
- Keep module names business-facing, such as `战略定位与增长路径`, `组织管控与权责机制`, `绩效激励与人才体系`, `财务经营分析与预算管理`, `流程效率与数字化赋能`.
- If the user asks for PPT or Word output, combine this skill with the relevant presentation or document skill and preserve this proposal logic. For final Word output, follow the multi-DOCX split above.
