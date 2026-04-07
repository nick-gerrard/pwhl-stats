"""add unique id to goalie_stats

Revision ID: 0106a8906cec
Revises: f37a0fa5deeb
Create Date: 2026-04-07 05:43:22.911449

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0106a8906cec"
down_revision: str | Sequence[str] | None = "f37a0fa5deeb"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE goalie_stats ADD CONSTRAINT goalie_stats_player_team_season_unique UNIQUE (player_id, team_id, season_id);"
    )


def downgrade() -> None:
    op.execute("ALTER TABLE goalie_stats DROP CONSTRAINT goalie-stats_player_team_season_unique")
