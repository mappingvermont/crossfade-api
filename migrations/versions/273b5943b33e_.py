"""empty message

Revision ID: 273b5943b33e
Revises: 06ebc4126c55
Create Date: 2016-08-02 07:31:21.230361

"""

# revision identifiers, used by Alembic.
revision = '273b5943b33e'
down_revision = '06ebc4126c55'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('playlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hash_id', sa.String(), nullable=True),
    sa.Column('json_state', postgresql.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('playlist')
    ### end Alembic commands ###
