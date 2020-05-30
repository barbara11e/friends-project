"""address

Revision ID: 9fcae79e3843
Revises: db892ddb9e49
Create Date: 2020-05-30 21:56:19.036317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fcae79e3843'
down_revision = 'db892ddb9e49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('address', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'address')
    # ### end Alembic commands ###