"""phase_17_snapshots

Revision ID: 9fde5c2f129e
Revises: 1e36fdfea038
Create Date: 2026-09-03 12:43:09.520847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fde5c2f129e'
down_revision: Union[str, Sequence[str], None] = '1e36fdfea038'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('official_authority_sources', sa.Column('last_extracted_text', sa.String(), nullable=True))
    op.add_column('official_authority_sources', sa.Column('previous_extracted_text', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('official_authority_sources', 'previous_extracted_text')
    op.drop_column('official_authority_sources', 'last_extracted_text')
