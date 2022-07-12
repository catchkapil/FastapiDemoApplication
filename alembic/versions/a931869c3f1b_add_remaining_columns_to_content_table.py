"""Add remaining columns to content table

Revision ID: a931869c3f1b
Revises: 3828b2062b31
Create Date: 2022-07-12 11:13:54.349074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a931869c3f1b'
down_revision = '3828b2062b31'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(),
                            nullable=False, server_default='True'))
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            nullable=False, server_default=sa.text('now()')))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
