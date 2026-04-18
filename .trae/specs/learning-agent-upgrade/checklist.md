# Learning Agent Upgrade - Verification Checklist

## 核心功能验证
- [ ] State 定义完整，包含所有工作流节点所需字段
- [ ] Source Evaluation 节点正确输出 source_name, source_type, credibility, bias_risk, need_verification
- [ ] Domain Classification 节点正确识别领域和类型
- [ ] Topic Extraction 节点输出标准化、可复用的主题名
- [ ] Knowledge Matching 节点正确匹配已有知识并计算相似度
- [ ] Content Filtering 节点正确删除低价值内容，保留高价值信息
- [ ] Knowledge Structuring 节点按要求结构化知识
- [ ] Value Evaluation 节点正确输出价值等级、ROI 潜力、是否长期方向
- [ ] Note Generation 节点按统一格式生成笔记，包含所有必需部分
- [ ] Merge or Create 节点正确处理更新和新建
- [ ] Log Generation 节点按统一格式生成日志
- [ ] 完整工作流可正常执行

## 目录和归档验证
- [ ] 目录结构正确：domain/subdomain/type/topic.md
- [ ] 自动创建所需目录
- [ ] 笔记文件路径正确
- [ ] 更新模式正确追加内容，不覆盖原文件
- [ ] 兜底机制有效（topic__v2.md）

## 标签和格式验证
- [ ] 笔记包含领域标签
- [ ] 笔记包含能力标签
- [ ] 笔记包含属性标签
- [ ] 笔记格式完整（核心结论、价值评级、关键知识等）
- [ ] 日志格式完整

## 测试用例验证
- [ ] TikTok 课程测试：分类正确、归档正确、避免重复、价值判断正确
