from sqlalchemy.types import TypeDecorator, Integer
from datetime import timedelta

class MinuteInterval(TypeDecorator):
    impl = Integer

    def process_bind_param(self, value: timedelta, dialect):
        if value is None:
            return None
        return int(value.total_seconds() // 60)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return timedelta(minutes=value)
