"""add playoff_series_id to games

Revision ID: a7690bb0da98
Revises: e8869456c548
Create Date: 2026-04-08 15:00:41.534484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7690bb0da98'
down_revision: Union[str, Sequence[str], None] = 'e8869456c548'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE games
        ADD COLUMN playoff_series_id INTEGER REFERENCES playoff_series(id)
    """)


def downgrade() -> None:
    op.execute("ALTER TABLE games DROP COLUMN playoff_series_id")
