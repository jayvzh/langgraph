# Learning Agent 架构重构 Spec

## Why
当前 learning-agent 存在三个核心问题：1) 文件平铺存放，未按 `domain/subdomain/type/topic.md` 创建多级目录；2) 10个节点串行调用 LLM，速度慢且重复上传 raw_text 浪费 token；3) 节点输出为自由文本而非结构化 JSON，难以在后续节点中精确引用。

## What Changes
- **BREAKING**: 重构 State 结构，从字符串字段改为结构化字段（domain, subdomain, type, topic, source dict, structured dict, evaluation dict 等）
- **BREAKING**: 合并前3个节点（source_evaluation, domain_classification, topic_extraction）为 `initial_analysis_node`
- **BREAKING**: 实现多级目录归档 `domain/subdomain/type/topic.md`，禁止平铺文件
- **BREAKING**: raw_text 仅在 initial_analysis_node 使用，后续节点全部使用 summary / structured data
- **BREAKING**: 所有节点输出必须为 JSON 结构
- 实现 merge_or_create_node 的正确合并逻辑（追加认知迭代记录，不覆盖）
- 双模型策略：initial_analysis_node 用强模型，其余节点用快速模型
- 统一标签系统（领域标签 + 能力标签 + 属性标签）

## Impact
- Affected code: `state.py`, `nodes.py`, `graph.py`, `__init__.py`
- Affected behavior: 输出目录结构从平铺变为多级目录；工作流从10节点变为8节点

## ADDED Requirements

### Requirement: initial_analysis_node 合并节点
系统 SHALL 提供 `initial_analysis_node`，将来源评估、领域分类、主题提取合并为单次 LLM 调用。

#### Scenario: 正常分析
- **WHEN** 输入 raw_text 和 source_file
- **THEN** 输出 JSON 结构包含 domain, subdomain, type, topic, source(dict), summary(压缩至≤20%)

#### Scenario: raw_text 隔离
- **WHEN** initial_analysis_node 执行完毕
- **THEN** 后续所有节点禁止访问 raw_text，仅使用 summary 和结构化数据

### Requirement: 多级目录归档
系统 SHALL 按 `domain/subdomain/type/topic.md` 结构创建多级目录存放笔记。

#### Scenario: 新建笔记归档
- **WHEN** 生成新笔记
- **THEN** 文件路径为 `output/obsidian/{domain}/{subdomain}/{type}/{topic}.md`

#### Scenario: 跨境电商内容
- **WHEN** domain="跨境电商", subdomain="TikTok", type="方法论", topic="增长框架"
- **THEN** 文件路径为 `output/obsidian/跨境电商/TikTok/方法论/增长框架.md`

### Requirement: 防覆盖合并机制
系统 SHALL 在检测到已有匹配文件时追加内容，不覆盖原文件。

#### Scenario: 匹配到已有文件
- **WHEN** knowledge_matching_node 发现 similarity > 0.7 的已有文件
- **THEN** merge_or_create_node 追加 `## 🔄 认知迭代记录` 段落

#### Scenario: 写入失败
- **WHEN** 文件写入失败
- **THEN** 生成 `{topic}__v2.md` 作为临时文件

### Requirement: 双模型策略（可选，默认关闭）
系统 SHALL 支持双模型策略，通过环境变量 `DUAL_MODEL_ENABLED` 控制开关，默认不启用。

#### Scenario: 双模型关闭（默认）
- **WHEN** 环境变量 `DUAL_MODEL_ENABLED` 未设置或为 `false`
- **THEN** 所有节点统一使用 `OPENAI_MODEL` 模型

#### Scenario: 双模型启用
- **WHEN** 环境变量 `DUAL_MODEL_ENABLED` 设为 `true`
- **THEN** initial_analysis_node 使用强模型（`OPENAI_MODEL`），其余7个节点使用快速模型（`OPENAI_FAST_MODEL`，默认 `gpt-4o-mini`）

#### Scenario: 模型配置
- **WHEN** 用户需要自定义模型
- **THEN** 通过 `.env` 文件配置 `OPENAI_MODEL`（强模型）、`OPENAI_FAST_MODEL`（快速模型）、`DUAL_MODEL_ENABLED`（开关）

### Requirement: 结构化 JSON 输出
系统 SHALL 要求所有节点输出 JSON 格式数据。

#### Scenario: knowledge_structuring_node 输出
- **WHEN** 执行知识结构化
- **THEN** 输出 JSON 包含 market, model, process, data, strategy 五个字段

#### Scenario: value_evaluation_node 输出
- **WHEN** 执行价值评估
- **THEN** 输出 JSON 包含 value_level, roi, long_term, reason, insight, action

### Requirement: 统一标签系统
系统 SHALL 在笔记中生成三类标签。

#### Scenario: 标签生成
- **WHEN** 生成笔记
- **THEN** 包含领域标签（如 #跨境电商）、能力标签（如 #选品）、属性标签（如 #高ROI #红海）

## MODIFIED Requirements

### Requirement: State 结构
State 从字符串字段改为结构化字段：

```python
class LearningState(TypedDict):
    raw_text: str
    source_file: str
    domain: str
    subdomain: str
    type: str
    topic: str
    summary: str
    source: Dict
    filtered_content: str
    structured: Dict
    evaluation: Dict
    matched_file: str
    similarity: float
    path: str
    filename: str
    content: str
    log: str
    note_path: Optional[str]
    log_path: Optional[str]
```

### Requirement: 工作流顺序
工作流从10节点改为8节点：
1. initial_analysis_node → 2. content_filtering_node → 3. knowledge_structuring_node → 4. value_evaluation_node → 5. knowledge_matching_node → 6. note_generation_node → 7. merge_or_create_node → 8. log_generation_node

## REMOVED Requirements

### Requirement: source_evaluation_node 独立节点
**Reason**: 已合并到 initial_analysis_node
**Migration**: source 评估结果通过 initial_analysis_node 的 JSON 输出获取

### Requirement: domain_classification_node 独立节点
**Reason**: 已合并到 initial_analysis_node
**Migration**: domain/subdomain/type 通过 initial_analysis_node 的 JSON 输出获取

### Requirement: topic_extraction_node 独立节点
**Reason**: 已合并到 initial_analysis_node
**Migration**: topic 通过 initial_analysis_node 的 JSON 输出获取
