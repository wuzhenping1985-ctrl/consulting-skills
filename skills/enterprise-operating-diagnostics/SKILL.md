---
name: enterprise-operating-diagnostics
description: Analyze enterprise operating effectiveness, operating safety, and business operations, especially for SOEs, local state-owned platforms, city-investment companies, infrastructure groups, industrial/manufacturing groups, and listed companies. Use when Codex needs to diagnose financial and business fundamentals from annual reports, audit reports, credit rating reports, financial statements, user-provided data, operation data, or public information, and produce a Chinese Word-style consulting/article report on 经营成效, 经营安全, 企业家底盘点, 十五五规划前诊断, 财务视角分析, 业财融合分析, 采购/生产/销售/研发经营分析, 经营分析报告, or similar topics.
---

# Enterprise Operating Diagnostics

## Overview

Use this skill to turn company data into a structured Chinese diagnostic report on operating effectiveness, operating safety, and business operations. The method is based on connecting indicators into evidence chains, not mechanically listing ratios.

For detailed financial indicators, read `references/indicator-framework.md`. For business-operation methods from strategy, procurement, production, sales, R&D, and reporting, read `references/business-analysis-methods.md`. For report structure and writing patterns, read `references/report-template.md`. To generate a `.docx` from drafted Markdown, use `scripts/markdown_to_docx.py`.

## Workflow

1. Clarify the target company, analysis period, industry, ownership type, and requested scope: `经营成效`, `经营安全`, `业务经营分析`, or a combined diagnosis.
2. Collect source material: financial statements, annual reports, audit reports, rating reports, company background, business segment data, operation data, industry benchmarks, debt maturity data, and government support information if relevant.
3. Build the analysis dataset before writing. At minimum capture revenue, profit, net profit attributable to parent, total assets, net assets, interest-bearing debt, cash, short-term debt, long-term debt, finance expense or interest paid, operating cash inflow, operating cash flow net amount, investment cash flow, financing cash flow, capex, accounts receivable, other receivables, inventory, and major non-recurring gains. For business-operation analysis, also collect product, customer, channel, price, procurement, production, quality, R&D, headcount, capacity, and project data where available.
4. Select indicators by business logic. Do not cover every indicator if it does not help the diagnosis. Prioritize the indicators that explain contradictions, such as high revenue growth but weak profit, profit without cash, low asset-liability ratio but high net debt pressure, or rapid expansion with worsening receivables/inventory.
5. Diagnose through cross-checks:
   - Scale growth: is revenue or asset expansion supported by main business, or by trade pass-through, engineering pass-through, consolidation, valuation gains, or debt-driven asset expansion?
   - Profit quality: is profit from core operations, or from fair-value gains, asset disposal, subsidies, capitalization, or non-recurring items?
   - Cash quality: do revenue and profit convert into operating cash inflow and operating cash flow net amount?
   - Debt safety: is apparent leverage masking interest-bearing debt, short-term repayment pressure, restricted cash, guarantees, off-balance obligations, or minority-interest/consolidation issues?
   - Growth structure: are marginal returns, operating leverage, receivables, inventory, and capex consistent with the company's development stage?
   - Business drivers: which procurement, production, sales, pricing, credit, inventory, quality, R&D, or organization factors explain the financial result?
6. Write conclusions before prose. For each major section, first decide the diagnostic judgment, then support it with the strongest data evidence and business explanation.
7. Produce the final report as a Chinese Word document when requested. Draft in Markdown, convert to `.docx`, then visually check headings, tables, Chinese font, and paragraph spacing.

## Analysis Logic

For `经营成效`, use the route `规模变化 -> 效益变化 -> 现金约束 -> 现状小结 -> 未来关注`. The core question is whether growth has created real, sustainable profit and cash.

For `经营安全`, use the route `债务水平 -> 增长结构 -> 现金流水平 -> 综合判断 -> 未来关注`. The core question is whether the company can continue operating without relying on fragile refinancing, accounting gains, or unsustainable government/related-party support.

When both are requested, put `经营成效` first and `经营安全` second, then add a combined diagnosis: growth quality, solvency pressure, cash self-sufficiency, and planning implications.

For `业务经营分析`, use the route `战略目标 -> 业务场景 -> 关键驱动因素 -> 数据建模/差异分析 -> 改善措施 -> 风险挑战 -> 闭环跟踪`. The core question is how business decisions create or damage profit, cash flow, competitiveness, and management efficiency.

When financial diagnosis finds an abnormality, translate it into a business hypothesis. For example, weak gross margin may require product lifecycle, pricing, procurement, material, labor, manufacturing expense, quality-loss, or R&D cost analysis; weak cash conversion may require credit policy, receivables, inventory, supplier payment, and capex rhythm analysis.

## Evidence Standards

- Prefer multi-year trend data over single-year point values.
- Compare growth rates, not only absolute values: revenue vs profit, assets vs liabilities, revenue vs receivables, revenue vs inventory, operating cash flow vs net profit.
- Treat accounting indicators as clues, not conclusions. Explain the business reason behind each abnormality.
- Use operational data to verify financial conclusions: volume, unit price, product mix, BOM, material price, labor hours, capacity utilization, defect rate, customer credit terms, sales expense, R&D stage-gate cost, and project milestones.
- For SOEs and city-investment companies, explicitly discuss policy role, government payment cycle, land/infrastructure inventory, hidden debt, guarantees, refinancing access, and fiscal support where evidence allows.
- Mark uncertainty clearly when data is missing. Do not invent exact figures.
- Cite source document names or public URLs in the report when using external information.

## Writing Requirements

- Use a direct consulting/article tone: judgment first, data second, explanation third.
- Avoid generic textbook definitions unless the concept is necessary for the reader.
- Avoid exhaustive ratio tables without interpretation.
- Use section endings such as `小结`, `综合判断`, and `未来关注` to convert analysis into planning implications.
- The final report should resemble a professional Chinese Word article: clear title, numbered headings, compact paragraphs, selective tables, and a firm diagnostic conclusion.

## Word Output

If a Word file is requested:

1. Draft the report in Markdown using the structure in `references/report-template.md`.
2. Convert it with:

```powershell
& "C:\Users\A\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "C:\Users\A\.codex\skills\enterprise-operating-diagnostics\scripts\markdown_to_docx.py" input.md output.docx
```

3. If the bundled Python path differs, use any Python environment with `python-docx` installed.
4. Open or render-check the Word file if document layout quality matters.
