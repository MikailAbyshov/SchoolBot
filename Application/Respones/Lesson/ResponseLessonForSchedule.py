from dataclasses import dataclass
from datetime import datetime

@dataclass
class ResponseLessonForSchedule:
    subject_name: str
    self_datetime: datetime
    teacher_name: str
