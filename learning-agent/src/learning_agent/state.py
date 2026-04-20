from typing import TypedDict, Optional, Dict


class LearningState(TypedDict):
    raw_text: str
    source_file: str
    domain: str
    subdomain: str
    subsubdomain: str
    type: str
    topic: str
    summary: str
    source: Dict
    filtered_content: str
    structured: Dict
    evaluation: Dict
    matched_file: str
    similarity: float
    path: str
    filename: str
    content: str
    log: str
    note_path: Optional[str]
    log_path: Optional[str]
