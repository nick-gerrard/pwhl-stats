"""create goalie_stats table

Revision ID: 3a85a86c85e3
Revises: abc115a07137
Create Date: 2026-04-07 03:42:16.317987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a85a86c85e3'
down_revision: Union[str, Sequence[str], None] = 'abc115a07137'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE goalie_stats (
            id SERIAL PRIMARY KEY,
            player_id INTEGER NOT NULL REFERENCES players(id),
            team_id INTEGER NOT NULL REFERENCES teams(id),
            season_id INTEGER NOT NULL REFERENCES seasons(id),
            games_played SMALLINT NOT NULL DEFAULT 0,
            wins SMALLINT NOT NULL DEFAULT 0,
            losses SMALLINT NOT NULL DEFAULT 0,
            ot_losses SMALLINT NOT NULL DEFAULT 0,
            shutouts SMALLINT NOT NULL DEFAULT 0,
            shots_against INTEGER NOT NULL DEFAULT 0,
            goals_against INTEGER NOT NULL DEFAULT 0,
            save_percentage NUMERIC(5,3),
            gaa NUMERIC(4,2),
            minutes_played INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
)
    """
    )


def downgrade() -> None:
    op.execute("DROP TABLE goalie_stats")
