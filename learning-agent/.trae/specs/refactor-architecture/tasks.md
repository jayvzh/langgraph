# Tasks

- [ ] Task 1: 重构 State 定义
  - [ ] SubTask 1.1: 将 LearningState 从字符串字段改为结构化字段（domain, subdomain, type, topic, summary, source dict, structured dict, evaluation dict, matched_file, similarity, path, filename, content, log）
  - [ ] SubTask 1.2: 移除旧字段（source_evaluation, domain_classification, topic_extraction, knowledge_matching, knowledge_structuring, value_evaluation, note_content, merge_or_create, log_content）

- [ ] Task 2: 实现 initial_analysis_node 合并节点
  - [ ] SubTask 2.1: 创建 initial_analysis_node 函数，合并来源评估+领域分类+主题提取为单次 LLM 调用
  - [ ] SubTask 2.2: Prompt 要求输出 JSON 结构（domain, subdomain, type, topic, source dict, summary）
  - [ ] SubTask 2.3: 使用强模型（OPENAI_MODEL），summary 压缩至≤20%
  - [ ] SubTask 2.4: 解析 LLM JSON 输出并写入 State 对应字段

- [ ] Task 3: 重构 content_filtering_node
  - [ ] SubTask 3.1: 输入改为 summary（不再使用 raw_text）
  - [ ] SubTask 3.2: 使用快速模型（OPENAI_FAST_MODEL）
  - [ ] SubTask 3.3: 输出 filtered_content 字符串

- [ ] Task 4: 重构 knowledge_structuring_node
  - [ ] SubTask 4.1: 输入改为 filtered_content
  - [ ] SubTask 4.2: 使用快速模型
  - [ ] SubTask 4.3: 输出 JSON 结构（market, model, process, data, strategy），写入 State.structured

- [ ] Task 5: 重构 value_evaluation_node
  - [ ] SubTask 5.1: 输入改为 structured + source
  - [ ] SubTask 5.2: 使用快速模型
  - [ ] SubTask 5.3: 输出 JSON 结构（value_level, roi, long_term, reason, insight, action），写入 State.evaluation

- [ ] Task 6: 重构 knowledge_matching_node
  - [ ] SubTask 6.1: 输入改为 topic + domain 路径
  - [ ] SubTask 6.2: 扫描 output/obsidian 下的多级目录结构
  - [ ] SubTask 6.3: 计算与已有文件的相似度（基于文件名和目录路径匹配）
  - [ ] SubTask 6.4: 输出 matched_file 和 similarity 写入 State

- [ ] Task 7: 重构 note_generation_node
  - [ ] SubTask 7.1: 输入改为所有结构化数据（domain, subdomain, type, topic, source, structured, evaluation）
  - [ ] SubTask 7.2: 使用快速模型
  - [ ] SubTask 7.3: 生成完整 Markdown 笔记内容（含统一格式和三类标签）
  - [ ] SubTask 7.4: 按 `domain/subdomain/type/topic.md` 规则生成 path 和 filename
  - [ ] SubTask 7.5: 自动创建多级目录

- [ ] Task 8: 重构 merge_or_create_node
  - [ ] SubTask 8.1: 根据 matched_file 和 similarity 判断是 merge 还是 create
  - [ ] SubTask 8.2: merge 模式：追加 `## 🔄 认知迭代记录` 段落，不覆盖原内容
  - [ ] SubTask 8.3: create 模式：创建新文件到多级目录
  - [ ] SubTask 8.4: fallback 机制：写入失败时生成 `{topic}__v2.md`

- [ ] Task 9: 重构 log_generation_node
  - [ ] SubTask 9.1: 按统一格式生成日志（时间、来源文件、领域、主题、匹配情况、价值判断、是否写入、原因、风险）

- [ ] Task 10: 重构 graph.py 工作流
  - [ ] SubTask 10.1: 更新节点导入（移除旧3节点，新增 initial_analysis_node）
  - [ ] SubTask 10.2: 更新工作流边：START → initial_analysis → content_filtering → knowledge_structuring → value_evaluation → knowledge_matching → note_generation → merge_or_create → log_generation → END
  - [ ] SubTask 10.3: 更新 initial_state 初始化

- [ ] Task 11: 添加双模型支持（可选，默认关闭）
  - [ ] SubTask 11.1: 创建 get_fast_llm() 函数，使用 OPENAI_FAST_MODEL 环境变量（默认 gpt-4o-mini）
  - [ ] SubTask 11.2: 创建 get_llm_for_node(is_initial=False) 函数，根据 DUAL_MODEL_ENABLED 环境变量决定使用哪个模型
  - [ ] SubTask 11.3: DUAL_MODEL_ENABLED 默认为 false，此时所有节点统一使用 OPENAI_MODEL
  - [ ] SubTask 11.4: DUAL_MODEL_ENABLED 为 true 时，initial_analysis_node 使用 OPENAI_MODEL，其余节点使用 OPENAI_FAST_MODEL
  - [ ] SubTask 11.5: 更新 .env.example 添加 DUAL_MODEL_ENABLED 和 OPENAI_FAST_MODEL 配置项

- [ ] Task 12: 测试验证
  - [ ] SubTask 12.1: 使用 TikTok 课程文档测试完整工作流
  - [ ] SubTask 12.2: 验证多级目录结构正确生成
  - [ ] SubTask 12.3: 验证笔记格式完整（含三类标签）
  - [ ] SubTask 12.4: 验证日志格式正确

- [ ] Task 13: 更新 CHANGELOG.md

# Task Dependencies
- [Task 2] depends on [Task 1]
- [Task 3] depends on [Task 1]
- [Task 4] depends on [Task 1]
- [Task 5] depends on [Task 1]
- [Task 6] depends on [Task 1]
- [Task 7] depends on [Task 1]
- [Task 8] depends on [Task 6, Task 7]
- [Task 9] depends on [Task 1]
- [Task 10] depends on [Task 2-9]
- [Task 11] depends on [Task 1]
- [Task 12] depends on [Task 10, Task 11]
- [Task 13] depends on [Task 12]
