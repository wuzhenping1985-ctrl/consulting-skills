# Workflow Gates And Progress

Read this before creating downstream artifacts, advancing between phases, or reporting progress.

## Mandatory Phase Gates

This workflow has explicit approval gates. Do not advance to a later approval-gated phase until the previous approval gate has been approved by the user, unless the user explicitly asks to skip that confirmation. The default visual style is `中智蓝色咨询模板风` and is pre-approved; applying that default style is not a separate user confirmation gate.

Phase order:

1. Source reading and asset extraction
2. Outline confirmation
3. Default visual style application
4. Image backend confirmation
5. One sample slide approval
6. Full slide generation
7. QA and PPT assembly; speaker notes only after an explicit request

Hard rules:

- For every Word/PDF/text report deck, record viewpoints and all supporting items at every source level, then complete `source_structure_map`, `source_structure_ledger`, and outline-level `source_item_mapping` before requesting outline approval. Read `source-fidelity-and-structure-conservation.md`.
- Before outline approval, do not create final `deck_spec.json`, prompt job files, slide images, or `.pptx` files. Do not create `speech.md` at any stage unless the user explicitly requests speaker notes.
- If you need an internal planning artifact before approval, name it with `.draft.` such as `deck_spec.draft.json`, and clearly report that it is not final. Use `speech.draft.md` only in an explicit speaker-notes workflow.
- Downstream artifacts (`deck_spec.json`, `prompts/`, `slide_jobs.json`, final slide images, and `.pptx`) should be created only after the relevant gates have been approved. Add `speech.md` to this list only when speaker notes were explicitly requested.
- If the deck uses required source images, stop at outline confirmation and ask the user to verify the slide-to-image mapping before backend confirmation or image generation.
- Unless the user explicitly requests another visual style, use `references/中智蓝色咨询模板风.md` as the color-only default and proceed without asking for style selection confirmation. Briefly state the default style being applied, then continue to backend confirmation.

## Visible Progress Plan

For non-trivial decks, keep a user-visible checklist with one active step:

1. Prepare source, outline, style, and backend decisions.
2. Generate and approve one sample slide.
3. Prepare slide jobs and slide state.
4. Dispatch slide subagents.
5. Record generated slide results.
6. QA, repair, and PPT assembly.

Completion evidence:

- `Prepare source, outline, style, and backend decisions`: `outline.md` is approved and image backend is confirmed. For a Word/PDF/text report deck, the approved outline also contains complete core ledger coverage, exact one-to-one core item mappings, and planned concise visible wording.
- `Generate and approve one sample slide`: one final `origin_image/slide_XX.png` is approved as the style reference.
- `Prepare slide jobs and slide state`: `prompts/slide_XX.json`, `slide_jobs.json`, and `slide_run_state.json` exist. For a Word/PDF/text report deck, `prepare_slide_prompts.py` completed its source-structure validation and every mapped slide job contains `source_fidelity_contract`.
- `Dispatch slide subagents`: `slide_job_status.py` shows dispatchable slides and each spawned worker is recorded by `record_slide_dispatch.py`.
- `Record generated slide results`: each worker output is recorded by `record_slide_result.py`, which copies the selected image into `origin_image/slide_XX.png` and records backend provenance.
- `QA, repair, and PPT assembly`: every expected final image exists, QA is complete, and `{deck_name}.pptx` exists. For a Word/PDF/text report deck, visible module counts, core meanings, required terms, parent-child relations, order, and presentation compression have passed ledger reconciliation. If speaker notes were explicitly requested, `speech.md` is final, the notes passed the same reconciliation, and assembly used `--include-speaker-notes`.

Do not mark a step complete just because the chat says it is complete; use real files or script-recorded state.
