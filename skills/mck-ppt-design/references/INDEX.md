# Knowledge Index — PPT Skill Reference Router

> AI 在每个阶段应该读哪些文件。按需加载，不要全量读取。

## Stage → Load Map

| 阶段 | 必须读 | 可选读（按需） |
|------|--------|--------------|
| S1 需求定义 | `team/brand-guide.md`（了解约束）| — |
| S2 结构设计 | `framework/engine-api.md`, `references/layout-matrix.yaml` | 涉及具体版式时读 `layout-catalog.md`，参数查 `framework/engine-api.md` |
| S3 内容填充 | `framework/guard-rails.md`, `experiences/*.md`（若存在）| `framework/planning-guide.md`（复杂结构时）|
| S4 渲染 | `layout-catalog.md` 与 `framework/engine-api.md` 中实际用到的版式| `team/presentation-convention.md`（确认边距）|
| S5 交付 | — | — |

## File Directory

```
references/
├── INDEX.md                      # 本文件，知识路由表
├── layout-matrix.yaml            # 版式×能力边界×字符预算（真相源）
│
├── team/                         # 团队级（最稳定，所有项目继承）
│   ├── brand-guide.md            # 配色、字体、设计原则
│   └── presentation-convention.md # 边距、必须元素、文件交付
│
├── framework/                    # 框架级（中频更新）
│   ├── engine-api.md             # 67方法 API 速查表
│   ├── guard-rails.md            # 10条生产护栏（防崩溃规则）
│   └── planning-guide.md        # 版式选择、内容密度、结构规划
│
├── color-palette.md              # 已有，颜色色板参考
├── layout-catalog.md             # 已有，版式目录索引
│
└── scripts/                      # 门禁脚本（机读化执行，不可用 AI 自评替代）
    ├── gate_check.py             # S4 门禁：QA 分类，输出 gate_result.json
    └── gate_check_s3.py          # S3 门禁：API格式+数量+source检查，输出 gate_s3.json
```

## experiences/ Directory

```
experiences/                      # Self-Refinement 经验沉淀（AI 自动维护）
├── overflow.md                   # 文字溢出类经验
├── chart-limits.md               # 图表数据段数限制经验
├── layout-pitfalls.md            # 版式特定踩坑
└── cjk-issues.md                 # 中文渲染问题
```

## Quick Load Cheatsheet

**只需要做一个封面** → 读 `team/brand-guide.md` 即可

**做完整 10+ 页汇报** → S2 读 `engine-api.md` + `layout-matrix.yaml`；S3 读 `guard-rails.md`；S4 查 `layout-catalog.md` 和 `framework/engine-api.md` 中实际用到的版式

**有图表** → S4 查 `framework/engine-api.md` 中对应图表方法，并核对引擎真实签名

**之前做过同类汇报有报错** → S3 先读 `experiences/*.md`
