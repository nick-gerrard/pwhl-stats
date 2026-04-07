"""create teams table

Revision ID: dc89a9396b1e
Revises: 
Create Date: 2026-04-07 03:06:34.531986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc89a9396b1e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE teams (
            id SERIAL PRIMARY KEY,
            api_id INTEGER UNIQUE NOT NULL,
            name VARCHAR NOT NULL,
            city VARCHAR NOT NULL,
            code VARCHAR(10) NOT NULL,
            nickname VARCHAR,
            logo_url VARCHAR
        )
    """)
    pass


def downgrade() -> None:
    op.execute("DROP TABLE teams")
    pass
