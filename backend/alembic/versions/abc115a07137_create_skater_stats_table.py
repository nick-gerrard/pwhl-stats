"""create skater_stats table

Revision ID: abc115a07137
Revises: 84056ef22437
Create Date: 2026-04-07 03:41:16.655282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abc115a07137'
down_revision: Union[str, Sequence[str], None] = '84056ef22437'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE skater_stats (
            id SERIAL PRIMARY KEY,
            player_id INTEGER NOT NULL REFERENCES players(id),
            team_id INTEGER NOT NULL REFERENCES teams(id),
            season_id INTEGER NOT NULL REFERENCES seasons(id),
            games_played SMALLINT NOT NULL DEFAULT 0,
            goals SMALLINT NOT NULL DEFAULT 0,
            assists SMALLINT NOT NULL DEFAULT 0,
            pim SMALLINT NOT NULL DEFAULT 0,
            plus_minus SMALLINT NOT NULL DEFAULT 0,
            shots SMALLINT NOT NULL DEFAULT 0,
            avg_toi VARCHAR(8),
            pp_goals SMALLINT NOT NULL DEFAULT 0,
            sh_goals SMALLINT NOT NULL DEFAULT 0,
            gw_goals SMALLINT NOT NULL DEFAULT 0,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
)
    """)


def downgrade() -> None:
    op.execute("DROP TABLE skater_stats")
