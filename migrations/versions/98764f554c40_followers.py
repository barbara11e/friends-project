"""followers

Revision ID: 98764f554c40
Revises: c2f587324835
Create Date: 2020-05-30 13:45:09.047604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98764f554c40'
down_revision = 'c2f587324835'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###