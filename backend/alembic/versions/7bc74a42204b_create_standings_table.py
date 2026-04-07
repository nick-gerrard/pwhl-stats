"""create standings table

Revision ID: 7bc74a42204b
Revises: 3a85a86c85e3
Create Date: 2026-04-07 03:43:11.120003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bc74a42204b'
down_revision: Union[str, Sequence[str], None] = '3a85a86c85e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE standings (
            id SERIAL PRIMARY KEY,
            team_id INTEGER NOT NULL REFERENCES teams(id),
            season_id INTEGER NOT NULL REFERENCES seasons(id),
            wins SMALLINT NOT NULL DEFAULT 0,
            losses SMALLINT NOT NULL DEFAULT 0,
            ot_wins SMALLINT NOT NULL DEFAULT 0,
            ot_losses SMALLINT NOT NULL DEFAULT 0,
            shootout_wins SMALLINT NOT NULL DEFAULT 0,
            shootout_losses SMALLINT NOT NULL DEFAULT 0,
            games_played SMALLINT NOT NULL DEFAULT 0,
            points SMALLINT NOT NULL DEFAULT 0,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )

    """
    )


def downgrade() -> None:
    op.execute("DROP TABLE standings")
