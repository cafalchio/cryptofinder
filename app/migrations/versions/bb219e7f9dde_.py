"""empty message

Revision ID: bb219e7f9dde
Revises: 
Create Date: 2024-11-10 20:42:03.250606

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bb219e7f9dde'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('all_coins')
    op.drop_table('coins_details')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coins_details',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('symbol', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('added', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=800), autoincrement=False, nullable=True),
    sa.Column('homepage', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='coins_details_pkey')
    )
    op.create_table('all_coins',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('symbol', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('added', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('source', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('is_shit', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='all_coins_pkey')
    )
    # ### end Alembic commands ###
