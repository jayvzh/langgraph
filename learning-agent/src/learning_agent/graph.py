from pathlib import Path
from docx import Document
from langgraph.graph import StateGraph, START, END
from .state import LearningState
from .nodes import filter_node, extract_node, evaluate_node, note_node, log_node


def read_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def create_graph() -> StateGraph:
    graph = StateGraph(LearningState)
    
    graph.add_node("filter", filter_node)
    graph.add_node("extract", extract_node)
    graph.add_node("evaluate", evaluate_node)
    graph.add_node("note", note_node)
    graph.add_node("log", log_node)
    
    graph.add_edge(START, "filter")
    graph.add_edge("filter", "extract")
    graph.add_edge("extract", "evaluate")
    graph.add_edge("evaluate", "note")
    graph.add_edge("note", "log")
    graph.add_edge("log", END)
    
    return graph.compile()


def run_learning_agent(docx_path: str) -> dict:
    app = create_graph()
    raw_text = read_docx(docx_path)
    
    initial_state: LearningState = {
        "raw_text": raw_text,
        "source_file": Path(docx_path).name,
        "filtered": "",
        "knowledge": "",
        "evaluation": "",
        "note": "",
        "log": "",
        "note_path": None,
        "log_path": None,
    }
    
    result = app.invoke(initial_state)
    return result
