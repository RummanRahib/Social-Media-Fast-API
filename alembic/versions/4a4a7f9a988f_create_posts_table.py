"""create posts table

Revision ID: 4a4a7f9a988f
Revises: 
Create Date: 2022-01-21 22:16:26.501000

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '4a4a7f9a988f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False)
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
