# macOS Setup

This local installation uses Codex's standard Skill directory:

```text
/Users/shampwu/.codex/skills
```

Before running any reconstruction or QA command:

```bash
source /Users/shampwu/.codex/skills/slide-editable-deck-orchestrator/scripts/macos_env.sh
```

The helper exposes `PNGTOPPTX_SKILLS_ROOT`, selects the dedicated Python
environment, adds Homebrew tools to `PATH`, and makes the Codex-bundled
LibreOffice/Poppler binaries visible.

## Project dependencies

The renderer dependencies are installed inside
`slide-image-dual-render/node_modules`. A deck may also carry its own
`node_modules`; pass it with `--node-path` when present.

## Reconstruction command

Run from the deck project root:

```bash
node "${PNGTOPPTX_SKILLS_ROOT}/slide-image-dual-render/scripts/slide_pipeline.js" \
  --project "${PWD}" \
  --slides 1,2,3 \
  --quality reconstruction \
  --require-qa \
  --require-reconstruction \
  --profile "${PNGTOPPTX_SKILLS_ROOT}/slide-image-dual-render/styles/clinical-dark.json" \
  --assets "${PWD}/assets" \
  --crop-plan "${PWD}/work/crop_plan.json" \
  --target both \
  --pptx-out "${PWD}/out/deck.pptx" \
  --html-out "${PWD}/out/deck.html"
```

Run the final gate after reconstruction:

```bash
node "${PNGTOPPTX_SKILLS_ROOT}/slide-image-dual-render/scripts/final_gate.js" \
  --project "${PWD}" \
  --slides 1,2,3 \
  --quality reconstruction \
  --require-qa \
  --require-reconstruction \
  --require-pptx-openable \
  --target both \
  --pptx "${PWD}/out/deck.pptx" \
  --html "${PWD}/out/deck.html"
```

## Verification

```bash
bash /Users/shampwu/.codex/skills/slide-editable-deck-orchestrator/scripts/verify_macos.sh
```

Use `python3` or `${PNGTOPPTX_PYTHON}` in place of PowerShell examples that
invoke `python`. Use forward slashes, zsh line continuation, and quoted paths.
