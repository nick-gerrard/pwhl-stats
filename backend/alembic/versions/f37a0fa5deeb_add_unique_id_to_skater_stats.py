"""add unique id to skater_stats

Revision ID: f37a0fa5deeb
Revises: 051a62415528
Create Date: 2026-04-07 05:41:27.931154

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f37a0fa5deeb"
down_revision: str | Sequence[str] | None = "051a62415528"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE skater_stats 
        ADD CONSTRAINT skater_stats_player_team_season_unique 
        UNIQUE (player_id, team_id, season_id);
    """)


def downgrade() -> None:
    op.execute("ALTER TABLE skater_stats DROP CONSTRAINT skater_stats_player_team_season_unizue")
