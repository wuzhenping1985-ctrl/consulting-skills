# Backend Selection

Read this before confirming the image backend or generating the first sample slide.

## Image Backend Policy

This skill supports exactly one image backend: Codex built-in `image_gen`.

`Local API/CLI fallback` is disabled for this skill. Do not use `scripts/image_gen.py`, `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `CODEX_PPT_IMAGE_MODEL`, `.env` configuration, third-party OpenAI-compatible proxies, or any API-key-based image backend for slide image generation or editing.

If Codex built-in `image_gen` is unavailable, fails, or lacks a required capability, stop and report a blocker. Do not silently switch to another image backend, and do not ask the user for an API key as a fallback path.

## Decision Rules

- Actively check whether Codex built-in `image_gen` is callable in the current environment before generating the first slide image.
- If `image_gen` is callable, use it for sample generation, full slide generation, and image editing.
- If `image_gen` is not callable, unavailable to subagents, or cannot satisfy a required capability, stop and report a blocker with the phase, slide id when applicable, and evidence.
- Do not read `cli-api-fallback.md` or `image-model-configuration.md` during normal operation. Those documents are deprecated for this imagegen-only policy.
- Do not mention missing `OPENAI_API_KEY`, do not configure API keys, and do not run `scripts/image_gen.py`.
- The selected backend label in `deck_spec.json`, `prompts/slide_XX.json`, `slide_jobs.json`, and final reporting must be `Codex built-in image_gen` or `built-in image tool (image_gen)`.

## Confirmation Text

Use this wording before generating the sample slide:

```text
我检查到当前环境可调用 Codex 内置图片生成工具 `image_gen`。根据当前 skill 的 imagegen-only 规则，本次只使用内置 `image_gen`，不会使用 `scripts/image_gen.py`、本地 API/CLI fallback 或你的 `OPENAI_API_KEY`。可以开始生成 1 页样张吗？
```

## Blocker Text

If `image_gen` is unavailable or insufficient, use this wording and stop:

```text
当前环境无法调用 Codex 内置 `image_gen`，而该 skill 已设置为只允许使用内置 `image_gen`，禁止切换到本地 API/CLI fallback 或 API key 后端。因此我不能继续生成图片式 PPT。请在支持 `image_gen` 的 Codex 环境中重试，或明确要求恢复/修改该 skill 的后端策略。
```
