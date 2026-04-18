# Changelog

## [0.3.0] - 2026-04-19

### Added

- 双模型支持：`get_llm(strong=True)` 使用强模型，`get_llm()` 使用快速模型
- `DUAL_MODEL_ENABLED` 和 `OPENAI_FAST_MODEL` 环境变量配置
- `parse_json_output()` 辅助函数，自动处理 LLM 返回的 markdown 代码块包裹
- `initial_analysis_node` 合并节点（原 source_evaluation + domain_classification + topic_extraction），使用强模型，输出结构化 JSON
- `knowledge_matching_node` 纯代码实现，基于 SequenceMatcher 计算文件名/路径相似度
- `merge_or_create_node` 纯代码实现，支持 merge 模式（追加认知迭代记录）和 create 模式，含 fallback 机制
- `log_generation_node` 纯代码实现，统一日志格式
- 多级目录结构：按 `domain/subdomain/type/topic.md` 自动创建

### Changed

- **state.py**：从字符串字段重构为结构化字段（domain, subdomain, type, topic, source, structured, evaluation 等 Dict 字段）
- **nodes.py**：从 10 个节点精简为 8 个节点
  - 合并 source_evaluation + domain_classification + topic_extraction → initial_analysis
  - content_filtering 改为使用 summary 输入（不再使用 raw_text）
  - knowledge_structuring 输出结构化 JSON（market/model/process/data/strategy）
  - value_evaluation 输出结构化 JSON（value_level/roi/long_term/reason/insight/action）
  - knowledge_matching 改为纯代码逻辑（不再使用 LLM）
  - note_generation 使用结构化数据生成完整 Markdown 笔记
  - merge_or_create 改为纯代码逻辑（不再使用 LLM）
  - log_generation 改为纯代码逻辑（不再使用 LLM）
- **graph.py**：工作流从 10 节点线性链重构为 8 节点线性链
- **.env.example**：新增 DUAL_MODEL_ENABLED 和 OPENAI_FAST_MODEL 配置项
- raw_text 仅在 initial_analysis_node 中使用，后续节点禁止使用

### Removed

- 删除 source_evaluation_node、domain_classification_node、topic_extraction_node（合并为 initial_analysis_node）
- 删除旧的平铺文件命名方式（如 `跨境电商_TikTok美区机会与执行框架_方法论.md`）

### Tested

- 使用 docs 目录下的 TikTok 课程文档成功测试
- 验证多级目录结构正确生成（output/obsidian/跨境电商/TikTok美区兴趣电商入门与变现/教程/）
- 验证笔记格式完整（10 个模块全部包含）
- 验证日志格式正确
- 验证不存在平铺文件

## [0.2.0] - 2026-04-19

### Added

- 完整实现 10 个工作流节点：
  - Source Evaluation：来源可信度评估
  - Domain Classification：领域分类
  - Topic Extraction：主题提取
  - Knowledge Matching：知识与用户目标匹配度评估
  - Content Filtering：内容过滤（重构）
  - Knowledge Structuring：知识结构化
  - Value Evaluation：价值评估（重构）
  - Note Generation：笔记生成（完全重写）
  - Merge or Create：合并或创建笔记
  - Log Generation：日志生成（重构）

### Changed

- 重构 LearningState 状态定义，新增所有工作流节点所需字段
- 完全重写 nodes.py，实现所有新节点功能
- 更新 graph.py，连接所有 10 个节点形成完整工作流
- 增强 Note Generation 功能，新增来源信息、领域分类、主题提取等模块
- 优化 Log Generation，记录完整处理流程和所有节点输出

### Tested

- 使用 docs 目录下的 TikTok 课程文档成功测试
- 生成完整 Obsidian 笔记和运行日志

## [0.1.0] - 2026-04-19

### Added

- 初始化项目结构
- 实现基于LangGraph的学习智能体V1
- 5个核心节点：
  - filter_node：信息过滤，去除无价值内容
  - extract_node：知识抽取，整理为结构化知识
  - evaluate_node：价值判断，根据用户画像评估
  - note_node：生成Obsidian格式笔记
  - log_node：记录运行日志
- 支持docx文件输入
- 配置文件支持（.env）
- README文档和使用说明
