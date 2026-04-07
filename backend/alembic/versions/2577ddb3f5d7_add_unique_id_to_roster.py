"""add unique id to roster

Revision ID: 2577ddb3f5d7
Revises: 7bc74a42204b
Create Date: 2026-04-07 05:34:52.223399

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2577ddb3f5d7"
down_revision: str | Sequence[str] | None = "7bc74a42204b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE roster
    ADD CONSTRAINT roster_player_team_season_unique
    UNIQUE (player_id, team_id, season_id)
    """)


def downgrade() -> None:
    op.execute("ALTER TABLE roster DROP CONSTRAINT roster_player_team_season_unique")
