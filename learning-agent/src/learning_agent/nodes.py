import json
import os
import re
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def get_llm(strong: bool = False) -> ChatOpenAI:
    dual_enabled = os.getenv("DUAL_MODEL_ENABLED", "false").lower() == "true"
    if strong or not dual_enabled:
        model = os.getenv("OPENAI_MODEL", "gpt-4")
    else:
        model = os.getenv("OPENAI_FAST_MODEL", "gpt-4o-mini")
    return ChatOpenAI(model=model, temperature=0.7)


def extract_text_content(result) -> str:
    content = result.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
                elif item.get("type") == "code":
                    text_parts.append(f"```\n{item.get('text', '')}\n```")
            elif isinstance(item, str):
                text_parts.append(item)
        return "\n".join(text_parts)
    return str(content)


def parse_json_output(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
        text = text.strip()
    return json.loads(text)


def initial_analysis_node(state: Dict) -> Dict:
    llm = get_llm(strong=True)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """你是一个学习内容分析专家。分析输入文本，输出结构化JSON。

领域枚举：跨境电商, AI工具, 自动化, 流量增长, 商业模式
类型枚举：方法论, 教程, 工具, 行业认知

规则：
- 课程/卖课内容 → bias_risk 设为"高"
- AI生成的摘要 → credibility 下降一级
- 有实操步骤/数据支撑 → credibility 设为"高"
- topic 必须去除品牌词，标准化为通用概念
- summary 压缩至原文 ≤20%，保留核心信息

输出JSON格式：
{{
  "domain": "从枚举中选择",
  "subdomain": "具体子领域",
  "type": "从枚举中选择",
  "topic": "标准化主题（去品牌词）",
  "source": {{
    "source_name": "来源名称",
    "source_type": "来源类型（课程/文章/视频/报告等）",
    "credibility": "高/中/低",
    "bias_risk": "高/中/低",
    "need_verification": true或false
  }},
  "summary": "压缩后的内容摘要"
}}

只输出JSON，不要其他内容。""",
            ),
            ("human", "来源文件：{source_file}\n\n内容：\n{raw_text}"),
        ]
    )
    chain = prompt | llm
    result = chain.invoke(
        {
            "source_file": state["source_file"],
            "raw_text": state["raw_text"],
        }
    )
    parsed = parse_json_output(extract_text_content(result))
    return {
        "domain": parsed.get("domain", ""),
        "subdomain": parsed.get("subdomain", ""),
        "type": parsed.get("type", ""),
        "topic": parsed.get("topic", ""),
        "source": parsed.get("source", {}),
        "summary": parsed.get("summary", ""),
    }


def content_filtering_node(state: Dict) -> Dict:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """你是内容过滤专家。从摘要中删除以下内容：
- 宣传内容和营销话术
- 机构介绍和讲师背景
- 无实际执行价值的信息
- 重复内容

只保留：
- 策略和方法
- 数据和指标
- 具体操作流程
- 可执行的步骤

输出JSON格式：
{{"filtered_content": "过滤后的内容"}}

只输出JSON，不要其他内容。""",
            ),
            ("human", "{summary}"),
        ]
    )
    chain = prompt | llm
    result = chain.invoke({"summary": state["summary"]})
    parsed = parse_json_output(extract_text_content(result))
    return {"filtered_content": parsed.get("filtered_content", "")}


def knowledge_structuring_node(state: Dict) -> Dict:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """你是知识结构化专家。将过滤后的内容结构化为以下分类：

输出JSON格式：
{{
  "market": ["市场认知相关要点"],
  "model": ["商业模式相关要点"],
  "process": ["操作流程相关要点"],
  "data": ["关键数据和指标"],
  "strategy": ["可复制策略"]
}}

要求：
- 每个分类下的要点必须简洁有价值
- 去除废话，只保留核心信息
- 如果某个分类无相关内容，使用空列表

只输出JSON，不要其他内容。""",
            ),
            ("human", "{filtered_content}"),
        ]
    )
    chain = prompt | llm
    result = chain.invoke({"filtered_content": state["filtered_content"]})
    parsed = parse_json_output(extract_text_content(result))
    return {"structured": parsed}


def value_evaluation_node(state: Dict) -> Dict:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """你是价值评估专家。基于结构化知识和来源信息评估知识价值。

判断标准：
- 是否能提升收入
- 是否可规模化
- 是否可自动化
- 是否有复利效应
- 是否已进入红海

规则：
- 入门级知识 → 价值低
- 无壁垒 → 降级
- 可系统化/自动化 → 高价值
- 有数据支撑 → 加分

输出JSON格式：
{{
  "value_level": "高/中/低",
  "roi": "高/中/低",
  "long_term": true或false,
  "reason": "价值判断理由",
  "insight": "核心洞察",
  "action": "建议行动"
}}

只输出JSON，不要其他内容。""",
            ),
            ("human", "结构化知识：{structured}\n\n来源信息：{source}"),
        ]
    )
    chain = prompt | llm
    result = chain.invoke(
        {
            "structured": json.dumps(state["structured"], ensure_ascii=False),
            "source": json.dumps(state["source"], ensure_ascii=False),
        }
    )
    parsed = parse_json_output(extract_text_content(result))
    return {"evaluation": parsed}


def knowledge_matching_node(state: Dict) -> Dict:
    obsidian_dir = Path("output/obsidian")
    if not obsidian_dir.exists():
        return {"matched_file": "", "similarity": 0.0}

    topic = state.get("topic", "")
    domain = state.get("domain", "")
    query = f"{domain} {topic}".strip().lower()

    best_match = ""
    best_score = 0.0

    for md_file in obsidian_dir.rglob("*.md"):
        rel_path = md_file.relative_to(obsidian_dir)
        path_str = (
            str(rel_path)
            .replace("\\", "/")
            .replace("/", " ")
            .replace(".md", "")
            .lower()
        )
        score = SequenceMatcher(None, query, path_str).ratio()
        if score > best_score:
            best_score = score
            best_match = str(md_file)

    if best_score > 0.7:
        return {"matched_file": best_match, "similarity": best_score}
    return {"matched_file": "", "similarity": best_score}


def note_generation_node(state: Dict) -> Dict:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """你是知识笔记生成专家。基于结构化数据生成完整的Markdown笔记。

必须包含以下所有模块，格式严格如下：

# [{topic}]

## 🧠 核心结论（必须有判断）
一句话判断值不值得做

## 📊 价值评级
- 价值等级：{value_level}
- ROI潜力：{roi}
- 是否长期方向：{long_term}

## 📌 关键知识
列出关键知识点

## ⚙️ 可执行策略
列出可执行的具体策略

## 💡 启发（结合用户目标）
结合用户擅长数据/工具/自动化，目标跨境电商+AI，风格ROI优先

## 🔗 关联知识
用Obsidian双链格式，如 [[跨境电商_选品逻辑_策略]]

## � 信息来源
- 来源名称：{source_name}
- 来源文件：{source_file}
- 来源类型：{source_type}

## � 可信度评估
- 可信度：{credibility}
- 偏差风险：{bias_risk}
- 是否需要验证：{need_verification}

## 🧪 验证状态
- 未验证

## 🏷 标签
- 领域标签
- 能力标签
- 属性标签（如#高ROI #红海）

只输出Markdown内容，不要输出其他内容。""",
            ),
            (
                "human",
                "领域：{domain}\n子领域：{subdomain}\n类型：{type}\n主题：{topic}\n来源信息：{source}\n结构化知识：{structured}\n价值评估：{evaluation}",
            ),
        ]
    )
    chain = prompt | llm
    result = chain.invoke(
        {
            "domain": state["domain"],
            "subdomain": state["subdomain"],
            "type": state["type"],
            "topic": state["topic"],
            "source": json.dumps(state["source"], ensure_ascii=False),
            "source_file": state["source_file"],
            "structured": json.dumps(state["structured"], ensure_ascii=False),
            "evaluation": json.dumps(state["evaluation"], ensure_ascii=False),
            "value_level": state["evaluation"].get("value_level", "中"),
            "roi": state["evaluation"].get("roi", "中"),
            "long_term": "是" if state["evaluation"].get("long_term", False) else "否",
            "source_name": state["source"].get("source_name", ""),
            "source_type": state["source"].get("source_type", ""),
            "credibility": state["source"].get("credibility", ""),
            "bias_risk": state["source"].get("bias_risk", ""),
            "need_verification": "是"
            if state["source"].get("need_verification", False)
            else "否",
        }
    )
    content = extract_text_content(result)

    domain = state["domain"]
    subdomain = state["subdomain"]
    type_ = state["type"]
    topic = state["topic"]

    safe_topic = re.sub(r'[<>:"/\\|?*]', "_", topic)
    path = f"{domain}/{subdomain}/{type_}"
    filename = f"{safe_topic}.md"

    return {
        "path": path,
        "filename": filename,
        "content": content,
    }


def merge_or_create_node(state: Dict) -> Dict:
    obsidian_dir = Path("output/obsidian")
    note_dir = obsidian_dir / state["path"]
    note_dir.mkdir(parents=True, exist_ok=True)

    matched_file = state.get("matched_file", "")
    similarity = state.get("similarity", 0.0)
    content = state["content"]
    topic = state["topic"]

    if matched_file and similarity > 0.7:
        try:
            existing_path = Path(matched_file)
            existing_content = existing_path.read_text(encoding="utf-8")
            date_str = datetime.now().strftime("%Y-%m-%d")
            source_name = state["source"].get("source_name", "未知来源")
            evaluation = state["evaluation"]
            iteration = f"""

## 🔄 认知迭代记录

- [{date_str}]
  - 来源：{source_name}
  - 新增结论：{evaluation.get("insight", "无")}
  - 修正观点：{evaluation.get("reason", "无")}
"""
            merged_content = existing_content + iteration
            existing_path.write_text(merged_content, encoding="utf-8")
            return {"note_path": str(existing_path)}
        except Exception:
            fallback_name = f"{topic}__v2.md"
            fallback_path = note_dir / fallback_name
            fallback_path.write_text(content, encoding="utf-8")
            return {"note_path": str(fallback_path)}
    else:
        note_path = note_dir / state["filename"]
        try:
            note_path.write_text(content, encoding="utf-8")
            return {"note_path": str(note_path)}
        except Exception:
            fallback_name = f"{topic}__v2.md"
            fallback_path = note_dir / fallback_name
            fallback_path.write_text(content, encoding="utf-8")
            return {"note_path": str(fallback_path)}


def log_generation_node(state: Dict) -> Dict:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    evaluation = state.get("evaluation", {})
    source = state.get("source", {})
    matched_file = state.get("matched_file", "")
    similarity = state.get("similarity", 0.0)

    if matched_file and similarity > 0.7:
        match_info = f"匹配到已有笔记：{matched_file}（相似度：{similarity:.2f}）"
        write_action = "追加认知迭代记录"
    else:
        match_info = "未匹配到已有笔记"
        write_action = "创建新笔记"

    risk = source.get("bias_risk", "未知")
    need_verification = source.get("need_verification", False)

    log_content = f"""# Learning Log

时间：{timestamp}
来源文件：{state["source_file"]}
领域：{state["domain"]}/{state["subdomain"]}
主题：{state["topic"]}

匹配情况：{match_info}
价值判断：{evaluation.get("value_level", "未知")} - {evaluation.get("reason", "无")}

是否写入：是
原因：{write_action}

风险：偏差风险-{risk}，需验证-{"是" if need_verification else "否"}
"""

    log_dir = Path("output/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    log_path.write_text(log_content, encoding="utf-8")

    return {"log": log_content, "log_path": str(log_path)}
