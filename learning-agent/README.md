# Learning Agent

基于 LangGraph 的个人学习智能体，帮助你从文档资料中提取有价值的知识。

## 功能

- **信息过滤**：去除宣传内容、机构介绍等无价值信息
- **知识抽取**：将内容分类整理为结构化知识
- **价值判断**：根据你的画像评估知识的价值
- **Obsidian笔记**：自动生成适合Obsidian的Markdown笔记
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

复制 `.env.example` 为 `.env`，然后填入你的OpenAI API密钥：

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
│   ├── obsidian/             # 生成的Obsidian笔记
│   └── logs/                 # 运行日志
├── tests/                    # 测试文件
├── main.py                   # 主程序入口
├── pyproject.toml            # 项目配置
└── .env.example              # 环境变量模板
```

## 工作流程

1. **输入**：你的docx文档
2. **过滤**：去除水分，保留有价值内容
3. **抽取**：整理为结构化知识
4. **评估**：根据你的画像判断价值
5. **笔记**：生成Obsidian格式笔记
6. **日志**：记录整个过程

## 配置说明

在 `.env` 文件中可以配置：

- `OPENAI_API_KEY`：你的OpenAI API密钥（必需）
- `OPENAI_MODEL`：使用的模型，默认是 `gpt-4`
- `OPENAI_API_BASE`：API基础URL，可用于代理
