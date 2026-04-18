# Changelog

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
