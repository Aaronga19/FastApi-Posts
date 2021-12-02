"""add users table

Revision ID: 86964c5c96d0
Revises: e7d47aa0e5d1
Create Date: 2021-11-25 14:06:17.203527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86964c5c96d0'
down_revision = 'e7d47aa0e5d1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'), nullable=False),
        sa.Column('premium',sa.Boolean, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        )


def downgrade():
    op.drop_table('users')
    pass
