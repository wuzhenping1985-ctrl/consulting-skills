---
name: ciic-style-ppt
description: Create, edit, restyle, and visually verify PowerPoint presentations in the CIIC/Zhongzhi blue consulting style. Use when the user asks for CIIC style, 中智蓝色咨询模板风, 中智咨询风格, a blue Chinese management-consulting deck, or wants an existing PPT/PPTX converted to that visual system. Supports editable slide decks and full-slide image decks while keeping source content grounded and Chinese text readable.
---

# CIIC Style PPT

## 管理咨询与国企汇报模式

用于管理咨询或国企汇报时，先读[认可样本设计方法](/Users/shampwu/.codex/skills/ppt-layout-library/references/approved-consulting-design.md)和[设计参数](/Users/shampwu/.codex/skills/ppt-layout-library/references/consulting-tokens.json)，按来源关系选择整页结构与组件，在制作记录中注明借鉴文件、页码和适配方式。

- 默认16:9、Microsoft YaHei、原生可编辑、无阴影；当前任务明确指定的模板、复刻或其他样式要求优先。
- 标题表达有依据的核心观点，同时保留来源要求的分类名称与归属。新写同层条目通常不超过6项；已有来源的项数、顺序、父子关系及完整表达优先。
- 先核对来源，再渲染全部页面；按设计方法逐页验收，并检查原生对象、字体、配色和无阴影。已知偏好直接沿用，内部样页由制作方检验。

## 艺术构图与原文措辞（长期要求）

新建、改版、规划及审稿时，必须执行[PPT艺术构图与展示要求](/Users/shampwu/.codex/skills/ppt-art-direction.md)。默认采用更具艺术感的非表格整页构图，优先沿用原文完整句子，以有意义的曲线、几何、局部色面和留白组织阅读。用户明确指定模板、原样复刻或表格保留范围时按其要求处理。

该共享要求优先于本技能及其 agents、references、docs、提示模板中的表格首选、均匀卡片、固定密度、占用率、留白比例、图形份额及默认文字压缩建议。原文项数、顺序、归属与完整解释保持；技术密度诊断仅作审图提示，不能据此填充装饰或删改原文。

## 一、必读规则

每次制作或修改前，必须完整阅读 [PPT文字与原文结构要求](/Users/shampwu/.codex/skills/ppt-content-rules.md)、[中智视觉规范](references/ciic-blue-style.md) 和 [共享版式库说明](/Users/shampwu/.codex/skills/ppt-layout-library/README.md)。用户的明确要求优先，版式不得改变内容。

- 原文每一层级的同层项数、顺序、父子关系和关键名词原样保留；两点不能拆成三点或合成一点，支撑说明继续放在原父级之下。
- 正文使用完整、自然的表达，保留对象、动作、关系与适用条件，不为版面删词或堆砌名词。完整说明优先放在无边框正文区，图形与文字保持清楚的对应关系。
- 先逐项核对原文结构，再由独立审稿者只看实际渲染页面检查句意和阅读顺序。任一审查未通过，修正后重审，不得交付。

## 二、制作流程

1. 阅读来源与已有页面，记录各层级及其对应位置。已有结论、数据和专业口径须有来源支持。
2. 按共享版式库 README 的方法检索 `catalog.json`，以原文关系选择候选条目，并实际查看对应的 `previews/` 图像后确定构图。借鉴比例、线条、几何组合和空间安排，保留原文分点。未查看预览时不得声称已采用该参考；无适合条目时按原文关系自行构图。
3. 综合阅读共享库中的[五份资料设计方法](/Users/shampwu/.codex/skills/ppt-layout-library/references/consulting-page-design.md)：用A/B/C选择构图和基本图形关系，用D/E安排整页结构与完整正文，沿`related_refs`查看关联原页。需要参考原生绘制时查看库中`reconstructions/`的样页和代码。在大纲中记录页面目的、原文映射、所用参考条目及借鉴内容。相同关系可以复用版式，不规定图形种类或每套参考的使用次数。
4. 默认制作16:9、简体中文、可编辑PPT。使用原生文字、几何形状和图表；精确查数、薪酬编制规则及真实二维分类可按内容采用原生表格，观点与关系页不默认排成行列表格。用户指定表格范围或整页图片时按要求制作。仅确认会实际影响交付的缺失信息。
5. 排版时让图形说明原文关系，完整正文保留在清楚可读的位置。放不下时调整容器和布局，必要时保留原层级续页。
6. 渲染全部页面，先完成结构和文字审查，再检查视觉、编辑性及文件是否可正常打开。

## 三、视觉与资产

保持中智蓝色系和微软雅黑视觉风格。允许原生圆弧、斜线、圆环、扇区、多边形、功能图标、局部色面及有作用的留白；具体使用见视觉规范。图形应有清楚作用，不得凭空增加层级、流程、闭环、权重或比例含义，也不按固定轮换顺序追求多样化。

优先查看共享版式库的参考页面。本技能内的 [配色参考图](assets/contact-sheet.png) 用于核对品牌；[原模板](assets/ciic-consulting-2024-template-16x9.pptx) 用于用户明确要求保留原母版或复现原模板的任务。仅借鉴版式时，按当前内容重建适合的结构，不带入原模板的占位文案、标志或页脚。

## 四、交付检查

- 原文各层级、项数、顺序、名词及图形关系逐项对应；正文独立可读，事实和数据可追溯。
- 图形含义与来源一致，完整说明可读，留白和色面有明确作用；不以形状数量、页面占用率或图形种类判断质量。
- 修正溢出、遮挡、错字、乱码及误导性的连线、比例或大小；核对品牌色、对齐和目标阅读尺寸。相同版式的重复须与内容关系相符。
- PPTX可以正常打开，原生编辑要求得到满足，所有最终页面均经过实际渲染检查。
