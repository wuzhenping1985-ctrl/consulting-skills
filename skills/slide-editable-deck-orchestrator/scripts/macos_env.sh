#!/usr/bin/env bash

# Local runtime configuration for the pngtopptx SkillSet on this Mac.
export PNGTOPPTX_SKILLS_ROOT="/Users/shampwu/.codex/skills"
export PNGTOPPTX_PYTHON="/Users/shampwu/.codex/venvs/pngtopptx/bin/python3"

PNGTOPPTX_CODEX_BIN="/Users/shampwu/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override"
export PATH="/Users/shampwu/.codex/venvs/pngtopptx/bin:/opt/homebrew/bin:${PNGTOPPTX_CODEX_BIN}:${PATH}"
export NODE_PATH="/Users/shampwu/.codex/skills/slide-image-dual-render/node_modules${NODE_PATH:+:${NODE_PATH}}"

if [[ -x "/Applications/LibreOffice.app/Contents/MacOS/soffice" ]]; then
  export PATH="/Applications/LibreOffice.app/Contents/MacOS:${PATH}"
fi

unset PNGTOPPTX_CODEX_BIN
