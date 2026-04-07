"""add unique id to standings

Revision ID: 051a62415528
Revises: 2577ddb3f5d7
Create Date: 2026-04-07 05:39:58.247713

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "051a62415528"
down_revision: str | Sequence[str] | None = "2577ddb3f5d7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE standings ADD CONSTRAINT standings_team_season_unique UNIQUE (team_id, season_id);

    
    """)


def downgrade() -> None:
    op.execute("ALTER TABLE standings DROP CONSTRAINT standings_team_season_unique")
