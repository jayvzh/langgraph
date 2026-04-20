# Learning Agent Upgrade - The Implementation Plan (Decomposed and Prioritized Task List)

## [ ] Task 1: 重构 State 定义
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 扩展 LearningState TypedDict，新增所有工作流节点所需字段
  - 新增字段包括：source_evaluation, domain_classification, topic, knowledge_match, structured_knowledge, value_evaluation, merged 等
- **Acceptance Criteria Addressed**: [AC-1, AC-2, AC-3, AC-4, AC-7, AC-8, AC-9]
- **Test Requirements**:
  - `programmatic` TR-1.1: State 包含所有新字段定义
  - `programmatic` TR-1.2: 所有字段类型标注正确
- **Notes**: 参考需求文档中每个节点的输入输出定义

## [ ] Task 2: 实现 Source Evaluation 节点
- **Priority**: P0
- **Depends On**: Task 1
- **Description**: 
  - 创建 source_evaluation_node 函数
  - 输入：docx 文件名 + 内容
  - 输出：source_name, source_type, credibility, bias_risk, need_verification
  - 实现规则：课程/卖课 bias 高，AI 摘要可信度下降，实操/数据可信度高
- **Acceptance Criteria Addressed**: [AC-1]
- **Test Requirements**:
  - `programmatic` TR-2.1: 节点正确输出所有 5 个字段
  - `human-judgement` TR-2.2: 来源类型和可信度评估合理

## [ ] Task 3: 实现 Domain Classification 节点
- **Priority**: P0
- **Depends On**: Task 2
- **Description**: 
  - 创建 domain_classification_node 函数
  - 输出：domain（多选）和 type
  - domain 枚举：跨境电商, AI工具, 自动化, 流量增长, 商业模式
  - type 枚举：方法论, 教程, 工具, 行业认知
- **Acceptance Criteria Addressed**: [AC-2]
- **Test Requirements**:
  - `programmatic` TR-3.1: domain 从指定枚举中选择
  - `programmatic` TR-3.2: type 正确识别

## [ ] Task 4: 实现 Topic Extraction 节点
- **Priority**: P0
- **Depends On**: Task 3
- **Description**: 
  - 创建 topic_extraction_node 函数
  - 输出标准化主题名
  - 去品牌词（如 TikTok 课程 → TikTok 增长）
  - 确保可复用性
- **Acceptance Criteria Addressed**: [AC-3]
- **Test Requirements**:
  - `human-judgement` TR-4.1: 主题名标准化且可复用
  - `programmatic` TR-4.2: 正确去除品牌词

## [ ] Task 5: 实现 Knowledge Matching 节点
- **Priority**: P0
- **Depends On**: Task 4
- **Description**: 
  - 创建 knowledge_matching_node 函数
  - 扫描 output/obsidian 目录
  - 查找是否已有相同 topic 文件
  - 计算相似度，> 0.7 视为匹配
- **Acceptance Criteria Addressed**: [AC-4]
- **Test Requirements**:
  - `programmatic` TR-5.1: 正确返回 matched_file_path 或 None
  - `programmatic` TR-5.2: 正确计算 similarity_score

## [ ] Task 6: 重构 Content Filtering 节点
- **Priority**: P0
- **Depends On**: Task 1
- **Description**: 
  - 更新现有 filter_node
  - 删除：宣传内容、机构介绍、无执行价值信息、重复内容
  - 保留：策略、数据、方法、流程
- **Acceptance Criteria Addressed**: [AC-5]
- **Test Requirements**:
  - `human-judgement` TR-6.1: 过滤后内容仅保留高价值信息

## [ ] Task 7: 实现 Knowledge Structuring 节点
- **Priority**: P0
- **Depends On**: Task 6
- **Description**: 
  - 创建 knowledge_structuring_node 函数
  - 结构化为：市场认知、商业模式、操作路径、关键数据、可执行策略
- **Acceptance Criteria Addressed**: [AC-7]
- **Test Requirements**:
  - `programmatic` TR-7.1: 包含所有 5 个结构部分

## [ ] Task 8: 重构 Value Evaluation 节点
- **Priority**: P0
- **Depends On**: Task 7
- **Description**: 
  - 更新现有 evaluate_node
  - 输出：价值等级、ROI 潜力、是否长期方向
  - 判断标准：提升收入、可规模化、可自动化、有复利、红海判断
- **Acceptance Criteria Addressed**: [AC-7]
- **Test Requirements**:
  - `programmatic` TR-8.1: 输出所有 3 个字段
  - `human-judgement` TR-8.2: 价值判断符合规则

## [ ] Task 9: 实现目录生成逻辑
- **Priority**: P0
- **Depends On**: Task 3, Task 4
- **Description**: 
  - 实现路径生成：domain / 子领域 / type / topic.md
  - 子领域映射规则（如 TikTok → 跨境电商子领域）
  - 自动创建目录
- **Acceptance Criteria Addressed**: [AC-5]
- **Test Requirements**:
  - `programmatic` TR-9.1: 路径格式正确
  - `programmatic` TR-9.2: 目录自动创建成功

## [ ] Task 10: 重构 Note Generation 节点
- **Priority**: P0
- **Depends On**: Task 2-9
- **Description**: 
  - 完全重写 note_node
  - 按需求文档格式生成笔记
  - 包含所有必需 Markdown 结构
  - 统一标签系统（领域、能力、属性
- **Acceptance Criteria Addressed**: [AC-7, AC-8]
- **Test Requirements**:
  - `programmatic` TR-10.1: 笔记格式包含所有必需部分
  - `programmatic` TR-10.2: 标签系统完整

## [ ] Task 11: 实现 Merge or Create 节点
- **Priority**: P0
- **Depends On**: Task 5, Task 10
- **Description**: 
  - 创建 merge_or_create_node 函数
  - 如果匹配文件存在 → 更新模式，追加认知迭代记录
  - 否则新建文件
  - 兜底机制：写入失败生成 topic__v2.md
- **Acceptance Criteria Addressed**: [AC-6]
- **Test Requirements**:
  - `programmatic` TR-11.1: 更新时正确追加
  - `programmatic` TR-11.2: 新建文件正确创建
  - `programmatic` TR-11.3: 兜底机制有效

## [ ] Task 12: 重构 Log Generation 节点
- **Priority**: P0
- **Depends On**: Task 1-11
- **Description**: 
  - 更新现有 log_node
  - 按需求文档格式生成日志
  - 包含所有必需字段
- **Acceptance Criteria Addressed**: [AC-9]
- **Test Requirements**:
  - `programmatic` TR-12.1: 日志格式完整

## [ ] Task 13: 重构 Graph 工作流
- **Priority**: P0
- **Depends On**: Task 1-12
- **Description**: 
  - 更新 create_graph 函数
  - 按顺序连接所有 10 个节点
  - 正确设置边和条件
- **Acceptance Criteria Addressed**: [AC-10]
- **Test Requirements**:
  - `programmatic` TR-13.1: 工作流完整可编译
  - `programmatic` TR-13.2: 节点顺序正确

## [ ] Task 14: 测试：TikTok 课程
- **Priority**: P1
- **Depends On**: Task 13
- **Description**: 
  - 使用 docs 目录下的 TikTok 课程文档测试
  - 验证分类、归档、重复避免、价值判断
- **Acceptance Criteria Addressed**: [AC-1, AC-2, AC-5, AC-6, AC-7, AC-10]
- **Test Requirements**:
  - `programmatic` TR-14.1: 分类正确
  - `programmatic` TR-14.2: 归档目录正确
  - `programmatic` TR-14.3: 价值判断存在

## [ ] Task 15: 添加依赖更新 CHANGELOG
- **Priority**: P1
- **Depends On**: Task 14
- **Description**: 
  - 更新 CHANGELOG.md 记录本次主要修改
- **Acceptance Criteria Addressed**: []
- **Test Requirements**:
  - `programmatic` TR-15.1: CHANGELOG 更新正确
