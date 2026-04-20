# Learning Agent

基于 LangGraph 的个人学习智能体——"商业认知过滤系统"，帮助你从文档资料中筛选对赚钱有价值的信息，自动结构化归档到 Obsidian 知识库。

## 功能

- **来源评估**：判断来源可信度、偏差风险
- **领域分类**：自动识别内容所属领域和子领域
- **信息过滤**：去除宣传内容、机构介绍等无价值信息
- **知识结构化**：按市场认知/商业模式/操作路径/关键数据/可执行策略整理
- **价值判断**：根据用户画像评估知识的价值等级和ROI潜力
- **Obsidian笔记**：自动生成多级目录归档的Markdown笔记
- **防覆盖机制**：相似内容自动追加认知迭代记录
- **运行日志**：记录每次处理的详细过程

## 安装

### 1. 创建Conda环境

```powershell
conda create -n learning-agent python=3.12 -y
conda activate learning-agent
```

### 2. 安装依赖

```powershell
cd e:\Code\github\langgraph\learning-agent
pip install -e .
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env`，然后填入你的API密钥：

```powershell
copy .env.example .env
# 然后编辑 .env 文件，填入你的 OPENAI_API_KEY
```

## 使用

运行智能体处理你的docx文件：

```powershell
python main.py path/to/your/document.docx
```

## 项目结构

```
learning-agent/
├── src/
│   └── learning_agent/
│       ├── __init__.py
│       ├── state.py          # 状态定义
│       ├── nodes.py          # 节点实现
│       └── graph.py          # 图构建与运行
├── output/
│   ├── obsidian/             # 生成的Obsidian笔记（多级目录）
│   └── logs/                 # 运行日志
├── docs/                     # 待处理的文档
├── main.py                   # 主程序入口
├── pyproject.toml            # 项目配置
└── .env.example              # 环境变量模板
```

## 工作流程（8节点）

```
① initial_analysis（初始分析：来源评估+领域分类+主题提取+摘要压缩）
    ↓
② content_filtering（内容过滤）
    ↓
③ knowledge_structuring（知识结构化）
    ↓
④ value_evaluation（价值评估）
    ↓
⑤ knowledge_matching（知识匹配：检测已有笔记）
    ↓
⑥ note_generation（笔记生成）
    ↓
⑦ merge_or_create（合并或新建）
    ↓
⑧ log_generation（日志生成）
```

## 笔记目录结构

笔记按 `领域/子领域/细分类/类型/主题.md` 多级目录归档：

```
output/obsidian/
├── 跨境电商/
│   ├── TikTok/
│   │   ├── 美区运营/
│   │   │   └── 方法论/
│   │   │       └── TikTok美区增长框架.md
│   │   └── 选品/
│   │       └── 策略/
│   │           └── 数据驱动选品方法论.md
│   └── 亚马逊/
│       └── 运营/
│           └── 教程/
│               └── 亚马逊FBA全流程操作指南.md
├── AI工具/
│   └── Agent/
│       └── 架构设计/
│           └── 系统/
│               └── 学习型Agent架构设计.md
└── 自动化/
    └── 工作流/
        └── 数据管道/
            └── 工具/
                └── n8n自动化工作流搭建.md
```

### 目录层级说明

| 层级  | 字段           | 说明          | 示例                      |
| --- | ------------ | ----------- | ----------------------- |
| 第1级 | domain       | 大领域         | 跨境电商、AI工具、自动化、流量增长、商业模式 |
| 第2级 | subdomain    | 子领域（2-6字短词） | TikTok、亚马逊、Agent、选品     |
| 第3级 | subsubdomain | 细分类（2-8字）   | 美区运营、数据驱动、架构设计          |
| 第4级 | type         | 知识类型        | 方法论、教程、工具、行业认知          |
| 文件名 | topic        | 具体主题（6-15字） | TikTok美区增长框架.md         |

## 配置说明

### 环境变量

在 `.env` 文件中配置以下变量：

#### 基础配置（必需）

| 变量                | 说明           | 默认值                         |
| ----------------- | ------------ | --------------------------- |
| `OPENAI_API_KEY`  | OpenAI API密钥 | （必需）                        |
| `OPENAI_MODEL`    | 主模型（强模型）     | `gpt-4`                     |
| `OPENAI_API_BASE` | API基础URL     | `https://api.openai.com/v1` |

#### 双模型配置（可选）

| 变量                     | 说明              | 默认值                  |
| ---------------------- | --------------- | -------------------- |
| `DUAL_MODEL_ENABLED`   | 是否启用双模型策略       | `false`              |
| `OPENAI_FAST_MODEL`    | 快速模型            | `gpt-4o-mini`        |
| `OPENAI_FAST_API_BASE` | 快速模型 API 基础 URL | 使用 `OPENAI_API_BASE` |
| `OPENAI_FAST_API_KEY`  | 快速模型 API 密钥     | 使用 `OPENAI_API_KEY`  |

### 模型分配策略

| 节点                     | 类型  | 默认模型             | 双模型启用时                 |
| ---------------------- | --- | ---------------- | ---------------------- |
| initial\_analysis      | LLM | OPENAI\_MODEL（强） | OPENAI\_MODEL（强）       |
| content\_filtering     | LLM | OPENAI\_MODEL    | OPENAI\_FAST\_MODEL（快） |
| knowledge\_structuring | LLM | OPENAI\_MODEL    | OPENAI\_FAST\_MODEL（快） |
| value\_evaluation      | LLM | OPENAI\_MODEL    | OPENAI\_FAST\_MODEL（快） |
| note\_generation       | LLM | OPENAI\_MODEL    | OPENAI\_FAST\_MODEL（快） |
| knowledge\_matching    | 纯代码 | -                | -                      |
| merge\_or\_create      | 纯代码 | -                | -                      |
| log\_generation        | 纯代码 | -                | -                      |

### 模型推荐

#### 强模型（用于 initial\_analysis，需理解全文+多维度判断）

| 模型              | 提供商      | 特点             |
| --------------- | -------- | -------------- |
| `gpt-5.4`       | OpenAI   | 当前最强，理解力和推理力顶尖 |
| `deepseek-chat` | DeepSeek | 国产性价比高，中文好     |
| `qwen-plus`     | 阿里云      | 国产便宜，中文场景优秀    |

#### 快速模型（用于过滤/结构化/评估/笔记生成等简单任务）

| 模型               | 提供商       | 特点                |
| ---------------- | --------- | ----------------- |
| `deepseek-r1:8b` | Ollama 本地 | 推理能力强，中文优秀，免费（推荐） |
| `qwen3:8b`       | Ollama 本地 | 新一代架构，中英文均衡，免费    |
| `gemma3:4b`      | Ollama 本地 | Google出品，轻量快速，免费  |

#### 本地 Ollama 模型选择建议

**deepseek-r1:8b 能否胜任？**

可以胜任当前业务流程。该模型在中文理解、文本摘要、信息提取等任务上表现优秀，完全能满足内容过滤、知识结构化、价值评估和笔记生成等节点需求。

**是否需要更换其他模型？**

- **保持 deepseek-r1:8b**：如果你的文档以中文为主，且注重推理和提取能力，当前模型已足够
- **考虑 qwen3:8b**：如果需要更好的中英文双语能力，或遇到 deepseek-r1 输出格式不稳定的情况
- **考虑 gemma3:4b**：如果显存有限（<8GB），需要更快的推理速度

**其他模型简评**：

- `gpt-oss`：OpenAI 开源模型，但 20B 版本需要 ≥16GB 显存，资源消耗大
- `qwen3-vl`：视觉多模态模型，当前业务不需要图像理解，无需使用
- `minimax-m2`：国产商业模型，API 调用成本较高，不如本地模型经济

> **注意**：Ollama 本地模型仅建议用于快速模型节点。initial\_analysis 节点需要强理解力，建议使用云端强模型。

