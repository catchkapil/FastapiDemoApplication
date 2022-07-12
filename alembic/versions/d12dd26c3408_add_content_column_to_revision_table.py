"""add content column to revision table

Revision ID: d12dd26c3408
Revises: 9b949a37ff15
Create Date: 2022-07-12 10:44:44.721502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd12dd26c3408'
down_revision = '9b949a37ff15'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
