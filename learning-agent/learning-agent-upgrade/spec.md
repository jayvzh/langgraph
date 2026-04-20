# Learning Agent Upgrade - Product Requirement Document

## Overview
- **Summary**: 将现有的 learning-agent 从简单的内容总结工具重构为完整的"商业认知过滤系统"，使用完整的 LangGraph 工作流处理文档，进行多维度价值判断、领域分类、知识匹配和结构化归档。
- **Purpose**: 帮助用户从大量资料中筛选对"赚钱（可规模化+可自动化+长期收益）"有价值的信息，自动结构化并归档到 Obsidian 知识库，避免信息过载和重复工作。
- **Target Users**: 专注于跨境电商、AI工具、自动化和商业方向的创业者和学习者。

## Goals
- 实现完整的 10 节点 LangGraph 工作流
- 新增来源评估、领域分类、主题提取、知识匹配等功能
- 实现价值判断而非简单总结
- 建立目录化归档机制，避免长文件名
- 实现防止覆盖和重复的机制
- 统一标签系统和日志格式

## Non-Goals (Out of Scope)
- 不支持除 docx 外的其他文件格式
- 不实现多人协作编辑功能
- 不实现实时同步 Obsidian Vault
- 不构建 Web 界面，保持 CLI 工具形态

## Background & Context
现有系统仅包含 5 个节点：filter → extract → evaluate → note → log，缺乏关键的来源评估、领域分类、知识匹配等功能。笔记以长文件名形式直接存放，无目录结构，无防止覆盖机制。

## Functional Requirements
- **FR-1**: 来源评估节点 - 评估来源可信度、偏差风险等
- **FR-2**: 领域分类节点 - 识别内容所属领域和类型
- **FR-3**: 主题提取节点 - 提取标准化主题名
- **FR-4**: 知识匹配节点 - 在 Obsidian 中匹配已有知识
- **FR-5**: 内容过滤节点 - 保留高价值信息，删除宣传等低价值内容
- **FR-6**: 知识结构化节点 - 按固定结构整理知识
- **FR-7**: 价值评估节点 - 判断价值等级、ROI潜力等
- **FR-8**: 笔记生成节点 - 按统一格式生成笔记
- **FR-9**: 合并或新建节点 - 判断是新建还是更新已有笔记
- **FR-10**: 日志生成节点 - 按统一格式生成日志
- **FR-11**: 目录化归档 - 按 domain/subdomain/type/topic.md 结构存放
- **FR-12**: 防止覆盖机制 - 更新时追加而非覆盖
- **FR-13**: 统一标签系统 - 包含领域、能力、属性三类标签

## Non-Functional Requirements
- **NFR-1**: 工作流执行时间应 < 2 分钟（假设 GPT-4 模型）
- **NFR-2**: 代码遵循 PEP8 规范
- **NFR-3**: 保持与现有 Python 3.12 兼容
- **NFR-4**: 所有文件读写操作包含错误处理

## Constraints
- **Technical**: 使用现有 tech stack（LangGraph, LangChain, OpenAI, Python 3.12+）
- **Business**: 无外部预算，无明确 timeline
- **Dependencies**: OpenAI API, python-docx 库

## Assumptions
- 用户已有配置好的 OpenAI API key
- Obsidian 知识库目录结构在 output/obsidian 下
- docx 文件包含有效文本内容

## Acceptance Criteria

### AC-1: 来源评估功能
- **Given**: 输入一个 docx 文件
- **When**: 系统处理该文件
- **Then**: 输出 source_name, source_type, credibility, bias_risk, need_verification
- **Verification**: `programmatic`

### AC-2: 领域分类功能
- **Given**: 输入文档内容
- **When**: 执行领域分类节点
- **Then**: 输出 domain（多选自指定枚举）和 type（方法论/教程/工具/行业认知）
- **Verification**: `programmatic`

### AC-3: 主题提取功能
- **Given**: 过滤后的文档内容
- **When**: 执行主题提取节点
- **Then**: 输出标准化主题名（去品牌词，可复用）
- **Verification**: `human-judgment`

### AC-4: 知识匹配功能
- **Given**: 提取的主题和现有 Obsidian 笔记
- **When**: 执行知识匹配节点
- **Then**: 输出 matched_file_path（或 None）和 similarity_score（>0.7 视为匹配）
- **Verification**: `programmatic`

### AC-5: 目录化归档
- **Given**: domain, subdomain, type, topic
- **When**: 生成笔记文件路径
- **Then**: 路径格式为 domain/subdomain/type/topic.md
- **Verification**: `programmatic`

### AC-6: 防止覆盖机制
- **Given**: 已存在匹配文件
- **When**: 执行更新模式
- **Then**: 追加认知迭代记录，不覆盖原内容
- **Verification**: `programmatic`

### AC-7: 笔记格式正确
- **Given**: 所有节点处理完成
- **When**: 生成最终笔记
- **Then**: 笔记包含所有必需的 Markdown 结构（核心结论、价值评级、关键知识等）
- **Verification**: `programmatic`

### AC-8: 标签系统完整
- **Given**: 生成的笔记
- **When**: 检查标签
- **Then**: 包含领域标签、能力标签、属性标签
- **Verification**: `programmatic`

### AC-9: 日志格式正确
- **Given**: 处理完成
- **When**: 生成日志
- **Then**: 日志包含时间、输入来源、识别领域、主题、是否命中、价值判断等
- **Verification**: `programmatic`

### AC-10: 完整工作流执行
- **Given**: 一个测试 docx 文件
- **When**: 运行完整工作流
- **Then**: 所有节点按顺序执行，生成笔记和日志
- **Verification**: `programmatic`

## Open Questions
- [ ] 是否需要支持更多文件格式（PDF, TXT, Markdown）？
- [ ] 是否需要支持自定义领域枚举？
- [ ] 是否需要支持配置子领域映射规则？
