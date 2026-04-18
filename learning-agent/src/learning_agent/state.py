from typing import TypedDict, Optional


class LearningState(TypedDict):
    raw_text: str
    source_file: str
    filtered: str
    knowledge: str
    evaluation: str
    note: str
    log: str
    note_path: Optional[str]
    log_path: Optional[str]
