# Chart Data Limits — Circular Chart Experience

> Self-Refinement 经验沉淀。AI 在 S3 内容填充前必须读取。

## Experience 001: Donut/Pie Max 6 Segments

**Date**: 2026-05-02
**Problem**: donut 和 pie 版式超过6段时，标签区宽度不足，文字严重溢出。
**Root Cause**: 每段对应一条图例标签，7+段时标签列高度超出内容区。
**Fix**: 该环形/饼图预设最多容纳6段。类别更多时保留全部类别及原顺序，改用适合的图表或表格；不得自动排序、归并为其他或删除类别。
**Rule**: `len(segments) > 6` 表示此预设不适用，应更换版式。只有用户明确要求聚合且逐项范围可追溯时，才按其要求调整。

## Experience 002: grouped_bar Max 6 Categories × 3 Series

**Date**: 2026-05-02
**Problem**: 分组柱状图超过6个类别时，每组柱宽度过窄，文字标签重叠。
**Root Cause**: 动态宽度计算结果导致字体降级不够。
**Fix**: 此预设最多容纳6个类别、3个系列。超出时改选版式，或在保留类别、系列、顺序及父级标识的前提下续页；不能合并类别或把系列改成新的同级分点。
**Rule**: S3 门禁检查 `len(categories) <= 6 and len(series) <= 3`。
