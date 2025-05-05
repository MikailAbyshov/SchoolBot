from dataclasses import dataclass

@dataclass
class ResponseStudentBriefForParent:
    self_id: int
    name: str
    tg_teg: str
    payment_status: int
