"""add page table

Revision ID: de0e0ba47366
Revises: 9dababc2b444
Create Date: 2023-09-07 23:04:48.741705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de0e0ba47366'
down_revision = '9dababc2b444'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pages',
    sa.Column('_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('html', sa.Text(), nullable=True),
    sa.Column('tags', sa.String(), nullable=True),
    sa.Column('create_date', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('toc', sa.String(), nullable=True),
    sa.Column('meta', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pages')
    # ### end Alembic commands ###
