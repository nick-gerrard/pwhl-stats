"""add_regulation_wins_to_standings

Revision ID: c943fd8f64a7
Revises: a490390c8d65
Create Date: 2026-04-08 22:29:26.968952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c943fd8f64a7'
down_revision: Union[str, Sequence[str], None] = 'a490390c8d65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE standings ADD COLUMN regulation_wins SMALLINT NOT NULL DEFAULT 0")


def downgrade() -> None:
    op.execute("ALTER TABLE standings DROP COLUMN regulation_wins")
