"""add season_type to seasons

Revision ID: a490390c8d65
Revises: a7690bb0da98
Create Date: 2026-04-08 15:05:49.833560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a490390c8d65'
down_revision: Union[str, Sequence[str], None] = 'a7690bb0da98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE seasons
        ADD COLUMN season_type VARCHAR NOT NULL DEFAULT 'regular'
    """)


def downgrade() -> None:
    op.execute("ALTER TABLE seasons DROP COLUMN season_type")
