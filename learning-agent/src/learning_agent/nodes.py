import os
from datetime import datetime
from pathlib import Path
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4"),
        temperature=0.7,
    )


def filter_node(state: Dict) -> Dict:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个极度理性的商业分析者。

目标：
从以下内容中删除：
- 宣传内容
- 机构介绍
- 无实际操作价值的信息
- 重复内容

只保留：
- 可执行策略
- 市场判断
- 数据信息
- 操作流程

输出要求：
- 用简洁要点表达
- 不要解释"""),
        ("human", "{input_text}")
    ])
    chain = prompt | llm
    result = chain.invoke({"input_text": state["raw_text"]})
    return {"filtered": str(result.content)}


def extract_node(state: Dict) -> Dict:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", """将以下内容整理为"知识结构"，必须分类：

输出结构：
1. 市场认知
2. 商业模式
3. 操作路径
4. 关键数据
5. 可复制策略

要求：
- 去掉废话
- 每点必须有价值"""),
        ("human", "{filtered_text}")
    ])
    chain = prompt | llm
    result = chain.invoke({"filtered_text": state["filtered"]})
    return {"knowledge": str(result.content)}


def evaluate_node(state: Dict) -> Dict:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你正在为一个用户做决策：

用户画像：
- 擅长：数据 / 工具 / 自动化
- 目标：跨境电商 + AI
- 风格：ROI优先，不做低价值重复劳动

任务：
判断这些知识：

1. 是否值得深入？
2. 是否已经是红海？
3. 是否适合自动化？
4. 是否适合长期做？

输出：
- 高价值 / 中价值 / 低价值
- 原因"""),
        ("human", "{knowledge_text}")
    ])
    chain = prompt | llm
    result = chain.invoke({"knowledge_text": state["knowledge"]})
    return {"evaluation": str(result.content)}


def note_node(state: Dict) -> Dict:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", """请生成一个Obsidian风格的Markdown笔记。

格式要求：
# [标题]（课程提炼）

## 🧠 核心结论
- [结论要点]

## 📌 关键知识
- [知识要点]

## 💡 启发（针对我）
- [启发要点]

## 🎯 行动建议
- [建议要点]

## 🏷 标签
#[标签1] #[标签2] #[标签3]

标签建议：包含 #跨境电商 #TikTok #选品 等相关标签"""),
        ("human", """知识结构：
{knowledge_text}

价值评估：
{evaluation_text}""")
    ])
    chain = prompt | llm
    result = chain.invoke({
        "knowledge_text": state["knowledge"],
        "evaluation_text": state["evaluation"]
    })
    
    note_content = str(result.content)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    note_path = Path("output/obsidian") / f"learning_note_{timestamp}.md"
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text(note_content, encoding="utf-8")
    
    return {"note": note_content, "note_path": str(note_path)}


def log_node(state: Dict) -> Dict:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_content = f"""# Learning Log

时间：{timestamp}

输入：
{state['source_file']}

决策：
- 执行信息过滤
- 执行知识抽取
- 执行价值评估
- 生成Obsidian笔记

处理结果：
{str(state['evaluation'])}

生成文件：
- Obsidian笔记: {state['note_path']}
"""
    
    log_path = Path("output/logs") / f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(log_content, encoding="utf-8")
    
    return {"log": log_content, "log_path": str(log_path)}
