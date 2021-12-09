"""add foreignkey to post table

Revision ID: 149b4d03f68c
Revises: 86964c5c96d0
Create Date: 2021-11-25 14:22:54.689192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '149b4d03f68c'
down_revision = '86964c5c96d0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
        local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')

    pass
