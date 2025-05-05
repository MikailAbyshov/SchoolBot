from dataclasses import dataclass
from typing import List
from Application.Respones.Student.ResponseStudentBriefForParent import ResponseStudentBriefForParent

@dataclass
class ResponseParentInitial:
    name: str
    tg_teg: str
    timezone: str
    students: List[ResponseStudentBriefForParent]

