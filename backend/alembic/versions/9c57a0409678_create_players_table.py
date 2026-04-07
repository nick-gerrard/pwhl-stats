"""create players table

Revision ID: 9c57a0409678
Revises: 8cfa6ee2eb62
Create Date: 2026-04-07 03:16:06.569812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c57a0409678'
down_revision: Union[str, Sequence[str], None] = '8cfa6ee2eb62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE players (
            id SERIAL PRIMARY KEY,
            api_id INTEGER UNIQUE NOT NULL,
            first_name VARCHAR NOT NULL,
            last_name VARCHAR NOT NULL,
            height SMALLINT,
            weight SMALLINT,
            birthdate DATE,
            nationality VARCHAR,
            shoots CHAR(1),
            position VARCHAR(2),
            active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE players")
