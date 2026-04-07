"""create seasons table

Revision ID: 8cfa6ee2eb62
Revises: dc89a9396b1e
Create Date: 2026-04-07 03:13:42.133522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cfa6ee2eb62'
down_revision: Union[str, Sequence[str], None] = 'dc89a9396b1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE seasons (
            id SERIAL PRIMARY KEY,
            api_id INTEGER UNIQUE NOT NULL,
            name VARCHAR NOT NULL,
            start_date DATE,
            end_date DATE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE seasons")
    pass
