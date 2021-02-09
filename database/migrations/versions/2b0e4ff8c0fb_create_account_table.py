"""create account table

Revision ID: 2b0e4ff8c0fb
Revises:
Create Date: 2021-02-01 11:34:30.405831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b0e4ff8c0fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_info',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('fullName', sa.String(300), nullable=False),
        sa.Column('username', sa.String(100), nullable=False),
        sa.Column('password', sa.String(300), nullable=False),
        sa.Column('email', sa.String(300), nullable=False),
        sa.Column('admin', sa.Boolean),
    )
    op.create_table(
        'product_info',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('productName', sa.String(300), nullable=False),
        sa.Column('userId', sa.Integer, nullable=False),
        sa.Column('code', sa.String(100), nullable=False),
        sa.Column('description', sa.String(1000)),
        sa.Column('price', sa.Float, nullable=False),
    )


def downgrade():
    op.drop_table('user_info')
    op.drop_table('product_info')
