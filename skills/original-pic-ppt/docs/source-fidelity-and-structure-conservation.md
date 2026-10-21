# Source Fidelity And Structure Conservation

原文措辞与艺术构图同时执行[PPT艺术构图与展示要求](/Users/shampwu/.codex/skills/ppt-art-direction.md)：默认完整沿用原文，只有用户明确要求改写或精简文字时才启用压缩；空间不足先调整布局或忠实续页。

Read this before outlining, writing `deck_spec.json`, preparing prompts, generating slides, or performing QA for any deck based on a Word/PDF/text report. Apply the speaker-note provisions only when notes were explicitly requested.

## Fidelity Boundary

Preserve viewpoints, supporting items, and the argument structure at every level. Use natural, complete wording. Existing schema names such as `core_viewpoint` and `core_meaning` do not exempt supporting levels from preservation or mapping.

Treat these source properties as binding:

- exact number of peer items at every explicit source level, including nested headings and named or numbered subpoints
- core meaning of every item
- parent-child relation and source order
- causal direction, conditions, scope, polarity, and stated conclusion
- names, policy terms, numbers, dates, units, and other required terms
- one visible content module for each source item

Visible wording uses complete original phrases and sentences by default. Faithful compression is available only when the user explicitly requests rewriting or text simplification and the authorization is recorded. Original paragraph length is not a failure; adjust geometry or continue the same source item. Preserve all counts, order, parent-child relationships, terms, conditions and meaning.

## Viewpoints And Supporting Items

Classify content before building the slide outline.

Record all of the following together with their supporting levels:

- main conclusions, judgements, recommendations, requirements, and principles stated by the source
- direct numbered or named elements, dimensions, stages, measures, paths, results, and conditions under a core argument
- causal relationships, comparison outcomes, scope limits, and qualifications that change the conclusion
- user-emphasized points and evidence whose exact number or wording determines the conclusion

Examples, citations, descriptive background, conditions, and elaboration remain supporting content under their original parent. Preserve every supporting item and its original order; distinguish it from genuinely repeated wording, which may be removed only when no item, meaning, relationship, or condition is lost.

Write or diagram supporting items within their original parent while retaining their count, order, meaning, and necessary explanation. Do not omit a supporting item to fit a page, combine peer supporting items, or promote a detail into a new peer module. When space is insufficient, adapt the layout or continue the same item on a clearly linked page.

## Structure Conservation

Treat every countable source structure at any level as a cardinality-locked group. If one argument or supporting subsection has four elements, preserve four distinct visible content modules in the same order and under the same parent. Do not add, merge, split, omit, duplicate, reparent, or reorder items at any level.

A visible label may differ from the source label only with explicit user authorization for rewriting or text simplification, and all conditions below must also be satisfied:

- `label_mode` is `faithful_compression`
- `compression_note` explains how the wording was shortened
- the visible label and visible message preserve the item's `core_meaning`
- all `required_terms` appear in the visible label or visible message
- the wording does not change causality, conditions, scope, polarity, conclusion, or numerical meaning

## Sequence Marker Single-Source Rule

Every ordered core group must use one sequence signal per item and one consistent sequence-marker mode across the group.

- Use `sequence_marker_mode: embedded_text` when the approved visible wording already contains an explicit sequence expression such as `一是 / 二是`, `首先 / 其次`, `第一 / 第二`, `其一 / 其二`, `（一）/（二）`, `1. / 2.`, or `A. / B.`. Leave `external_sequence_marker` and `sequence_edit_note` empty. Do not add a separate number, letter, badge, circle, tab, or step marker.
- Use `sequence_marker_mode: external_marker` when an external number or letter is needed for composition. Remove the corresponding sequence expression from `visible_label` and `visible_message`, set one unique `external_sequence_marker` for each item, and record the removal in `sequence_edit_note`.
- Use `sequence_marker_mode: none` only when the group requires no explicit sequence display. The visible wording and layout must contain no sequence word, number, letter, badge, or step marker.
- Keep `visible_order` as validation metadata. Never render `visible_order` as audience-facing text.
- Treat pure ordinal carriers as structure metadata rather than substantive `required_terms`. When the exact ordinal wording is legally, politically, or rhetorically material, retain it with `embedded_text`.

For example, `一是坚持长期主义` may appear exactly as that text with no external marker. If the design uses an external `1`, the approved visible text must be `坚持长期主义`; the slide must not display `1 一是坚持长期主义` or `A. 一是坚持长期主义`.

## Presentation Compression

Use the report as the semantic boundary and write for slide readability.

- Write natural labels and complete explanations for each source item. Use as many sentences as needed to keep relationships and conditions clear.
- Do not replace explanation with noun stacks, slash-separated terms, invented shorthand, or slogan-like phrases.
- There is no default writing length limit. The historical 36-character label and 80-character message thresholds produce non-blocking `text_capacity_diagnostics` only. Keep `presentation_text_limits` empty unless the user explicitly supplies limits; then validate those constraints or record an approved exception in `text_length_override_note`. Preserve complete wording and adapt the layout; never cut meaning to pass a length check.
- Remove redundant wording only within the same source item. Preserve every explicit subpoint, its order, and its parent; do not collapse them into one sentence or promote supporting details into new peers.
- Convert procedural, causal, hierarchical, comparative, and cyclical prose into matching diagrams.
- Use continuation slides for supporting explanation that would overload one slide, retaining its heading, source item id, order, and parent. Do not omit supporting items for space; remove only genuinely repeated wording.
- Use long verbatim passages only when the exact quotation is required evidence or the user explicitly requests quotation display.

## Required Workflow

1. Build the source structure artifacts before outlining.
   - Create `source_structure_map` for the complete heading and paragraph hierarchy.
   - Record viewpoints and all supporting levels, including examples and conditions, under their original parents.
   - Create `source_structure_ledger` for every countable group at any source level.
2. Confirm core coverage in the outline.
   - Mark each core group `included` or `excluded_with_user_approval`.
   - Exclude a whole source group only after explicit user approval and record the approval note.
   - Include all direct child items, including supporting subpoints when the parent group is included.
3. Create one-to-one slide mappings.
   - Add `source_item_mapping` to each slide that represents source items.
   - Map each included ledger item exactly once across the deck.
   - Record complete original visible wording and any explicitly user-authorized faithful revision.
   - Record one `sequence_marker_mode` for every mapped item and keep the mode consistent across its source group.
4. Run deterministic validation before prompt generation.
   - Use `scripts/prepare_slide_prompts.py`.
   - Stop on a missing ledger, count mismatch, missing mapping, duplicate mapping, unrecorded label compression, missing required term, changed parent, changed order, reused visual module id, mapped text exceeding the configured layout capacity without a recorded text-length exception, mixed sequence-marker modes, duplicate external markers, or simultaneous embedded and external sequence signals.
5. Run semantic and visual QA before result recording and assembly.
   - Compare every visible item with its `core_meaning` and `required_terms`.
   - Count visible peer content modules and verify parent-child relations and order.
   - After the source-by-source structure check, have an independent reviewer read only the rendered slide and identify unclear fragments, missing conditions, or relationships that require consulting the source to understand. Record both checks and repair any failure before delivery.
   - If speaker notes were explicitly requested, compare `speech.md` with the same semantic and structural anchors before assembly with `--include-speaker-notes`.

## Deck Spec Schema

Use a deck-level `source_structure_ledger`:

```json
{
  "source_structure_scan_note": "Core viewpoints and supporting details were classified; all countable groups at every source level were scanned.",
  "presentation_text_limits": {},
  "source_structure_ledger": [
    {
      "group_id": "G-01",
      "parent_label": "某论点",
      "core_viewpoint": "某论点由四个相互区分且共同支撑结论的要素构成",
      "source_basis": "第2章第3节第2段",
      "source_count": 4,
      "deck_status": "included",
      "ordered_items": [
        {
          "item_id": "G-01-01",
          "label": "要素一的原文表述",
          "core_meaning": "要素一需要保留的核心含义",
          "required_terms": ["关键术语A"],
          "order": 1,
          "source_basis": "第2章第3节第2段第1项"
        },
        {
          "item_id": "G-01-02",
          "label": "要素二的原文表述",
          "core_meaning": "要素二需要保留的核心含义",
          "required_terms": [],
          "order": 2,
          "source_basis": "第2章第3节第2段第2项"
        },
        {
          "item_id": "G-01-03",
          "label": "要素三的原文表述",
          "core_meaning": "要素三需要保留的核心含义",
          "required_terms": [],
          "order": 3,
          "source_basis": "第2章第3节第2段第3项"
        },
        {
          "item_id": "G-01-04",
          "label": "要素四的原文表述",
          "core_meaning": "要素四需要保留的核心含义",
          "required_terms": [],
          "order": 4,
          "source_basis": "第2章第3节第2段第4项"
        }
      ]
    }
  ]
}
```

Use `deck_status: excluded_with_user_approval` only for a whole source group that the user explicitly approved for exclusion. Add a non-empty `approval_note` that identifies the approval. Do not map excluded groups to slides.

If the report contains no countable groups at every source level, use an empty `source_structure_ledger` and a non-empty `source_structure_scan_note` confirming that the classification and scan were completed.

Use slide-level `source_item_mapping`:

```json
{
  "number": 4,
  "title": "某论点包含四个核心要素",
  "source_item_mapping": [
    {
      "group_id": "G-01",
      "item_id": "G-01-01",
      "visible_parent_label": "某论点",
      "visible_label": "要素一",
      "visible_message": "用一句简洁文字表达要素一的核心含义，并保留关键术语A。",
      "sequence_marker_mode": "embedded_text",
      "external_sequence_marker": "",
      "sequence_edit_note": "",
      "label_mode": "faithful_compression",
      "compression_note": "缩短原文标签并保留关键术语A和原有含义",
      "text_length_override_note": "",
      "visible_order": 1,
      "visual_module_id": "module-1"
    }
  ]
}
```

Create corresponding mappings for the other three items. The complete group still has four visible peer modules. Parent headers, connectors, arrows, evidence captions, and decorative separators do not count as peer content modules.

When the design uses external markers, change the same item to the following pattern:

```json
{
  "visible_label": "坚持长期主义",
  "visible_message": "保持战略定力并持续投入长期能力建设。",
  "sequence_marker_mode": "external_marker",
  "external_sequence_marker": "1",
  "sequence_edit_note": "删除原标签中的一是，保留外置序号1作为唯一顺序信号",
  "label_mode": "faithful_compression",
  "compression_note": "删除结构性顺序词并保留完整核心含义"
}
```

Use `text_length_override_note` when complete original wording or another required statement needs more space than the configured layout allows. Record the layout adjustment or faithful continuation; do not shorten original text to satisfy a capacity limit.

## Failed Output Conditions

Reject the outline, deck spec, prompt job, or slide image when any included source group has a changed count, missing item, added peer item, combined peer items, divided peer item, repeated item, changed parent, changed order, missing required term, changed numerical meaning, semantic drift, reversed causality, altered scope, altered polarity, altered conclusion, mixed sequence-marker modes, duplicate external markers, or simultaneous embedded and external sequence signals. Apply the same rejection rule to speaker notes only when they were explicitly requested. Reject unauthorized wording compression or missing source text. Complete original paragraphs are valid when their placement and typography are readable; original length alone is not grounds for rejection.
