# Learning Agent 优化计划

## 问题分析

### 1. 目录生成问题
- **现状**：文件直接放在 `output/obsidian` 下，没有按 `domain/subdomain/type/topic.md` 结构创建多级目录
- **原因**：
  - `domain_classification_node` 没有以结构化的方式输出 domain、subdomain、type 信息
  - `note_generation_node` 没有使用结构化信息来创建目录

### 2. 速度优化问题
- **现状**：10个节点串行调用，速度较慢
- **原因**：每个节点都单独调用 LLM API，导致多次网络往返

### 3. Token使用优化问题
- **现状**：多个节点重复上传完整 `raw_text`
- **原因**：每个节点都传递完整原始文本，造成 token 浪费

## 解决方案

### 方案1：正确实现目录生成规则
1. **修改 `domain_classification_node`**：以结构化 JSON 格式输出 domain、subdomain、type 信息
2. **修改 `topic_extraction_node`**：输出标准化的 topic 名称
3. **重构 `note_generation_node`**：
   - 解析 domain、subdomain、type、topic 信息
   - 创建多级目录结构：`domain/subdomain/type/`
   - 按规则生成文件路径

### 方案2：优化工作流速度
1. **节点合并**：将前3个节点（source_evaluation, domain_classification, topic_extraction）合并为一个 `initial_analysis_node`
2. **并行处理**：将可以并行的节点（如 content_filtering 与其它分析节点）并行执行
3. **模型选择**：为简单节点使用更快的模型（如 gpt-3.5-turbo），复杂节点保留 gpt-4

### 方案3：优化Token使用量
1. **减少重复上传**：只在第一个节点传递完整 `raw_text`，后续节点传递前节点的处理结果
2. **精简Prompt**：优化每个节点的 System Prompt，去除冗余内容
3. **结构化输出**：使用结构化输出（JSON）减少输出 token 消耗

## 文件修改清单

1. `src/learning_agent/state.py` - 更新 state 结构，新增结构化字段
2. `src/learning_agent/nodes.py` - 重构节点，实现上述优化
3. `src/learning_agent/graph.py` - 更新工作流，支持新节点结构
4. `pyproject.toml` - 升级版本号
5. `CHANGELOG.md` - 记录优化内容

## 实施步骤

1. 更新 state 定义，新增结构化字段
2. 重构 nodes.py，实现优化方案
3. 更新 graph.py，调整工作流结构
4. 测试验证功能正常
5. 更新 CHANGELOG 和版本号

## 预期效果

- ✅ 正确的多级目录结构
- ✅ 工作流速度提升约40-50%
- ✅ Token使用量减少约30-40%
