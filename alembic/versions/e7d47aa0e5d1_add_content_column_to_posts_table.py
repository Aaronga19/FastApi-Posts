"""add content column to posts table

Revision ID: e7d47aa0e5d1
Revises: 9f9ddc79007e
Create Date: 2021-11-25 14:00:57.283903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7d47aa0e5d1'
down_revision = '9f9ddc79007e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('Content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
