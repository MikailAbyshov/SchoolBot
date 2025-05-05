from dataclasses import dataclass

@dataclass
class ResponseStudentInitial:
    self_id: int
    name: str
    tg_teg: str
    parent_name: str
    parent_tg_teg: str
    timezone: str
