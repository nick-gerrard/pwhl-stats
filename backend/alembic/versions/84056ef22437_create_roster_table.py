"""create roster table

Revision ID: 84056ef22437
Revises: cb07011b8953
Create Date: 2026-04-07 03:40:18.790751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84056ef22437'
down_revision: Union[str, Sequence[str], None] = 'cb07011b8953'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE roster (
            id SERIAL PRIMARY KEY,
            player_id INTEGER NOT NULL REFERENCES players(id),
            team_id INTEGER NOT NULL REFERENCES teams(id),
            season_id INTEGER NOT NULL REFERENCES seasons(id),
            player_number SMALLINT,
            is_rookie BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
)

    """)

def downgrade() -> None:
    op.execute("DROP TABLE roster")
