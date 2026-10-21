# Overflow Experiences — Text Overflow Patterns

> Self-Refinement 经验沉淀。AI 在 S3 内容填充前必须读取。

## Experience 001: Action Title Too Long

**Date**: 2026-05-02
**Problem**: Action Title 超过 40 个字符时，22pt 字体导致标题溢出到内容区。
**Root Cause**: 标题栏高度固定 0.9"，超长文字换行后高度超出。
**Fix**: 保留标题的完整意思，先增加标题容器高度、调整内容区起点或改选适配版式。仅当文意自然且层级不变时使用主副标题，不得为40字符删除限定或改写原文结构。
**Rule**: 40字符是该固定标题栏的容量提示；以实际渲染无溢出和文意完整为通过依据。

## Experience 002: Four-Column Desc Too Long

**Date**: 2026-05-02
**Problem**: `four_column` 每栏描述超过 120 字时底部溢出。
**Root Cause**: 4栏均分后每栏宽度约 2.7"，正文14pt 120字超出高度限制。
**Fix**: 先核对原文是否确有四个同级分点，再决定是否使用四栏。完整说明超过预设容量时，改用更宽的容器或保持原层级续页，不把一句话拆成新增同级要点。
**Rule**: 120字符只提示该预设栏宽可能不足；逐项结构一致、文字完整且渲染清楚才算通过。

## Experience 003: process_chevron 5+ Steps

**Date**: 2026-05-02
**Problem**: `process_chevron` 超过 5 个步骤时，箭头间距变为负值导致文件损坏。
**Root Cause**: Rule 10 保护了外框，但箭头连接器间距公式未同步收窄。
**Fix**: 保留原文步骤数与顺序。该接口的预设容量为5步、描述50字符；超出时使用其他布局或保持步骤编号和父级的续页，不合并步骤或删去说明关系。
**Rule**: 容量检查失败时更换布局；不得把容量上限转成原文项数或内容上限。

## Experience 004: process_chevron Step Label 不能含 \n

**Date**: 2026-05-02
**Problem**: `process_chevron` 步骤标签（第一个元素）中使用 `\n` 换行，导致 Oval 高度溢出 21%。
**Root Cause**: Oval 圆形标签固定高度 0.45"，多行文字撑爆容器。
**Fix**: 该固定圆形容器不支持多行标签。完整标签需要换行时，改用可容纳它的文本容器或其他版式；不得删去阶段名称或时间信息来强行单行显示。
**Rule**: S3 门禁检查 `'\n' not in step_label`。

## Experience 005: four_column items 需要三元组 (num, title, desc)

**Date**: 2026-05-02
**Problem**: 传入二元组 `(title, desc)` 导致 `ValueError: not enough values to unpack`。
**Root Cause**: engine 期望 `(num, col_title, desc)` 三元组，num 用于圆形编号显示。
**Fix**: 始终传三元组，第一个元素是编号/标识符（如 "RS1", "1", "A"）。
**Rule**: S3 门禁确认 `four_column` items 每个元素有 3 个字段。

## Experience 006: timeline 最后一个 milestone 标签容易溢出右边界

**Date**: 2026-05-02
**Problem**: timeline 5个里程碑时，最后一个标签位置接近右边界，标签超出 0.47"。
**Root Cause**: timeline engine 均分布局后，最后节点的标签文字向右对齐导致超出内容区。
**Fix**: 保留里程碑完整名称，调整末端标签的对齐、宽度或位置；必要时改用其他时间轴布局。
**Rule**: 6字符是旧版末端标签的容量提示，不是写作上限。实际标签应无溢出，并完整保留原文含义。
