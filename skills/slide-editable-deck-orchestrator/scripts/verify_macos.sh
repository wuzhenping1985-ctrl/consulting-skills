#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/macos_env.sh"

failures=0

check_command() {
  local name="$1"
  if command -v "${name}" >/dev/null 2>&1; then
    printf '[PASS] %s: %s\n' "${name}" "$(command -v "${name}")"
  else
    printf '[FAIL] %s missing\n' "${name}"
    failures=$((failures + 1))
  fi
}

for command_name in node npm python3 soffice pdftoppm tesseract; do
  check_command "${command_name}"
done

for skill_name in slide-text-layer-inpaint slide-image-dual-render slide-visual-polish-qa slide-editable-deck-orchestrator; do
  skill_file="${PNGTOPPTX_SKILLS_ROOT}/${skill_name}/SKILL.md"
  if [[ -f "${skill_file}" ]]; then
    printf '[PASS] %s\n' "${skill_file}"
  else
    printf '[FAIL] %s missing\n' "${skill_file}"
    failures=$((failures + 1))
  fi
done

"${PNGTOPPTX_PYTHON}" - <<'PY'
modules = ["PIL", "numpy", "cv2", "skimage", "pytesseract"]
failed = []
for module in modules:
    try:
        __import__(module)
        print(f"[PASS] Python module: {module}")
    except Exception as exc:
        print(f"[FAIL] Python module: {module}: {exc}")
        failed.append(module)
raise SystemExit(1 if failed else 0)
PY
python_status=$?
if [[ ${python_status} -ne 0 ]]; then
  failures=$((failures + 1))
fi

if [[ ${failures} -ne 0 ]]; then
  printf '[FAIL] macOS verification failed with %d problem(s)\n' "${failures}"
  exit 1
fi

printf '[PASS] macOS verification completed\n'
