"""create playoff_rounds and playoff_series tables

Revision ID: e8869456c548
Revises: 0106a8906cec
Create Date: 2026-04-08 15:00:41.377190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8869456c548'
down_revision: Union[str, Sequence[str], None] = '0106a8906cec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE playoff_rounds (
            id SERIAL PRIMARY KEY,
            season_id INTEGER NOT NULL REFERENCES seasons(id),
            round_number INTEGER NOT NULL,
            round_name VARCHAR NOT NULL,
            UNIQUE (season_id, round_number)
        )
    """)
    op.execute("""
        CREATE TABLE playoff_series (
            id SERIAL PRIMARY KEY,
            round_id INTEGER NOT NULL REFERENCES playoff_rounds(id),
            season_id INTEGER NOT NULL REFERENCES seasons(id),
            series_letter CHAR(1) NOT NULL,
            series_name VARCHAR NOT NULL,
            team1_id INTEGER NOT NULL REFERENCES teams(id),
            team2_id INTEGER NOT NULL REFERENCES teams(id),
            team1_wins INTEGER NOT NULL DEFAULT 0,
            team2_wins INTEGER NOT NULL DEFAULT 0,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            feeder_series1 CHAR(1),
            feeder_series2 CHAR(1),
            UNIQUE (season_id, series_letter)
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE playoff_series")
    op.execute("DROP TABLE playoff_rounds")
