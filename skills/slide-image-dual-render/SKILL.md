---
name: slide-image-dual-render
description: >-
  Reconstruct slide images into both editable PPTX and standalone HTML from one
  backend-agnostic renderer. Use when slide screenshots or exported PNGs need
  faithful native-object reconstruction, crop metadata, visual QA, and package
  validation.
---

# Slide Image Dual Render

## PPT文字与原文结构要求（必读）

使用本技能前，必须完整阅读并执行 [PPT文字与原文结构要求](/Users/shampwu/.codex/skills/ppt-content-rules.md)。

- 忠实还原时保留原图文字；原文含糊处保留证据并指出，不擅自补写或润色。用户授权新写或改写时，才按文字要求调整表达。
- 重建前核对原文各层级；每层的项数、顺序、父子关系必须一致。原文两项不得拆成三项或合成一项，文本框及分页安排不构成新增或合并语义项的理由。
- 新写或改写须表达自然完整。空间不足时先调整文字框和版面，不得用删减条件、堆砌关键词或生硬缩写挤进预定布局。
- 逐页 QA 必须检查结构对应和适用的文字要求。任何一项未通过均不得交付，即使渲染、像素比较和 `final_gate.js` 已通过。

## macOS Local Installation

Before running commands on macOS, source
`../slide-editable-deck-orchestrator/scripts/macos_env.sh` and follow
[macOS setup](../slide-editable-deck-orchestrator/references/macos.md).

This module turns slide images into faithful editable reconstructions in two
formats from one source of truth:

- a `.pptx` where titles, panels, text, icons, tables, lines, and callouts are
  native objects where practical; and
- a standalone `.html` rendering that uses the same slide authoring code.

The renderer uses source-pixel coordinates and a backend-agnostic drawing layer.
Each slide is described once, then replayed onto PPTX and HTML surfaces.

## Style Profiles

Profiles in `styles/` keep conversions consistent across decks:

- `styles/clinical-dark.json`
- `styles/corporate-light.json`
- `styles/_schema.md`

Set `DECK_PROFILE` to the selected profile before rendering. Use
`scripts/preview.js` to inspect a profile specimen.

## Setup

Create a deck project outside the installed toolkit directory:

```bash
mkdir -p deck/src deck/assets deck/work deck/out deck/lib
cd deck
npm i pptxgenjs sharp react react-dom react-icons
pip install pillow numpy
```

Copy source images into `src/` as `slide1.png`, `slide2.png`, and so on.

## Production Entry Point

Use `scripts/slide_pipeline.js` for validator-backed runs:

```powershell
$env:SLIDE_PIPELINE_STRICT="1"
$env:DECK_PROFILE="$PWD\styles\clinical-dark.json"
$env:DECK_ASSETS="$PWD\assets"
$env:DECK_PXW="1672"
$env:DECK_PXH="941"

node scripts\slide_pipeline.js --project . --slides 1,2,3 --target both --crop-plan work\crop_plan.json --node-path .\node_modules --pptx-out out\deck.pptx --html-out out\deck.html
```

Run the final gate before delivery:

```powershell
node scripts\final_gate.js --project . --target both --pptx out\deck.pptx --html out\deck.html
```

When using an installed toolkit layout, call the same scripts from:

```text
%USERPROFILE%\.pngtopptx\skills\slide-image-dual-render\scripts
```

## Workflow

1. Study each source image and measure key coordinates.
2. Choose or tune a style profile.
3. Generate assets and crop manifests.
4. Author slide functions in `lib/slides.js` using the kit helpers.
5. Render PPTX/HTML through `slide_pipeline.js`.
6. Run raster/HTML comparison and `final_gate.js`.
7. Disclose crop-heavy regions in delivery notes.

## Quality Modes

- `canary`: one-slide setup smoke test.
- `preservation`: visible fidelity may rely on disclosed crop regions.
- `reconstruction`: native reconstruction, QA evidence, native object counts,
  crop budgets, and strict final gates are required.

## Important Rules

- Draw once, render twice. Backend-specific concessions belong in surface atoms.
- Use source-pixel coordinates throughout.
- Keep one resolved font policy for both PPTX and HTML.
- Do not use hidden browser scaling for visual QA.
- Preserve continuous-tone regions as crops instead of pretending they are
  editable vectors.

## Reference Files

- `references/workflow.md`
- `references/kit-api.md`
- `references/pptxgenjs-gotchas.md`
- `references/qa-and-rendering.md`
