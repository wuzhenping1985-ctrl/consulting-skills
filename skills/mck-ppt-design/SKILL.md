---
name: mck-ppt-design
description: Create editable management-consulting PowerPoint presentations with MckEngine, Microsoft YaHei throughout, and the user's strict CIIC blue palette. Use for strategy decks, business reviews, consulting proposals, and executive reports requiring native PPTX output and automated layout and brand checks.

---

# McKinsey PPT Design — Harness Framework

## 管理咨询与国企汇报模式

用于管理咨询或国企汇报时，先读[认可样本设计方法](/Users/shampwu/.codex/skills/ppt-layout-library/references/approved-consulting-design.md)和[设计参数](/Users/shampwu/.codex/skills/ppt-layout-library/references/consulting-tokens.json)，按来源关系选择整页结构与组件，在制作记录中注明借鉴文件、页码和适配方式。

- 默认16:9、Microsoft YaHei、原生可编辑、无阴影；当前任务明确指定的模板、复刻或其他样式要求优先。
- 标题表达有依据的核心观点，同时保留来源要求的分类名称与归属。新写同层条目通常不超过6项；已有来源的项数、顺序、父子关系及完整表达优先。
- 先核对来源，再渲染全部页面；按设计方法逐页验收，并检查原生对象、字体、配色和无阴影。已知偏好直接沿用，内部样页由制作方检验。

## 艺术构图与原文措辞（长期要求）

新建、改版、规划及审稿时，必须执行[PPT艺术构图与展示要求](/Users/shampwu/.codex/skills/ppt-art-direction.md)。默认采用更具艺术感的非表格整页构图，优先沿用原文完整句子，以有意义的曲线、几何、局部色面和留白组织阅读。用户明确指定模板、原样复刻或表格保留范围时按其要求处理。

该共享要求优先于本技能及其 agents、references、docs、提示模板中的表格首选、均匀卡片、固定密度、占用率、留白比例、图形份额及默认文字压缩建议。原文项数、顺序、归属与完整解释保持；技术密度诊断仅作审图提示，不能据此填充装饰或删改原文。

## 文字与原文结构（强制）

每次制作、改写或审稿前，必须完整阅读并执行 [PPT文字与原文结构要求](/Users/shampwu/.codex/skills/ppt-content-rules.md)。本节及共享规则优先于本技能中关于字数、短标签、内容密度和模板项数的建议。

1. 原文每一层级的同层项数、顺序和父子关系必须原样保留。原文两点就保留两点，不能拆成三点、合成一点，也不能把下级说明提升为同级分支。模板必须适应原文结构。
2. 正文须表达完整、清楚，让读者只看页面就能理解对象、动作、关系和适用条件。不得为版面删去因果、比较、限定或责任关系，不以名词堆砌、缩略标签和斜杠串联替代说明；放不下时先调整版式和容器，必要时在保留原层级的前提下续页。
3. 先按原文逐项核对各层级、项数、顺序及父子关系，再由独立审稿者只看实际渲染页面检查文字是否自然、意思是否完整。记录两轮审查结果；任一未通过，修正后重审，不得交付。

## 字体与配色硬性要求

- 全部中文、英文、数字、页码、脚注、图表、表格、备注和主题字体统一使用微软雅黑（`Microsoft YaHei`），不允许自动换成微软雅黑 UI 或其他字体。
- 每次制作先读 `references/team/brand-guide.md`。颜色数值的唯一依据为 `references/team/ciic-palette.json`，原图保存在 `references/team/ciic-color-reference.png`。图上明确标注的 RGB 优先于色块像素。
- 标题和主强调使用主蓝色；图表系列按 `CHART_COLORS` 排序。默认采用蓝色与灰色搭配，或规定的多级蓝色搭配；橙色仅用于少量重点/警示。状态必须配合文字或符号说明。
- 原有深海军蓝、绿色、红色、Georgia/Arial/KaiTi 等规则失效；示例、历史记录和旧变量名称不能覆盖本节。旧版式 API 保留，实际样式以品牌常量为准。
- 浅蓝、浅灰底使用深灰字；主蓝底使用白字。正文对比度至少 4.5:1，大字（18pt 以上或 14pt 以上加粗）至少 3:1，这是对附图搭配禁忌的本机量化执行标准。相近蓝色作为相邻图表系列时用白色间隔、直接标签或图例区分。
- 使用 `eng.save()` 写出最终文件，保存时统一主题和字体，并检查色值。使用其他生成路径或后处理后必须再运行 `gate_check.py`。品牌检查失败必须修复，不能归入引擎问题豁免。
- 品牌检查覆盖原生文本、形状、表格、主题和图表颜色；照片、外部图片、复杂交叠、透明或渐变底仍须逐页目视。不得把正文栅格化来规避字体检查。严格配色材料不使用自动生成的装饰封面图。

## 模型与逻辑图设计

- 管理咨询报告先识别每页需要表达的关系，再选版式：条件判断用分支及明确的与/或关系，测算用公式分解及汇总关系，管理流程用动作、责任与先后关系，框架用有含义的层级、分组和输入输出。
- 观点与管控框架优先采用开放构图和原生关系图；精确查数、薪酬编制规则、真实二维分类及用户指定的原表可采用原生表格。共同列与固定横行即使由文本框模拟，仍属于表格形式，须按其查数或分类用途判断。按内容选择载体，已获任务授权时不另加表格审批。
- 多个文本框加装饰性连线仍可能缺少模型含义。每条箭头必须能解释方向、条件或传递内容；中心节点必须承担明确作用。并列关系不能画成相加，独立事项不能画成因果，逐人折算不能简化为总量乘单一系数。
- 逐页目视检查后再判断设计是否完成，机器检查通过只说明对应技术项目通过。重复的四格框架、空泛中心标签和过长说明应回到关系设计修正。
- 相关经验：[模型图示与文字框的区别](experiences/semantic-models.md)。

## 本机 Codex 运行配置

- 技能根目录：`/Users/shampwu/.codex/skills/mck-ppt-design`。引用文档中的旧 WorkBuddy 路径均以此目录为准。
- 生成脚本及 QA 脚本统一使用 `/Users/shampwu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`，该环境已有 python-pptx 和 lxml。文中的 `python` 命令均替换为此完整路径。
- 本节为安装时添加的本机兼容配置；保留原有五阶段流程及 QA 判定规则。


> **Version**: 2.3.3-harness-v2 · **Engine**: MckEngine (python-pptx) · **Author**: [likaku](https://github.com/likaku/Mck-ppt-design-skill)
>
> **Required tools**: Read, Write, Bash · **Requires**: `pip install python-pptx lxml`

---

## 常见崩坏模式（每次生成前必读，先于 HARD RULES）

> 告诉 AI 要做什么效果一般，告诉它前人最容易在哪里塌效果更好。
> 以下三种反模式均已在真实执行中被验证，每次必须主动警惕。

### 反模式 1：口头宣布"门禁通过"（最常见）

**错误做法**：
> 「S4 QA 共 7 个 errors，判断均为 engine 设计行为，门禁通过，进入 S5」

**问题所在**：`passed` 是由 AI 口头判断的，不是由程序派生的。无论理由多充分，这句话都是 AI 在给自己写完成证书。

**正确做法**：
1. 执行 `python references/scripts/gate_check.py <pptx路径> <项目目录>`
2. 读取 `<项目目录>/gate_result.json`
3. 只有 `gate_result.json` 中 `"passed": true` 时，才能进入 S5
4. 如果 `"passed": false`，修复 `user_code_errors` 列表中的问题，重新渲染，再次执行 gate_check

---

### 反模式 2：S3 门禁"脑子里过一遍"就算通过

**错误做法**：
> 「S3 内容门禁预检：API 格式正确，字数在限制内，通过，进入 S4」（没有执行任何代码）

**问题所在**：今天真实发生的 3 个 API 格式错误（`four_column`/`matrix_2x2`/`executive_summary` 参数格式），靠脑子过是过不出来的，必须靠代码检查。

**正确做法**：
1. 执行 `python references/scripts/gate_check_s3.py <content.json路径> <项目目录>`
2. 读取 `<项目目录>/gate_s3.json`
3. 只有 `"passed": true` 时，才能进入 S4
4. 如果有 `fail` 项，修正 `content.json`，重新执行 gate_check_s3

---

### 反模式 3：engine_bug 分类作为软话逃生口

**错误做法**：
> 「peer_font_inconsistency 是 engine 内部设计行为，不是用户代码问题，可以放行」

**问题所在**：这个分类本身是正确的，但由 AI 在对话里口头做出，等于把豁免权交给了 AI 自己——而 AI 有动机让自己通过。

**正确做法**：
`gate_check.py` 里有硬编码的 `ENGINE_BUG_WHITELIST` 枚举。只有在白名单里的 error category，才会被豁免。白名单是代码，不是 AI 的判断。如果你认为某类 error 应该加入白名单，修改 `gate_check.py` 里的枚举，而不是口头声明豁免。

---

## HARD RULES（必须遵守，不可绕过）

1. **每次生成必须走五阶段流程**，不允许"一句话直接生成"跳过前置阶段
2. **阶段进度记录**：在当前任务内记录五阶段进度；有计划工具时使用计划工具，否则在项目文件中记录。不要为阶段进度创建独立的 Codex 任务。
3. **按需加载上下文**：每个阶段只读对应文件，不要全量加载旧版 SKILL.md 里的内容
4. **门禁必须机读化**：S3 和 S4 门禁必须执行对应的 gate_check 脚本，读 JSON 结果，不得口头判断
5. **Self-Refinement 必做**：每次修正 pattern-level 问题后，写入 `experiences/` 对应文件
6. **引擎路径固定**：`sys.path.insert(0, os.path.expanduser('~/.codex/skills/mck-ppt-design'))`

---

## 知识路由（上下文加载索引）

> **在每个阶段开始时，读对应文件**。不要一次性全读。

| 阶段 | 必须读 | 说明 |
|------|--------|------|
| S1 需求 | `references/team/brand-guide.md` | 了解设计约束 |
| S2 结构 | `references/framework/engine-api.md` + `references/layout-matrix.yaml` | 版式选择和能力边界 |
| S3 内容 | `references/framework/guard-rails.md` + `experiences/*.md`（存在时）| 防溢出规则 + 历史踩坑 |
| S4 渲染 | `references/layout-catalog.md` + `references/framework/engine-api.md` 中实际用到的版式 | 版式选择与实现参数 |
| S5 交付 | 无 | — |

**完整路由表**：`references/INDEX.md`

---

## 五阶段生成流程

```
┌─────────┐   ┌─────────────┐   ┌─────────────┐   ┌──────────────┐   ┌──────────┐
│ S1 需求  │──▶│ S2 结构 ⭐   │──▶│ S3 内容 ⭐   │──▶│ S4 渲染+QA ⭐⭐│──▶│ S5 交付   │
│ brief.md│   │ outline.json│   │content.json │   │  .pptx       │   │ + 沉淀   │
└─────────┘   └─────────────┘   └─────────────┘   └──────────────┘   └──────────┘
                    ⭐ = 门禁（FAIL 则在本阶段修正，不得跳过）
    S3/S4 门禁必须运行 gate_check 脚本，读 JSON 结果 — 不得口头宣布通过
```

### Stage 1: 需求定义

**读文件**：`references/team/brand-guide.md`

**收集信息**：
- 受众（职位/决策角色）
- 目标（决策/汇报/说服）
- 时长（分钟数 → 约 1 分钟/页）
- 关键信息（按原文各层级逐项记录，不以固定条数归并或删减）
- 数据来源（有哪些数据可用）

**产出**：在工作目录创建 `ppt-project-{slug}/brief.md`

**门禁**：`audience` + `goal` + `key_messages` 三项非空（AI 自评即可）

---

### Stage 2: 结构设计

**读文件**：`references/framework/engine-api.md`, `references/layout-matrix.yaml`

**任务**：
1. 根据时长确定页数（1分钟/页）
2. 为每张幻灯片选定 `layout`（查 engine-api.md 速查表）
3. 每页写清 `key_point`，表达完整意思；原文各层级另建逐项映射，不能用一句概括替代原有分点
4. 确认版式在能力边界内（查 layout-matrix.yaml）

**产出**：`ppt-project-{slug}/outline.json`

```json
{
  "brief": {"audience": "董事会", "goal": "战略汇报", "duration_minutes": 15},
  "slides": [
    {"idx": 1, "layout": "cover", "title": "Q1 2026 战略回顾", "key_point": ""},
    {"idx": 2, "layout": "toc", "title": "目录", "key_point": ""},
    {"idx": 3, "layout": "table_insight", "title": "市场格局三大转变驱动战略重构", "key_point": ""}
  ]
}
```

**⭐ 门禁 S2**（AI 自评）：
- [ ] `cover` 幻灯片存在
- [ ] 幻灯片数量在时长约束内（`count <= duration_minutes * 1.2`）
- [ ] 所有 layout 在 `layout-matrix.yaml` 中有定义
- [ ] 标题清楚表达页面主题或有依据的判断，不用字数判断是否完整，不为凑字数扩写原文标题
- [ ] 原文每层同级项数、顺序及父子关系均与页面映射一致
- [ ] `two_column_text` 数量 ≤ 1

---

### Stage 3: 内容填充

**读文件**：`references/framework/guard-rails.md`, `experiences/*.md`（全部存在的文件）

**任务**：
1. 为每张幻灯片填充具体文案、数字、图表数据
2. 确保每页有 `source` 出处
3. 先写完整、自然的文案，再用 `layout-matrix.yaml` 的 `char_budget` 检查所选版式容量；超出时调整容器、改选版式或保持层级续页，不能为通过门禁删掉关系与限定

**产出**：`ppt-project-{slug}/content.json`

**⭐ 门禁 S3**（必须机读化，不得 AI 自评）：

```bash
python ~/.codex/skills/mck-ppt-design/references/scripts/gate_check_s3.py \
    <项目目录>/content.json  <项目目录>
```

读取 `<项目目录>/gate_s3.json`：
- `"passed": true` → 进入 S4
- `"passed": false` → 修正 `content.json` 中 `fail_items` 列出的问题，重新执行

---

### Stage 4: 渲染 + QA

**读文件**：`references/layout-catalog.md` 和 `references/framework/engine-api.md` 中实际用到的版式；参数以引擎真实签名为准

**任务**：
1. 根据 `content.json` 生成 Python 渲染脚本
2. 执行脚本生成 `.pptx`
3. 运行 QA 门禁脚本，确认字体、配色与对比度检查同时通过
4. 对照原文逐项完成结构核对，再交独立审稿者只看渲染页面检查文字是否完整、自然、易懂；技术门禁不能替代这两轮审查

**⭐⭐ 门禁 S4**（必须机读化，不得口头宣布通过）：

```bash
python ~/.codex/skills/mck-ppt-design/references/scripts/gate_check.py \
    <pptx路径>  <项目目录>
```

读取 `<项目目录>/gate_result.json`：
- `"passed": true` → 进入 S5
- `"passed": false` → 查看 `user_code_errors`，修复渲染代码，重新渲染，再次执行

**注意**：`engine_bug` 类 errors（`peer_font_inconsistency` 等白名单条目）由脚本自动豁免，不需要 AI 口头判断。

**产出**：`<项目目录>/gate_result.json` + `.pptx`

---

### Stage 5: 交付 + Self-Refinement

**任务**：
1. 读取 `gate_result.json` 确认 `passed: true`，并确认逐项结构核对、独立读图审稿均通过（任何一项缺失或失败，均不得交付）
2. 交付 `.pptx` 文件
3. **Self-Refinement**：判断本次是否有 pattern-level 修正

**⭐ Self-Refinement 协议**：

```
修正后判断：
  ONE-TIME（单次特定调整）→ 不需要沉淀
  PATTERN（跨 deck 可重现的问题）→ 必须写入 experiences/
    - 溢出类 → experiences/overflow.md
    - 图表限制 → experiences/chart-limits.md
    - 版式踩坑 → experiences/layout-pitfalls.md
    - 中文渲染 → experiences/cjk-issues.md

格式：
  ## Experience NNN: {title}
  **Date**: YYYY-MM-DD
  **Problem**: ...
  **Root Cause**: ...
  **Fix**: ...
  **Rule**: ...（门禁层面如何预防）
```

---

## Fast Track（简单需求跳过 S2/S3 门禁）

满足**全部**条件时，AI 可跳过 S2 结构评审和 S3 内容审查：
- 总页数 ≤ 5
- 无数据图表（donut/bar/table 类）
- 用户明确表达"快速"/"马上要"/"简单"

**仍然必须**：S1 需求收集 + 原文逐项结构核对 + S4 QA 门禁（gate_check.py 脚本执行）+ 独立读图审稿 + S5 交付；快速模式不能省略结构和文字审查

---

## Checkpoint / 断点恢复

当用户说"继续做那个 PPT"时：

```python
import os, json, glob

projects = glob.glob('ppt-project-*/')
for proj in projects:
    brief   = os.path.exists(f'{proj}brief.md')
    outline = os.path.exists(f'{proj}outline.json')
    content = os.path.exists(f'{proj}content.json')
    gate_s3 = os.path.exists(f'{proj}gate_s3.json')
    gate_s4 = os.path.exists(f'{proj}gate_result.json')
    pptx    = bool(glob.glob(f'{proj}*.pptx'))

    if not brief:           stage = 1
    elif not outline:       stage = 2
    elif not content:       stage = 3
    elif not gate_s3:       stage = '3-gate'   # content 有了但 gate 还没跑
    elif not pptx:          stage = 4
    elif not gate_s4:       stage = '4-gate'   # pptx 有了但 gate 还没跑
    else:                   stage = 5

    print(f"项目 {proj}: 当前处于 Stage {stage}")
```

---

## MckEngine 快速模板

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.codex/skills/mck-ppt-design'))
from mck_ppt import MckEngine
from mck_ppt.constants import *

eng = MckEngine(total_slides=12)
eng.cover(title='标题', subtitle='副标题', author='作者', date='2026年')
eng.toc(items=[('1', '章节一', '一句话描述'), ('2', '章节二', '一句话描述')])
# ... 内容页 ...
eng.closing(title='谢谢', message='期待进一步交流')
eng.save('output/deck.pptx')  # 自动 full_cleanup
```

**详细 API**：`references/framework/engine-api.md`
**版式规范**：`references/layout-catalog.md`、`references/framework/engine-api.md`
**10条护栏**：`references/framework/guard-rails.md`
**版式能力边界**：`references/layout-matrix.yaml`
**历史踩坑**：`experiences/`
**S3 门禁脚本**：`references/scripts/gate_check_s3.py`
**S4 门禁脚本**：`references/scripts/gate_check.py`
