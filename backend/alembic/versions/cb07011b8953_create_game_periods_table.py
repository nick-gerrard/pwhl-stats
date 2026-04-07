"""create game_periods table

Revision ID: cb07011b8953
Revises: 8b9fe4cdb73f
Create Date: 2026-04-07 03:39:24.540289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb07011b8953'
down_revision: Union[str, Sequence[str], None] = '8b9fe4cdb73f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE game_periods (
            id SERIAL PRIMARY KEY,
            game_id INTEGER NOT NULL REFERENCES games(id),
            period SMALLINT NOT NULL,
            home_score INTEGER NOT NULL,
            away_score INTEGER NOT NULL
)

    """)


def downgrade() -> None:
    op.execute("DROP TABLE game_periods")
    pass
