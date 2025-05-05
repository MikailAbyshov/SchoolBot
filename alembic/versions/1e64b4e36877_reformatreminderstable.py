"""ReformatRemindersTable

Revision ID: 1e64b4e36877
Revises: 9e6ef596abc2
Create Date: 2025-04-17 15:40:29.720639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from OPDproject.Infrastructure.DBtypes import MinuteInterval


# revision identifiers, used by Alembic.
revision: str = '1e64b4e36877'
down_revision: Union[str, None] = '9e6ef596abc2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema for SQLite."""
    # 1. Переименовать исходную таблицу
    op.execute("""
        ALTER TABLE reminders RENAME TO reminders_old;
    """)

    # 2. Создать новую таблицу с нужной структурой
    op.create_table(
        'reminders',
        sa.Column('self_id', sa.Integer, primary_key=True),
        sa.Column('lesson_id', sa.Integer, sa.ForeignKey("lessons.self_id", ondelete="CASCADE"), nullable=False),
        sa.Column('student_id', sa.Integer, sa.ForeignKey("students.self_id", ondelete="CASCADE"), nullable=False),
        sa.Column('trigger_time', sa.DateTime, nullable=False),
        sa.Column('time_before_lesson', MinuteInterval(), nullable=False),
        sa.Column('is_sent', sa.Boolean, nullable=False)
    )


    # 4. Удалить временную таблицу
    op.execute("""
        DROP TABLE reminders_old;
    """)

    # 5. Создать индекс
    op.create_index(op.f('ix_reminders_time_before_lesson'), 'reminders', ['time_before_lesson'], unique=False)
    op.create_index(op.f('ix_reminders_trigger_time'), 'reminders', ['trigger_time'], unique=False)
    op.create_index(op.f('ix_reminders_is_sent'), 'reminders', ['is_sent'], unique=False)



def downgrade() -> None:
    """Downgrade schema for SQLite."""
    # 1. Переименовать текущую таблицу
    op.execute("""
        ALTER TABLE reminders RENAME TO reminders_old;
    """)

    # 2. Восстановить старую таблицу без поля time_before_lesson и с типом TIME
    op.create_table(
        'reminders',
        sa.Column('self_id', sa.Integer, primary_key=True),
        sa.Column('trigger_time', sa.Time, nullable=False),
    )

    op.create_table(
        'reminders',
        sa.Column('self_id', sa.Integer, primary_key=True),
        sa.Column('lesson_id', sa.Integer, sa.ForeignKey("lessons.self_id", ondelete="CASCADE"), nullable=False),
        sa.Column('student_id', sa.Integer, sa.ForeignKey("students.self_id", ondelete="CASCADE"), nullable=False),
        sa.Column('time_before_lesson', sa.Time, nullable=False),
        sa.Column('is_sent', sa.Boolean, nullable=False)
    )

    # 4. Удалить временную таблицу
    op.execute("""
        DROP TABLE reminders_old;
    """)
