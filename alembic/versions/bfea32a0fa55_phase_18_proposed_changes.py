"""phase_18_proposed_changes

Revision ID: bfea32a0fa55
Revises: 9fde5c2f129e
Create Date: 2026-09-03 13:37:03.807849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bfea32a0fa55'
down_revision: Union[str, Sequence[str], None] = '9fde5c2f129e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'proposed_authority_changes',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('source_id', sa.String(), nullable=False),
        sa.Column('authority_id', sa.String(), nullable=False),
        sa.Column('field_name', sa.String(), nullable=False),
        sa.Column('old_value', sa.String(), nullable=True),
        sa.Column('proposed_value', sa.String(), nullable=True),
        sa.Column('evidence_snippet', sa.String(), nullable=True),
        sa.Column('change_type', sa.String(), nullable=False),
        sa.Column('confidence', sa.String(), nullable=False),
        sa.Column('review_status', sa.String(), nullable=True),
        sa.Column('reviewed_by', sa.String(), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('review_notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['authority_id'], ['authorities.id'], ),
        sa.ForeignKeyConstraint(['source_id'], ['official_authority_sources.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_proposed_authority_changes_authority_id'), 'proposed_authority_changes', ['authority_id'], unique=False)
    op.create_index(op.f('ix_proposed_authority_changes_source_id'), 'proposed_authority_changes', ['source_id'], unique=False)
    op.create_index(op.f('ix_proposed_authority_changes_review_status'), 'proposed_authority_changes', ['review_status'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_proposed_authority_changes_review_status'), table_name='proposed_authority_changes')
    op.drop_index(op.f('ix_proposed_authority_changes_source_id'), table_name='proposed_authority_changes')
    op.drop_index(op.f('ix_proposed_authority_changes_authority_id'), table_name='proposed_authority_changes')
    op.drop_table('proposed_authority_changes')
