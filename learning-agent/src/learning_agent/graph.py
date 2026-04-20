from pathlib import Path
from docx import Document
from langgraph.graph import StateGraph, START, END
from .state import LearningState
from .nodes import (
    initial_analysis_node,
    content_filtering_node,
    knowledge_structuring_node,
    value_evaluation_node,
    knowledge_matching_node,
    note_generation_node,
    merge_or_create_node,
    log_generation_node,
)


def read_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def create_graph() -> StateGraph:
    graph = StateGraph(LearningState)

    graph.add_node("initial_analysis", initial_analysis_node)
    graph.add_node("content_filtering", content_filtering_node)
    graph.add_node("knowledge_structuring", knowledge_structuring_node)
    graph.add_node("value_evaluation", value_evaluation_node)
    graph.add_node("knowledge_matching", knowledge_matching_node)
    graph.add_node("note_generation", note_generation_node)
    graph.add_node("merge_or_create", merge_or_create_node)
    graph.add_node("log_generation", log_generation_node)

    graph.add_edge(START, "initial_analysis")
    graph.add_edge("initial_analysis", "content_filtering")
    graph.add_edge("content_filtering", "knowledge_structuring")
    graph.add_edge("knowledge_structuring", "value_evaluation")
    graph.add_edge("value_evaluation", "knowledge_matching")
    graph.add_edge("knowledge_matching", "note_generation")
    graph.add_edge("note_generation", "merge_or_create")
    graph.add_edge("merge_or_create", "log_generation")
    graph.add_edge("log_generation", END)

    return graph.compile()


def run_learning_agent(docx_path: str) -> dict:
    app = create_graph()
    raw_text = read_docx(docx_path)

    initial_state: LearningState = {
        "raw_text": raw_text,
        "source_file": Path(docx_path).name,
        "domain": "",
        "subdomain": "",
        "subsubdomain": "",
        "type": "",
        "topic": "",
        "summary": "",
        "source": {},
        "filtered_content": "",
        "structured": {},
        "evaluation": {},
        "matched_file": "",
        "similarity": 0.0,
        "path": "",
        "filename": "",
        "content": "",
        "log": "",
        "note_path": None,
        "log_path": None,
    }

    result = app.invoke(initial_state)
    return result
