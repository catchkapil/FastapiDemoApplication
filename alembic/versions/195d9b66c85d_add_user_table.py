"""add user table

Revision ID: 195d9b66c85d
Revises: d12dd26c3408
Create Date: 2022-07-12 10:50:22.444240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '195d9b66c85d'
down_revision = 'd12dd26c3408'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column('id', sa.Integer(),
                              primary_key=True, nullable=False),
                    sa.Column('email', sa.String(),
                              nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
