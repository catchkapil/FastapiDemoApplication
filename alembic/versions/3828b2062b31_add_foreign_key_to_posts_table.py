"""add foreign key to posts table

Revision ID: 3828b2062b31
Revises: 195d9b66c85d
Create Date: 2022-07-12 11:02:54.790992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3828b2062b31'
down_revision = '195d9b66c85d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
