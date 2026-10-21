#!/usr/bin/env python3
"""Prepare per-slide image generation jobs for codex-ppt.

This script is deterministic. It does not call an image model. It turns a
structured deck spec into one self-contained JSON job file per slide.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, Iterable, List, Optional

from slide_run_state import (
    DEFAULT_MAX_CONCURRENT_SLIDES,
    now_iso,
    rel_to_deck,
    save_jobs,
    set_run_status,
)


GLOBAL_FONT_FAMILY = "Microsoft YaHei (微软雅黑)"
GLOBAL_TYPOGRAPHY_POLICY: Dict[str, Any] = {
    "font_family": GLOBAL_FONT_FAMILY,
    "scope": (
        "all generated visible text, including titles, body text, labels, annotations, "
        "captions, citations, chart and table text, Chinese, Latin letters, numbers, "
        "and punctuation"
    ),
    "allowed_variants": "regular and bold weights within Microsoft YaHei only",
    "style_flexibility": (
        "font size, weight, color, alignment, spacing, and hierarchy may vary while the "
        "font family remains Microsoft YaHei"
    ),
    "forbidden": (
        "all other font families and imitations, including serif, handwritten, display, "
        "monospace, calligraphic, and decorative type"
    ),
    "strict_input_asset_exception": (
        "text already baked into a strict supplied image remains unchanged; do not redraw "
        "or re-typeset that source asset"
    ),
    "override_rule": (
        "this policy overrides every deck style, reusable style brief, approved sample, "
        "and visual reference typography direction"
    ),
}


def _die(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(1)


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        _die(f"Spec file not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        _die(f"Invalid JSON in {path}: {exc}")
    if not isinstance(data, dict):
        _die("Deck spec must be a JSON object.")
    return data


def _as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _string_list(value: Any) -> List[str]:
    return [str(item).strip() for item in _as_list(value) if str(item).strip()]


def _style_with_global_typography(style: Any) -> Dict[str, Any]:
    if isinstance(style, dict):
        normalized = dict(style)
    elif style in (None, ""):
        normalized = {}
    else:
        normalized = {"visual_direction": style}
    normalized["typography"] = dict(GLOBAL_TYPOGRAPHY_POLICY)
    normalized["typography_override_rule"] = (
        "Preserve the selected style through composition, palette, texture, scale, weight, "
        "spacing, and alignment. Use Microsoft YaHei for every generated text element."
    )
    return normalized


_MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def _parse_markdown_image(value: str) -> Optional[Dict[str, str]]:
    match = _MARKDOWN_IMAGE_RE.search(value)
    if not match:
        return None
    alt_text = match.group(1).strip()
    path = match.group(2).strip()
    description = value[: match.start()].strip(" \t\n\r:-;")
    role_parts = [part for part in [description, alt_text] if part]
    return {
        "path": path,
        "role": " — ".join(role_parts) if role_parts else "reference image",
    }


def _resolve_image_path(path: str, *, base_dir: Path) -> str:
    path = path.strip()
    if not path:
        return path
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", path):
        return path
    candidate = Path(path)
    if candidate.is_absolute():
        return str(candidate)
    return str((base_dir / candidate).resolve())


def _normalize_input_image(entry: Any, *, slide_number: int, image_index: int, base_dir: Path) -> Dict[str, Any]:
    if isinstance(entry, dict):
        image = dict(entry)
        raw_path = image.get("path") or image.get("attachment") or image.get("markdown")
        if isinstance(raw_path, str):
            parsed = _parse_markdown_image(raw_path)
            if parsed:
                image["path"] = parsed["path"]
                image.setdefault("role", parsed["role"])
        if isinstance(image.get("path"), str):
            image["path"] = _resolve_image_path(image["path"], base_dir=base_dir)
        return image
    if isinstance(entry, str):
        parsed = _parse_markdown_image(entry)
        if not parsed:
            _die(
                f"Slide {slide_number}: required_images entry {image_index} must be an "
                "object or a Markdown image reference like ![alt](path)."
            )
        lowered = entry.lower()
        fidelity = ""
        if "strict input asset" in lowered:
            fidelity = "strict input asset; preserve the supplied image content"
        return {
            "path": _resolve_image_path(parsed["path"], base_dir=base_dir),
            "role": parsed["role"],
            "fidelity": fidelity,
        }
    _die(f"Slide {slide_number}: required_images entry {image_index} has unsupported type.")


def _slide_images(slide: Dict[str, Any], *, slide_number: int, base_dir: Path) -> List[Dict[str, Any]]:
    images: List[Dict[str, Any]] = []
    for index, image in enumerate(_as_list(slide.get("required_images") or slide.get("input_images")), start=1):
        images.append(_normalize_input_image(image, slide_number=slide_number, image_index=index, base_dir=base_dir))
    return images


def _sample_generation_method(spec: Dict[str, Any], *, base_dir: Path) -> Optional[Dict[str, Any]]:
    method = spec.get("sample_generation_method") or spec.get("image_generation_method")
    if method is None:
        return None
    if not isinstance(method, dict):
        _die("sample_generation_method must be an object when present.")
    method = dict(method)
    for key in ("approved_sample_path", "sample_slide_path", "sample_output_path"):
        if isinstance(method.get(key), str):
            method[key] = _resolve_image_path(method[key], base_dir=base_dir)
    return method


def _method_backend_label(method: Optional[Dict[str, Any]]) -> Optional[str]:
    if not method:
        return None
    for key in ("backend_used", "selected_backend", "backend", "tool_name"):
        value = method.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _format_block(title: str, value: Any) -> str:
    if value is None or value == "" or value == [] or value == {}:
        return ""
    if isinstance(value, (dict, list)):
        body = json.dumps(value, ensure_ascii=False, indent=2)
    else:
        body = str(value).strip()
    return f"## {title}\n{body}\n"


def _format_input_images(images: Iterable[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for idx, image in enumerate(images, start=1):
        path = str(image.get("path") or image.get("attachment") or "").strip()
        role = str(image.get("role") or "reference image").strip()
        fidelity = str(image.get("fidelity") or image.get("constraints") or "").strip()
        if not path:
            _die(f"Input image {idx} is missing path or attachment.")
        if fidelity:
            lines.append(f"- Image {idx}: {path} — {role}; {fidelity}")
        else:
            lines.append(f"- Image {idx}: {path} — {role}")
    return "\n".join(lines)


def _slide_number(slide: Dict[str, Any], fallback: int) -> int:
    raw = slide.get("number", fallback)
    try:
        number = int(raw)
    except (TypeError, ValueError):
        _die(f"Invalid slide number: {raw}")
    if number <= 0:
        _die(f"Slide number must be positive: {number}")
    return number


_REPORT_SOURCE_MARKERS = (
    "word",
    "docx",
    "pdf",
    "text report",
    "written report",
    "source report",
    "document report",
    "报告",
    "文字材料",
    "文档",
)

_SEQUENCE_PREFIX_RE = re.compile(
    r"^\s*(?:"
    r"[（(](?:[一二三四五六七八九十百]+|\d+)[）)]"
    r"|(?:[一二三四五六七八九十百]+|\d+)\s*[、.．:：]"
    r"|[A-Za-z]\s*[、.．:：]"
    r")",
    re.MULTILINE,
)
_SEQUENCE_WORD_RE = re.compile(
    r"(?:"
    r"[一二三四五六七八九十]是"
    r"|首先|其次|再次|最后"
    r"|其[一二三四五六七八九十]"
    r"|第(?:[一二三四五六七八九十百]+|\d+)(?:项|点|步|阶段|部分|层|类|方面|条|章|节|个)?"
    r"|(?:要素|阶段|步骤|环节|层级|方面|部分|路径|措施|原则|任务|举措)(?:[一二三四五六七八九十百]+|\d+)"
    r"|\b(?:element|stage|step|phase|item|part|measure|principle)\s+(?:one|two|three|four|five|six|seven|eight|nine|ten|\d+)\b"
    r"|\b(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|firstly|secondly|thirdly|finally)\b"
    r")",
    re.IGNORECASE,
)
_EXTERNAL_SEQUENCE_MARKER_RE = re.compile(
    r"^\s*[（(]?(?:\d+|[A-Za-z]+|[一二三四五六七八九十百]+|[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+)[）)]?[、.．:：]?\s*$",
    re.IGNORECASE,
)


def _contains_sequence_wording(value: Any) -> bool:
    text = str(value or "").strip()
    return bool(text and (_SEQUENCE_PREFIX_RE.search(text) or _SEQUENCE_WORD_RE.search(text)))


def _canonical_sequence_marker(value: Any) -> str:
    return re.sub(r"[\s（()）、.．:：]+", "", str(value or "")).casefold()


def _is_report_grounded(spec: Dict[str, Any]) -> bool:
    if "source_structure_ledger" in spec:
        return True
    grounding = spec.get("source_grounding")
    values: List[str] = []
    if isinstance(grounding, dict):
        for key in ("source_type", "source_scope"):
            value = grounding.get(key)
            if value not in (None, ""):
                values.append(str(value))
    for key in ("source_type", "source_scope"):
        value = spec.get(key)
        if value not in (None, ""):
            values.append(str(value))
    source_description = " ".join(values).lower()
    return any(marker in source_description for marker in _REPORT_SOURCE_MARKERS)


def _required_text(value: Any, *, field: str) -> str:
    text = str(value).strip() if value is not None else ""
    if not text:
        _die(f"{field} must be a non-empty string.")
    return text


def _positive_int(value: Any, *, field: str) -> int:
    if isinstance(value, bool):
        _die(f"{field} must be a positive integer.")
    try:
        number = int(value)
    except (TypeError, ValueError):
        _die(f"{field} must be a positive integer.")
    if number <= 0:
        _die(f"{field} must be a positive integer.")
    return number


def _validate_source_structure(
    spec: Dict[str, Any],
    numbered_slides: List[tuple[int, Dict[str, Any], int]],
) -> Dict[int, Dict[str, Any]]:
    raw_text_limits = spec.get("presentation_text_limits", {})
    if not isinstance(raw_text_limits, dict):
        _die("presentation_text_limits must be an object when present.")
    # Only caller-supplied limits can block prompt preparation. The historical
    # 36/80 defaults are non-blocking layout review thresholds.
    explicit_text_limits = {
        name: _positive_int(raw_text_limits[name], field=f"presentation_text_limits.{name}")
        for name in ("visible_label_max_chars", "visible_message_max_chars")
        if name in raw_text_limits
    }
    advisory_text_lengths = {"visible_label_max_chars": 36, "visible_message_max_chars": 80}
    text_capacity_diagnostics: Dict[int, List[Dict[str, Any]]] = {}
    ledger = spec.get("source_structure_ledger")
    if ledger is None:
        if _is_report_grounded(spec):
            _die(
                "Report-grounded deck specs must include source_structure_ledger. "
                "Read docs/source-fidelity-and-structure-conservation.md."
            )
        return {}
    if not isinstance(ledger, list):
        _die("source_structure_ledger must be an array.")
    if not ledger and not str(spec.get("source_structure_scan_note") or "").strip():
        _die(
            "An empty source_structure_ledger requires a non-empty "
            "source_structure_scan_note confirming that the source scan was completed."
        )

    groups: Dict[str, Dict[str, Any]] = {}
    global_item_ids: Dict[str, str] = {}
    allowed_statuses = {"included", "excluded_with_user_approval"}

    for group_index, raw_group in enumerate(ledger, start=1):
        if not isinstance(raw_group, dict):
            _die(f"source_structure_ledger group {group_index} must be an object.")
        group_id = _required_text(
            raw_group.get("group_id"), field=f"source_structure_ledger group {group_index}.group_id"
        )
        if group_id in groups:
            _die(f"Duplicate source structure group_id: {group_id}")
        parent_label = _required_text(
            raw_group.get("parent_label"), field=f"source_structure_ledger {group_id}.parent_label"
        )
        core_viewpoint = _required_text(
            raw_group.get("core_viewpoint"),
            field=f"source_structure_ledger {group_id}.core_viewpoint",
        )
        _required_text(
            raw_group.get("source_basis"), field=f"source_structure_ledger {group_id}.source_basis"
        )
        source_count = _positive_int(
            raw_group.get("source_count"), field=f"source_structure_ledger {group_id}.source_count"
        )
        deck_status = _required_text(
            raw_group.get("deck_status"), field=f"source_structure_ledger {group_id}.deck_status"
        )
        if deck_status not in allowed_statuses:
            _die(
                f"source_structure_ledger {group_id}.deck_status must be one of: "
                f"{', '.join(sorted(allowed_statuses))}."
            )
        if deck_status == "excluded_with_user_approval":
            _required_text(
                raw_group.get("approval_note"),
                field=f"source_structure_ledger {group_id}.approval_note",
            )

        ordered_items = raw_group.get("ordered_items")
        if not isinstance(ordered_items, list):
            _die(f"source_structure_ledger {group_id}.ordered_items must be an array.")
        if len(ordered_items) != source_count:
            _die(
                f"source_structure_ledger {group_id} count mismatch: source_count={source_count}, "
                f"ordered_items={len(ordered_items)}."
            )

        items: Dict[str, Dict[str, Any]] = {}
        item_orders: List[int] = []
        for item_index, raw_item in enumerate(ordered_items, start=1):
            if not isinstance(raw_item, dict):
                _die(f"source_structure_ledger {group_id} item {item_index} must be an object.")
            item_id = _required_text(
                raw_item.get("item_id"),
                field=f"source_structure_ledger {group_id} item {item_index}.item_id",
            )
            if item_id in items:
                _die(f"Duplicate item_id {item_id} inside source group {group_id}.")
            if item_id in global_item_ids:
                _die(
                    f"Duplicate item_id {item_id} across source groups "
                    f"{global_item_ids[item_id]} and {group_id}."
                )
            label = _required_text(
                raw_item.get("label"),
                field=f"source_structure_ledger {group_id}.{item_id}.label",
            )
            core_meaning = _required_text(
                raw_item.get("core_meaning"),
                field=f"source_structure_ledger {group_id}.{item_id}.core_meaning",
            )
            raw_required_terms = raw_item.get("required_terms")
            if not isinstance(raw_required_terms, list):
                _die(
                    f"source_structure_ledger {group_id}.{item_id}.required_terms "
                    "must be an array, which may be empty."
                )
            required_terms = _string_list(raw_required_terms)
            if len(required_terms) != len(raw_required_terms):
                _die(
                    f"source_structure_ledger {group_id}.{item_id}.required_terms "
                    "must contain only non-empty strings."
                )
            order = _positive_int(
                raw_item.get("order"),
                field=f"source_structure_ledger {group_id}.{item_id}.order",
            )
            items[item_id] = {
                "label": label,
                "core_meaning": core_meaning,
                "required_terms": required_terms,
                "order": order,
            }
            global_item_ids[item_id] = group_id
            item_orders.append(order)

        expected_orders = list(range(1, source_count + 1))
        if item_orders != expected_orders:
            _die(
                f"source_structure_ledger {group_id} item order must be exactly "
                f"{expected_orders}; found {item_orders}."
            )
        groups[group_id] = {
            "group_id": group_id,
            "parent_label": parent_label,
            "core_viewpoint": core_viewpoint,
            "source_count": source_count,
            "deck_status": deck_status,
            "items": items,
            "source_has_explicit_sequence_wording": any(
                _contains_sequence_wording(f"{item['label']}\n{item['core_meaning']}")
                for item in items.values()
            ),
        }

    mapped_items: Dict[tuple[str, str], tuple[int, int]] = {}
    mappings_by_group: Dict[str, List[Dict[str, Any]]] = {group_id: [] for group_id in groups}
    slide_group_mappings: Dict[int, Dict[str, List[Dict[str, Any]]]] = {}
    allowed_sequence_marker_modes = {"embedded_text", "external_marker", "none"}

    for _, slide, slide_number in numbered_slides:
        raw_mappings = slide.get("source_item_mapping", [])
        if raw_mappings is None:
            raw_mappings = []
        if not isinstance(raw_mappings, list):
            _die(f"Slide {slide_number}: source_item_mapping must be an array.")
        used_visual_modules: Dict[str, int] = {}
        for mapping_index, raw_mapping in enumerate(raw_mappings, start=1):
            if not isinstance(raw_mapping, dict):
                _die(f"Slide {slide_number}: source_item_mapping {mapping_index} must be an object.")
            group_id = _required_text(
                raw_mapping.get("group_id"),
                field=f"Slide {slide_number} source_item_mapping {mapping_index}.group_id",
            )
            item_id = _required_text(
                raw_mapping.get("item_id"),
                field=f"Slide {slide_number} source_item_mapping {mapping_index}.item_id",
            )
            if group_id not in groups:
                _die(f"Slide {slide_number}: source mapping references unknown group_id {group_id}.")
            group = groups[group_id]
            if group["deck_status"] != "included":
                _die(f"Slide {slide_number}: excluded source group {group_id} cannot be mapped.")
            if item_id not in group["items"]:
                _die(
                    f"Slide {slide_number}: source mapping references unknown item_id "
                    f"{item_id} in group {group_id}."
                )
            item = group["items"][item_id]
            visible_parent_label = _required_text(
                raw_mapping.get("visible_parent_label"),
                field=f"Slide {slide_number} {group_id}.{item_id}.visible_parent_label",
            )
            visible_label = _required_text(
                raw_mapping.get("visible_label"),
                field=f"Slide {slide_number} {group_id}.{item_id}.visible_label",
            )
            visible_message = _required_text(
                raw_mapping.get("visible_message"),
                field=f"Slide {slide_number} {group_id}.{item_id}.visible_message",
            )
            sequence_marker_mode = _required_text(
                raw_mapping.get("sequence_marker_mode"),
                field=f"Slide {slide_number} {group_id}.{item_id}.sequence_marker_mode",
            )
            if sequence_marker_mode not in allowed_sequence_marker_modes:
                _die(
                    f"Slide {slide_number}: sequence_marker_mode for {group_id}.{item_id} "
                    "must be 'embedded_text', 'external_marker', or 'none'."
                )
            external_sequence_marker = str(
                raw_mapping.get("external_sequence_marker") or ""
            ).strip()
            sequence_edit_note = str(raw_mapping.get("sequence_edit_note") or "").strip()
            visible_has_sequence_wording = _contains_sequence_wording(
                f"{visible_label}\n{visible_message}"
            )
            if sequence_marker_mode == "embedded_text":
                if not visible_has_sequence_wording:
                    _die(
                        f"Slide {slide_number}: embedded_text mode for {group_id}.{item_id} "
                        "requires one explicit sequence expression in visible_label or "
                        "visible_message."
                    )
                if external_sequence_marker:
                    _die(
                        f"Slide {slide_number}: embedded_text mode for {group_id}.{item_id} "
                        "forbids external_sequence_marker."
                    )
                if sequence_edit_note:
                    _die(
                        f"Slide {slide_number}: embedded_text mode for {group_id}.{item_id} "
                        "does not use sequence_edit_note."
                    )
            elif sequence_marker_mode == "external_marker":
                if visible_has_sequence_wording:
                    _die(
                        f"Slide {slide_number}: external_marker mode for {group_id}.{item_id} "
                        "requires visible_label and visible_message to remove sequence wording "
                        "such as 一是, 首先, 第一, 1., or A."
                    )
                if not external_sequence_marker:
                    _die(
                        f"Slide {slide_number}: external_marker mode for {group_id}.{item_id} "
                        "requires a non-empty external_sequence_marker."
                    )
                if not _EXTERNAL_SEQUENCE_MARKER_RE.fullmatch(external_sequence_marker):
                    _die(
                        f"Slide {slide_number}: external_sequence_marker for "
                        f"{group_id}.{item_id} must be a compact number, letter, Chinese "
                        "numeral, or Roman numeral, with optional surrounding punctuation."
                    )
                if not sequence_edit_note:
                    _die(
                        f"Slide {slide_number}: external_marker mode for {group_id}.{item_id} "
                        "requires a non-empty sequence_edit_note."
                    )
            else:
                if visible_has_sequence_wording:
                    _die(
                        f"Slide {slide_number}: none sequence-marker mode for "
                        f"{group_id}.{item_id} forbids explicit sequence wording."
                    )
                if external_sequence_marker:
                    _die(
                        f"Slide {slide_number}: none sequence-marker mode for "
                        f"{group_id}.{item_id} forbids external_sequence_marker."
                    )
                if sequence_edit_note:
                    _die(
                        f"Slide {slide_number}: none sequence-marker mode for "
                        f"{group_id}.{item_id} does not use sequence_edit_note."
                    )
            label_mode = _required_text(
                raw_mapping.get("label_mode"),
                field=f"Slide {slide_number} {group_id}.{item_id}.label_mode",
            )
            if label_mode not in {"exact", "faithful_compression"}:
                _die(
                    f"Slide {slide_number}: label_mode for {group_id}.{item_id} must be "
                    "'exact' or 'faithful_compression'."
                )
            compression_note = str(raw_mapping.get("compression_note") or "").strip()
            text_length_override_note = str(
                raw_mapping.get("text_length_override_note") or ""
            ).strip()
            visible_text_lengths = {
                "visible_label_max_chars": len(visible_label),
                "visible_message_max_chars": len(visible_message),
            }
            exceeded_explicit_limits = {
                name: {"actual_chars": visible_text_lengths[name], "limit": limit}
                for name, limit in explicit_text_limits.items()
                if visible_text_lengths[name] > limit
            }
            if exceeded_explicit_limits and not text_length_override_note:
                _die(
                    f"Slide {slide_number}: visible wording for {group_id}.{item_id} exceeds "
                    f"explicit presentation text limits: {exceeded_explicit_limits}. "
                    "Preserve complete meaning; resolve the explicit constraint and layout "
                    "or record an approved text_length_override_note."
                )
            for name, threshold in advisory_text_lengths.items():
                if name not in explicit_text_limits and visible_text_lengths[name] > threshold:
                    text_capacity_diagnostics.setdefault(slide_number, []).append({
                        "group_id": group_id,
                        "item_id": item_id,
                        "field": name.removesuffix("_max_chars"),
                        "actual_chars": visible_text_lengths[name],
                        "advisory_threshold": threshold,
                        "blocking": False,
                        "message": "Preserve the complete wording and inspect the rendered layout; enlarge or rearrange the container, or use a clearly linked continuation. Do not cut relationships, conditions, or source items to fit.",
                    })
            visible_order = _positive_int(
                raw_mapping.get("visible_order"),
                field=f"Slide {slide_number} {group_id}.{item_id}.visible_order",
            )
            visual_module_id = _required_text(
                raw_mapping.get("visual_module_id"),
                field=f"Slide {slide_number} {group_id}.{item_id}.visual_module_id",
            )

            if visible_parent_label != group["parent_label"]:
                _die(
                    f"Slide {slide_number}: parent label changed for {group_id}.{item_id}; "
                    f"expected {group['parent_label']!r}, found {visible_parent_label!r}."
                )
            if visible_label == item["label"] and label_mode != "exact":
                _die(
                    f"Slide {slide_number}: unchanged label for {group_id}.{item_id} "
                    "must use label_mode='exact'."
                )
            if visible_label != item["label"]:
                if label_mode != "faithful_compression":
                    _die(
                        f"Slide {slide_number}: changed visible label for {group_id}.{item_id} "
                        "requires label_mode='faithful_compression'."
                    )
                if not compression_note:
                    _die(
                        f"Slide {slide_number}: faithful label compression for "
                        f"{group_id}.{item_id} requires a non-empty compression_note."
                    )
            visible_text = f"{visible_label}\n{visible_message}".casefold()
            missing_required_terms = [
                term for term in item["required_terms"] if term.casefold() not in visible_text
            ]
            if missing_required_terms:
                _die(
                    f"Slide {slide_number}: visible wording for {group_id}.{item_id} "
                    f"is missing required_terms={missing_required_terms}."
                )
            if visible_order != item["order"]:
                _die(
                    f"Slide {slide_number}: item order changed for {group_id}.{item_id}; "
                    f"expected {item['order']}, found {visible_order}."
                )
            if visual_module_id in used_visual_modules:
                _die(
                    f"Slide {slide_number}: visual_module_id {visual_module_id!r} is reused by "
                    "multiple source items. Each source item requires a distinct visible module."
                )
            used_visual_modules[visual_module_id] = mapping_index

            mapping_key = (group_id, item_id)
            if mapping_key in mapped_items:
                previous_slide, previous_index = mapped_items[mapping_key]
                _die(
                    f"Duplicate source item mapping for {group_id}.{item_id}: "
                    f"slide {previous_slide} mapping {previous_index} and "
                    f"slide {slide_number} mapping {mapping_index}."
                )
            mapped_items[mapping_key] = (slide_number, mapping_index)
            validated_mapping = {
                "group_id": group_id,
                "item_id": item_id,
                "visible_parent_label": visible_parent_label,
                "visible_label": visible_label,
                "visible_message": visible_message,
                "sequence_marker_mode": sequence_marker_mode,
                "external_sequence_marker": external_sequence_marker,
                "sequence_edit_note": sequence_edit_note,
                "label_mode": label_mode,
                "compression_note": compression_note,
                "text_length_override_note": text_length_override_note,
                "visible_order": visible_order,
                "visual_module_id": visual_module_id,
                "slide_number": slide_number,
                "mapping_index": mapping_index,
            }
            mappings_by_group[group_id].append(validated_mapping)
            slide_group_mappings.setdefault(slide_number, {}).setdefault(group_id, []).append(
                validated_mapping
            )

    for group_id, group in groups.items():
        group_mappings = mappings_by_group[group_id]
        if group["deck_status"] == "excluded_with_user_approval":
            if group_mappings:
                _die(f"Excluded source group {group_id} has slide mappings.")
            continue
        expected_item_ids = set(group["items"])
        mapped_item_ids = {mapping["item_id"] for mapping in group_mappings}
        missing_item_ids = sorted(expected_item_ids - mapped_item_ids)
        extra_item_ids = sorted(mapped_item_ids - expected_item_ids)
        if missing_item_ids or extra_item_ids:
            details: List[str] = []
            if missing_item_ids:
                details.append(f"missing={missing_item_ids}")
            if extra_item_ids:
                details.append(f"extra={extra_item_ids}")
            _die(f"Source group {group_id} mapping is incomplete: {', '.join(details)}.")
        sequence_marker_modes = {
            mapping["sequence_marker_mode"] for mapping in group_mappings
        }
        if len(sequence_marker_modes) != 1:
            _die(
                f"Source group {group_id} mixes sequence_marker_mode values "
                f"{sorted(sequence_marker_modes)}. Use one consistent mode for the group."
            )
        group_sequence_marker_mode = next(iter(sequence_marker_modes))
        if (
            group["source_has_explicit_sequence_wording"]
            and group_sequence_marker_mode == "none"
        ):
            _die(
                f"Source group {group_id} contains explicit sequence wording in the source. "
                "Use embedded_text or external_marker so the order signal remains visible."
            )
        if group_sequence_marker_mode == "external_marker":
            external_markers = [
                _canonical_sequence_marker(mapping["external_sequence_marker"])
                for mapping in group_mappings
            ]
            if len(external_markers) != len(set(external_markers)):
                _die(
                    f"Source group {group_id} reuses external_sequence_marker values. "
                    "Every mapped item requires one unique external marker."
                )
        ordered_mappings = sorted(
            group_mappings, key=lambda mapping: (mapping["slide_number"], mapping["mapping_index"])
        )
        mapped_orders = [mapping["visible_order"] for mapping in ordered_mappings]
        expected_orders = list(range(1, group["source_count"] + 1))
        if mapped_orders != expected_orders:
            _die(
                f"Source group {group_id} deck order changed: expected {expected_orders}, "
                f"found {mapped_orders}."
            )

    contracts: Dict[int, Dict[str, Any]] = {}
    for slide_number, grouped_mappings in slide_group_mappings.items():
        contract_groups: List[Dict[str, Any]] = []
        total_visible_modules = 0
        for group_id, group_mappings in grouped_mappings.items():
            group = groups[group_id]
            sorted_mappings = sorted(group_mappings, key=lambda mapping: mapping["visible_order"])
            visible_count = len(sorted_mappings)
            total_visible_modules += visible_count
            contract_groups.append(
                {
                    "group_id": group_id,
                    "required_visible_parent_label": group["parent_label"],
                    "core_viewpoint": group["core_viewpoint"],
                    "source_total_count": group["source_count"],
                    "slide_visible_module_count": visible_count,
                    "continuation_across_slides": visible_count != group["source_count"],
                    "sequence_marker_mode": sorted_mappings[0]["sequence_marker_mode"],
                    "required_items": [
                        {
                            "item_id": mapping["item_id"],
                            "source_label": group["items"][mapping["item_id"]]["label"],
                            "core_meaning": group["items"][mapping["item_id"]]["core_meaning"],
                            "required_terms": group["items"][mapping["item_id"]]["required_terms"],
                            "visible_label": mapping["visible_label"],
                            "visible_message": mapping["visible_message"],
                            "sequence_marker_mode": mapping["sequence_marker_mode"],
                            "external_sequence_marker": mapping[
                                "external_sequence_marker"
                            ],
                            "sequence_edit_note": mapping["sequence_edit_note"],
                            "label_mode": mapping["label_mode"],
                            "compression_note": mapping["compression_note"],
                            "text_length_override_note": mapping[
                                "text_length_override_note"
                            ],
                            "visible_order": mapping["visible_order"],
                            "visual_module_id": mapping["visual_module_id"],
                        }
                        for mapping in sorted_mappings
                    ],
                    "count_rule": (
                        f"Render exactly {visible_count} distinct peer content module(s) on this "
                        f"slide for source group {group_id}. Preserve core meaning and required "
                        "terms. Do not add, merge, split, omit, duplicate, semantically alter, "
                        "reparent, or reorder source items."
                    ),
                    "sequence_marker_rule": (
                        "Use exactly one sequence signal per item. In embedded_text mode, keep "
                        "the sequence wording inside the approved visible text and add no "
                        "numeric or alphabetic badge. In external_marker mode, render each "
                        "external_sequence_marker exactly once and do not restore removed "
                        "sequence wording. In none mode, render no sequence marker. Never "
                        "render visible_order as audience-facing text."
                    ),
                }
            )
        contracts[slide_number] = {
            "validation_status": "passed",
            "presentation_text_limits": dict(explicit_text_limits),
            "text_capacity_diagnostics": text_capacity_diagnostics.get(slide_number, []),
            "total_expected_visible_peer_modules": total_visible_modules,
            "groups": contract_groups,
        }
    return contracts


def _build_prompt(
    *,
    deck: Dict[str, Any],
    slide: Dict[str, Any],
    number: int,
    global_style_reference: Optional[Dict[str, Any]],
    source_fidelity_contract: Optional[Dict[str, Any]],
    base_dir: Path,
) -> str:
    title = str(slide.get("title") or f"Slide {number}").strip()
    headline_guidance = (
        slide.get("headline_guidance")
        or slide.get("title_guidance")
        or slide.get("storyline")
        or slide.get("core_viewpoint")
        or slide.get("core_message")
        or slide.get("takeaway")
        or slide.get("subtitle")
    )
    style = _style_with_global_typography(deck.get("style", {}))
    images: List[Dict[str, Any]] = []
    if global_style_reference:
        images.append(global_style_reference)
    images.extend(_slide_images(slide, slide_number=number, base_dir=base_dir))
    required_background = {
        key: value
        for key, value in {
            "deck_context": deck.get("deck_context"),
            "source_grounding": deck.get("source_grounding"),
            "source_report_rules": deck.get("source_report_rules"),
            "slide_local_context": slide.get("local_context"),
            "slide_source_basis": slide.get("source_basis"),
            "slide_source_evidence": slide.get("source_evidence"),
            "slide_source_excerpt": slide.get("source_excerpt"),
            "slide_source_fidelity_contract": source_fidelity_contract,
        }.items()
        if value not in (None, "", [], {})
    }
    canvas = {
        "type": "16:9 full-slide PowerPoint image",
        "language": deck.get("language", "Chinese"),
        "slide_number": number,
        "render_slide_number": bool(deck.get("render_slide_number", False)),
    }
    if isinstance(deck.get("canvas"), dict):
        canvas.update(deck["canvas"])
        canvas["slide_number"] = number
    render_slide_number = bool(canvas.get("render_slide_number"))

    prompt_parts = [
        "# Codex PPT Slide Image Prompt\n",
        _format_block("Canvas", canvas),
        _format_block("Deck Goal", deck.get("goal")),
        _format_block("Required Background", required_background),
        _format_block("Global Typography Policy", GLOBAL_TYPOGRAPHY_POLICY),
        _format_block("Global Style", style),
    ]

    if images:
        prompt_parts.append("## Input Images\n")
        prompt_parts.append(_format_input_images(images))
        prompt_parts.append("\n")

    prompt_parts.extend(
        [
            _format_block("Slide", {
                "number": number,
                "title": title,
                "role": slide.get("role"),
                "intent": slide.get("intent"),
            }),
            _format_block("Text", {
                "title": title,
                "top_headline": title,
                "headline_guidance": headline_guidance,
                "headline_rule": (
                    "Use the topmost title/headline as the page's core statement. Render that "
                    "title once at the top. Do not add a separate labelled row or subtitle for "
                    "a storyline/core viewpoint."
                ),
                "key_points": _string_list(slide.get("key_points")),
                "speaker_focus": slide.get("speaker_focus"),
            }),
            _format_block("Source Grounding", {
                "source_basis": slide.get("source_basis"),
                "source_evidence": slide.get("source_evidence"),
                "source_excerpt": slide.get("source_excerpt"),
                "grounding_rule": slide.get("grounding_rule"),
            }),
            _format_block("Source Fidelity Contract", source_fidelity_contract),
            _format_block("Layout", slide.get("layout")),
            _format_block("Visual Elements", slide.get("visual_elements")),
            _format_block("Source Image Rules", slide.get("source_image_rules")),
            _format_block("Constraints", _string_list(slide.get("constraints"))),
        ]
    )

    if global_style_reference:
        prompt_parts.append(
            "## Style Reference Rule\n"
            "Use Image 1 as the approved sample-slide style reference. Match its palette, "
            "typographic scale, weight, spacing, alignment, density, texture, and overall "
            "visual identity. Re-typeset every generated text element in Microsoft YaHei, "
            "even when the sample uses another font family. Do not copy its exact layout "
            "unless this slide's layout explicitly asks for it.\n"
        )

    if images:
        prompt_parts.append(
            "## Input Image Handling Rules\n"
            "For any input image marked as a strict input asset, include it visibly and "
            "preserve its content. Do not redraw, replace, relabel, or invent a similar "
            "figure. Scale and crop only as needed for composition while keeping the "
            "important labels, arrows, data, and relationships recognizable.\n"
        )

    slide_number_rule = (
        "- Render only the explicitly requested slide number; keep it small and do not add template footer/page-marker blocks.\n"
        if render_slide_number
        else "- No watermark, unrelated logo, or extra slide number.\n"
    )
    source_fidelity_rule = ""
    if source_fidelity_contract:
        source_fidelity_rule = (
            "- Follow the Source Fidelity Contract exactly. Render one distinct visible peer "
            "content module for every mapped source item. Preserve the exact visible module count, "
            "core meaning, required terms, parent label, and item order. Use the approved complete "
            "visible labels and messages. Do not add, merge, split, omit, duplicate, semantically "
            "alter, reparent, or reorder mapped source items. Parent headers, connectors, "
            "arrows, evidence captions, and decorative separators do not count as peer content "
            "modules. Use exactly one sequence signal per mapped item. If sequence_marker_mode "
            "is embedded_text, retain the approved sequence wording and add no numeric or "
            "alphabetic marker. If it is external_marker, render external_sequence_marker once "
            "and do not restore any removed ordinal wording. If it is none, add no sequence "
            "wording or marker. visible_order is validation metadata and must not be rendered.\n"
        )
    prompt_parts.append(
        "## Universal Constraints\n"
        "- The final image itself must contain the title and approved key content. When a Source Fidelity Contract is present, its visible_label and visible_message fields are the sole approved wording for mapped source items and supersede alternative key_points wording.\n"
        "- If this deck is based on a Word/PDF/text report, every visible claim, label, title/headline, recommendation, data point, and comparison must be grounded in the provided source text or explicitly supplied source assets. Do not invent facts, cases, numbers, citations, external benchmarks, causes, risks, or suggestions.\n"
        "- Treat source-grounding fields as content boundaries: write natural, complete explanations while preserving every source level and supporting item; remove only genuinely repeated wording and do not add unsupported meaning.\n"
        f"{source_fidelity_rule}"
        "- Preserve viewpoints and all supporting items at every source level. Use natural labels and complete explanations; keep objects, actions, relationships, conditions, item counts, order, and parents. Do not omit supporting items for space.\n"
        "- The Source Fidelity Contract has no default writing length limit. text_capacity_diagnostics are non-blocking layout reminders: keep complete wording and adapt the layout. Enforce only explicitly supplied presentation_text_limits, unless an approved text_length_override_note records an agreed exception.\n"
        "- Treat source_basis, source_evidence, filenames, attachment labels, and file types as internal-only provenance. In audience-facing text, state supported content directly. Do not render phrases such as '用户提供', '你提供的资料', '根据附件', '从Excel可见', '结合原报告', or any mention of prompts or the production process. If source disclosure is explicitly required, use only a neutral document title, organization, and/or date citation.\n"
        "- For normal consulting/report content slides, treat the topmost title/headline as the page storyline. Do not add any separate storyline/core-viewpoint row below the title.\n"
        "- Use Microsoft YaHei (微软雅黑) as the only font family for every generated visible text element, including Chinese, Latin letters, numbers, punctuation, titles, body text, labels, annotations, captions, citations, and chart/table text. Regular and bold weights are allowed within the same family. Do not use or imitate serif, handwritten, display, monospace, calligraphic, decorative, or fallback fonts. This rule overrides all style briefs and sample/reference typography. Text already baked into a strict input asset remains unchanged.\n"
        "- Render Chinese text exactly and legibly; avoid garbled characters.\n"
        "- Keep the confirmed deck style consistent while varying layout by slide role.\n"
        "- For consulting/report slides, make the main body a text-rich logic structure: labelled boxes, hierarchy frames, process lanes, matrices, comparison columns, causal chains, or conclusion callout boxes.\n"
        "- Let complete source content determine page density and spacing. Do not add, split, merge, omit, or shorten source items to fill the page.\n"
        "- Preserve the original count and nesting at every source level; do not impose a minimum text-unit count. First reconcile the source structure, then obtain independent review of the rendered wording before delivery.\n"
        "- If a summary viewpoint is needed, place it in the top headline or in a compact insight band between the title and the main body. Do not put summary, evidence, or takeaway text boxes at the bottom of the page.\n"
        "- Summary viewpoints must be logical and source-grounded: conclusions, implications, cause-effect judgements, or decision criteria. Do not use generic slogans, motivational phrases, decorative golden sentences, or unsupported catchphrases.\n"
        "- Do not add bottom takeaway boxes, paired bottom text boxes, bottom evidence boxes, bottom conclusion callouts, or bottom full-width conclusion slogan strips.\n"
        "- Omit decorative icons by default. Avoid icon rows, icon-only cards, repeated icon bullet rows, and decorative icon clusters unless explicitly requested.\n"
        f"{slide_number_rule}"
    )
    return "\n".join(part for part in prompt_parts if part)


def _job_images(
    slide: Dict[str, Any],
    *,
    number: int,
    global_style_reference: Optional[Dict[str, Any]],
    base_dir: Path,
) -> List[Dict[str, Any]]:
    images: List[Dict[str, Any]] = []
    if global_style_reference:
        images.append(global_style_reference)
    images.extend(_slide_images(slide, slide_number=number, base_dir=base_dir))
    return images


def _write_template(path: Path) -> None:
    template = {
        "deck_name": "example-deck",
        "language": "Chinese",
        "goal": "Explain the core idea of the source article.",
        "canvas": {
            "aspect_ratio": "16:9",
            "use_full_canvas": True,
            "render_slide_number": False,
        },
        "font_policy": dict(GLOBAL_TYPOGRAPHY_POLICY),
        "deck_context": {
            "source_summary": "Short source-wide summary that workers may need when a slide refers to the broader article.",
            "core_claim": "The central thesis that should stay consistent across the deck.",
            "canonical_terms": ["Term one", "Term two", "Term three"],
        },
        "source_grounding": {
            "source_type": "Word/PDF/text report",
            "grounding_rule": "All slide claims must be traceable to the report. Do not add external facts or recommendations unless explicitly requested.",
            "allowed_transformations": ["faithfully paraphrase one existing core source item", "remove genuinely repeated wording without deleting a source item", "keep supporting items under their original parent and in their original order", "turn the preserved source logic into a matching slide structure"],
            "forbidden_transformations": ["invent facts", "add external benchmarks", "add unsupported recommendations", "change numeric meaning", "change causal direction", "change scope or polarity", "add source items", "merge source items", "split source items", "omit source items", "duplicate source items", "reparent source items", "reorder source items"],
        },
        "source_structure_scan_note": "Viewpoints and all supporting items were recorded; countable groups at every source level were scanned.",
        "presentation_text_limits": {},
        "source_structure_ledger": [
            {
                "group_id": "G-01",
                "parent_label": "Four source-grounded evidence elements",
                "core_viewpoint": "The report identifies four distinct evidence elements that jointly support the conclusion.",
                "source_basis": "Report section containing the four explicit elements.",
                "source_count": 4,
                "deck_status": "included",
                "ordered_items": [
                    {"item_id": "G-01-01", "label": "The first evidence element retains Alpha as the required term", "core_meaning": "The first evidence element is defined by Alpha.", "required_terms": ["Alpha"], "order": 1},
                    {"item_id": "G-01-02", "label": "The second evidence element explains the operating condition", "core_meaning": "The second evidence element defines the operating condition.", "required_terms": [], "order": 2},
                    {"item_id": "G-01-03", "label": "The third evidence element states the observed result", "core_meaning": "The third evidence element states the observed result.", "required_terms": [], "order": 3},
                    {"item_id": "G-01-04", "label": "The fourth evidence element connects the result to the conclusion", "core_meaning": "The fourth evidence element connects the result to the conclusion.", "required_terms": [], "order": 4},
                ],
            }
        ],
        "selected_image_backend": "built-in image tool",
        "max_concurrent_slides": 6,
        "sample_generation_method": {
            "backend_used": "built-in image tool",
            "tool_name": "image_gen",
            "mode": "generate",
            "prompt_source": "the approved sample slide job prompt",
            "size": "16:9 landscape, 2560x1440 target",
            "quality": "medium",
            "approved_sample_path": "/absolute/path/to/approved-sample-slide.png",
            "input_context_preparation": "view_image local required images before built-in generation",
            "handoff_rule": "Subagents must use this same backend/tool/mode; return a blocker if unavailable.",
        },
        "style": {
            "name": "手绘技术解释风",
            "visual_direction": "clean hand-drawn technical explainer",
            "color_palette": "white background, black marker lines, pale yellow highlights",
            "typography": {
                "font_family": GLOBAL_FONT_FAMILY,
                "scope": "all generated Chinese, Latin, numeric, punctuation, title, body, label, annotation, caption, chart, and table text",
                "allowed_variants": "regular and bold weights within Microsoft YaHei only",
                "style_rule": "use scale, weight, spacing, alignment, and color to express the hand-drawn visual mood without changing font family",
            },
            "visual_structure": "for consulting/report decks, prefer medium-high density text-rich logic boxes over decorative icons and excessive blank whitespace",
        },
        "approved_style_reference": {
            "path": "/absolute/path/to/approved-sample-slide.png",
            "role": "approved sample slide style reference",
            "fidelity": "match style only; do not copy layout or content",
        },
        "slides": [
            {
                "number": 1,
                "title": "Cover",
                "role": "cover",
                "intent": "Open the talk",
                "key_points": ["Point one", "Point two"],
                "headline_guidance": "Use the top title itself to state the cover's main promise or scope; do not add a separate storyline subtitle.",
                "source_basis": "Report cover, executive summary, or stated purpose.",
                "source_evidence": ["Exact source section/page/paragraph supporting this slide."],
                "local_context": {
                    "required_background": "Facts, lists, definitions, comparisons, or prior-slide references this slide needs to be self-contained.",
                },
                "layout": {"composition": "large title with one supporting visual"},
                "visual_elements": {"main_visual": "topic-specific hand-drawn metaphor"},
                "constraints": ["Keep the cover title concise; ordinary consulting content slides should not be sparse"],
                "sample_approved": True,
            },
            {
                "number": 2,
                "title": "Evidence",
                "role": "data evidence",
                "intent": "Explain a supplied result figure",
                "key_points": [
                    "Alpha definition",
                    "Operating condition",
                    "Observed result",
                    "Conclusion link",
                ],
                "headline_guidance": "Use the top title itself as the evidence page headline; do not add a separate storyline subtitle.",
                "source_basis": "Report figure/table and surrounding explanation.",
                "source_evidence": ["Figure 2 and paragraph immediately below it."],
                "source_item_mapping": [
                    {"group_id": "G-01", "item_id": "G-01-01", "visible_parent_label": "Four source-grounded evidence elements", "visible_label": "Alpha definition", "visible_message": "Alpha defines the evidence element.", "sequence_marker_mode": "external_marker", "external_sequence_marker": "1", "sequence_edit_note": "Removed the source ordinal wording and retained one external sequence marker.", "label_mode": "faithful_compression", "compression_note": "Shortened the source label while retaining Alpha and the core meaning.", "visible_order": 1, "visual_module_id": "module-1"},
                    {"group_id": "G-01", "item_id": "G-01-02", "visible_parent_label": "Four source-grounded evidence elements", "visible_label": "Operating condition", "visible_message": "Defines the operating condition.", "sequence_marker_mode": "external_marker", "external_sequence_marker": "2", "sequence_edit_note": "Removed the source ordinal wording and retained one external sequence marker.", "label_mode": "faithful_compression", "compression_note": "Shortened the source label while retaining the core meaning.", "visible_order": 2, "visual_module_id": "module-2"},
                    {"group_id": "G-01", "item_id": "G-01-03", "visible_parent_label": "Four source-grounded evidence elements", "visible_label": "Observed result", "visible_message": "States the observed result.", "sequence_marker_mode": "external_marker", "external_sequence_marker": "3", "sequence_edit_note": "Removed the source ordinal wording and retained one external sequence marker.", "label_mode": "faithful_compression", "compression_note": "Shortened the source label while retaining the core meaning.", "visible_order": 3, "visual_module_id": "module-3"},
                    {"group_id": "G-01", "item_id": "G-01-04", "visible_parent_label": "Four source-grounded evidence elements", "visible_label": "Conclusion link", "visible_message": "Connects the result to the conclusion.", "sequence_marker_mode": "external_marker", "external_sequence_marker": "4", "sequence_edit_note": "Removed the source ordinal wording and retained one external sequence marker.", "label_mode": "faithful_compression", "compression_note": "Shortened the source label while retaining the core meaning.", "visible_order": 4, "visual_module_id": "module-4"},
                ],
                "required_images": [
                    {
                        "path": "/absolute/path/to/result_01.png",
                        "role": "strict input asset and main evidence figure",
                        "fidelity": "preserve data, axes, labels, legends, colors, and values",
                    },
                    "strict input asset and comparison chart\n\n![Result chart](assets/figures/result_02.png)",
                ],
                "layout": {"composition": "source figure left, text-rich logic explanation boxes right"},
            },
        ],
    }
    path.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", help="Deck spec JSON file.")
    parser.add_argument("--out-dir", help="Deck project directory.")
    parser.add_argument("--write-template", help="Write an example deck spec JSON and exit.")
    parser.add_argument(
        "--selected-backend",
        help="Confirmed image backend label, such as `built-in image tool` or `scripts/image_gen.py`.",
    )
    parser.add_argument(
        "--max-concurrent-slides",
        type=int,
        default=None,
        help=f"Maximum slide subagents to dispatch at once. Defaults to {DEFAULT_MAX_CONCURRENT_SLIDES}.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing prompt files.")
    args = parser.parse_args()

    if args.write_template:
        _write_template(Path(args.write_template))
        return 0

    if not args.spec or not args.out_dir:
        _die("Use --spec and --out-dir, or --write-template.")

    spec_path = Path(args.spec)
    spec = _read_json(spec_path)
    spec_dir = spec_path.resolve().parent
    slides = spec.get("slides")
    if not isinstance(slides, list) or not slides:
        _die("Deck spec must include a non-empty slides array.")

    numbered_slides: List[tuple[int, Dict[str, Any], int]] = []
    seen_slide_numbers: Dict[int, int] = {}
    for fallback, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            _die(f"Slide entry {fallback} must be an object.")
        number = _slide_number(slide, fallback)
        if number in seen_slide_numbers:
            _die(
                f"Duplicate slide number {number}: slide entries "
                f"{seen_slide_numbers[number]} and {fallback} would both write slide_{number:02d}.json."
            )
        seen_slide_numbers[number] = fallback
        numbered_slides.append((fallback, slide, number))

    source_fidelity_contracts = _validate_source_structure(spec, numbered_slides)

    out_dir = Path(args.out_dir)
    prompts_dir = out_dir / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "origin_image").mkdir(parents=True, exist_ok=True)

    global_style_reference = spec.get("approved_style_reference")
    if global_style_reference is not None and not isinstance(global_style_reference, dict):
        _die("approved_style_reference must be an object when present.")
    if global_style_reference and isinstance(global_style_reference.get("path"), str):
        global_style_reference = dict(global_style_reference)
        global_style_reference["path"] = _resolve_image_path(global_style_reference["path"], base_dir=spec_dir)

    sample_generation_method = _sample_generation_method(spec, base_dir=spec_dir)
    max_concurrent_slides = args.max_concurrent_slides
    if max_concurrent_slides is None:
        max_concurrent_slides = int(spec.get("max_concurrent_slides", DEFAULT_MAX_CONCURRENT_SLIDES))
    if max_concurrent_slides < 1:
        _die("max_concurrent_slides must be >= 1.")
    selected_backend = (
        args.selected_backend
        or spec.get("selected_image_backend")
        or spec.get("image_backend")
        or _method_backend_label(sample_generation_method)
    )
    slide_job_entries: List[Dict[str, Any]] = []

    for fallback, slide, number in numbered_slides:
        use_style_reference = bool(slide.get("use_approved_style_reference", True))
        slide_style_reference = global_style_reference if use_style_reference else None
        prompt = _build_prompt(
            deck=spec,
            slide=slide,
            number=number,
            global_style_reference=slide_style_reference,
            source_fidelity_contract=source_fidelity_contracts.get(number),
            base_dir=spec_dir,
        )
        images = _job_images(slide, number=number, global_style_reference=slide_style_reference, base_dir=spec_dir)
        job = {
            "slide": number,
            "title": slide.get("title", f"Slide {number}"),
            "prompt": prompt,
            "out": f"slide_{number:02d}.png",
            "input_images": images,
            "requires_context_images": bool(images),
            "expected_backend": selected_backend,
            "sample_generation_method": sample_generation_method,
            "font_policy": dict(GLOBAL_TYPOGRAPHY_POLICY),
            "source_fidelity_contract": source_fidelity_contracts.get(number),
            "generation_contract": {
                "must_use_selected_image_backend": True,
                "must_match_sample_generation_method": bool(sample_generation_method),
                "must_use_microsoft_yahei_only_for_generated_text": True,
                "must_preserve_source_structure_cardinality": bool(
                    source_fidelity_contracts.get(number)
                ),
                "must_preserve_source_core_meaning_and_required_terms": bool(
                    source_fidelity_contracts.get(number)
                ),
                "must_use_concise_presentation_wording": bool(
                    source_fidelity_contracts.get(number)
                ),
                "must_avoid_duplicate_sequence_markers": bool(
                    source_fidelity_contracts.get(number)
                ),
                "forbidden_final_image_methods": [
                    "local drawing/rendering scripts",
                    "Pillow-generated slides",
                    "SVG/HTML/CSS/canvas screenshots",
                    "python-pptx/PptxGenJS/native PPT layout screenshots",
                    "manually composited text/image overlays",
                ],
                "must_return": ["backend_used", "selected_source", "qa_note"],
            },
        }
        prompt_path = prompts_dir / f"slide_{number:02d}.json"
        if prompt_path.exists() and not args.force:
            _die(f"Slide job file already exists: {prompt_path} (use --force)")
        prompt_path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        slide_id = f"slide_{number:02d}"
        final_image = out_dir / "origin_image" / f"{slide_id}.png"
        sample_approved = bool(slide.get("sample_approved") or slide.get("approved_sample"))
        status = "accepted" if sample_approved and final_image.exists() else "pending"
        slide_job_entries.append(
            {
                "slide_id": slide_id,
                "number": number,
                "title": slide.get("title", f"Slide {number}"),
                "job": rel_to_deck(out_dir, prompt_path),
                "out": rel_to_deck(out_dir, final_image),
                "input_images": images,
                "requires_context_images": bool(images),
                "status": status,
                "dispatch": None,
                "result": {
                    "final_image": rel_to_deck(out_dir, final_image),
                    "accepted_sample": True,
                }
                if status == "accepted"
                else None,
                "blocker": None,
            }
        )

    slide_jobs = {
        "run_status": "jobs_prepared",
        "deck_name": spec.get("deck_name"),
        "selected_backend": selected_backend,
        "sample_generation_method": sample_generation_method,
        "font_policy": dict(GLOBAL_TYPOGRAPHY_POLICY),
        "max_concurrent_slides": max_concurrent_slides,
        "slides": slide_job_entries,
        "updated_at": now_iso(),
    }
    save_jobs(out_dir, slide_jobs)
    set_run_status(out_dir, "jobs_prepared", "prepared slide prompt jobs")

    print(f"Wrote {len(slides)} slide job file(s) to {prompts_dir}")
    print(f"Wrote slide job state to {out_dir / 'slide_jobs.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
