"""create games table

Revision ID: 8b9fe4cdb73f
Revises: 9c57a0409678
Create Date: 2026-04-07 03:32:09.392845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b9fe4cdb73f'
down_revision: Union[str, Sequence[str], None] = '9c57a0409678'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE games (
            id SERIAL PRIMARY KEY,
            api_id INTEGER UNIQUE NOT NULL,
            season_id INTEGER NOT NULL REFERENCES seasons(id),
            home_team_id INTEGER NOT NULL REFERENCES teams(id),
            visiting_team_id INTEGER NOT NULL REFERENCES teams(id),
            home_score INTEGER,
            away_score INTEGER,
            date DATE NOT NULL,
            status VARCHAR DEFAULT 'scheduled',
            venue VARCHAR,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE games")
