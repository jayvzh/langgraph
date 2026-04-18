# Verification Checklist

## State 结构验证
- [x] LearningState 包含 domain, subdomain, type, topic, summary 字段
- [x] LearningState 包含 source(Dict), structured(Dict), evaluation(Dict) 字段
- [x] LearningState 包含 matched_file, similarity, path, filename, content, log 字段
- [x] 旧字段（source_evaluation, domain_classification, topic_extraction, knowledge_matching, knowledge_structuring, value_evaluation, note_content, merge_or_create, log_content）已移除

## initial_analysis_node 验证
- [x] 单次 LLM 调用输出 JSON 包含 domain, subdomain, type, topic, source, summary
- [x] 使用强模型（OPENAI_MODEL）
- [x] summary 压缩至原始内容的≤20%
- [x] source 包含 source_name, source_type, credibility, bias_risk, need_verification

## Token 优化验证
- [x] raw_text 仅在 initial_analysis_node 中使用
- [x] content_filtering_node 输入为 summary（非 raw_text）
- [x] knowledge_structuring_node 输入为 filtered_content（非 raw_text）
- [x] value_evaluation_node 输入为 structured + source（非 raw_text）
- [x] knowledge_matching_node 输入为 topic + domain（非 raw_text）
- [x] note_generation_node 输入为结构化数据（非 raw_text）

## 双模型策略验证
- [x] get_fast_llm() 函数存在，使用 OPENAI_FAST_MODEL（默认 gpt-4o-mini）
- [x] get_llm(strong) 函数存在，根据 DUAL_MODEL_ENABLED 决定返回哪个模型
- [x] DUAL_MODEL_ENABLED 默认为 false，此时所有节点统一使用 OPENAI_MODEL
- [x] DUAL_MODEL_ENABLED 为 true 时，initial_analysis_node 使用 OPENAI_MODEL，其余节点使用 OPENAI_FAST_MODEL
- [x] .env.example 包含 DUAL_MODEL_ENABLED 和 OPENAI_FAST_MODEL 配置项

## 多级目录验证
- [x] 笔记文件路径格式为 output/obsidian/{domain}/{subdomain}/{type}/{topic}.md
- [x] 自动创建多级目录
- [x] 不存在平铺文件（output/obsidian/*.md）

## 防覆盖机制验证
- [x] matched_file 存在且 similarity > 0.7 时进入 merge 模式
- [x] merge 模式追加 `## 🔄 认知迭代记录` 段落
- [x] merge 模式不覆盖原文件内容
- [x] 写入失败时生成 `{topic}__v2.md` 临时文件

## 笔记格式验证
- [x] 包含 🧠 核心结论
- [x] 包含 📊 价值评级（value_level, roi, long_term）
- [x] 包含 📌 关键知识
- [x] 包含 ⚙️ 可执行策略
- [x] 包含 💡 启发
- [x] 包含 🔗 关联知识
- [x] 包含 📚 信息来源（source_name, source_file, source_type）
- [x] 包含 🔍 可信度评估（credibility, bias_risk, need_verification）
- [x] 包含 🧪 验证状态
- [x] 包含 🏷 标签（领域标签 + 能力标签 + 属性标签）

## 日志格式验证
- [x] 包含时间、来源文件、领域、主题
- [x] 包含匹配情况、价值判断
- [x] 包含是否写入、原因、风险

## 工作流验证
- [x] 工作流为8节点顺序执行
- [x] 节点顺序：initial_analysis → content_filtering → knowledge_structuring → value_evaluation → knowledge_matching → note_generation → merge_or_create → log_generation
- [x] 使用 TikTok 课程文档可完整运行
