"""adding address information

Revision ID: 3066b0d6563d
Revises: 4300edf62173
Create Date: 2019-07-28 22:27:52.287149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3066b0d6563d'
down_revision = '4300edf62173'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assessment', sa.Column('address', sa.String(length=80), nullable=True))
    op.add_column('assessment', sa.Column('city', sa.String(length=40), nullable=True))
    op.add_column('assessment', sa.Column('county', sa.String(length=60), nullable=True))
    op.add_column('assessment', sa.Column('state', sa.String(length=20), nullable=True))
    op.drop_column('assessment', 'body')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assessment', sa.Column('body', sa.VARCHAR(length=140), nullable=True))
    op.drop_column('assessment', 'state')
    op.drop_column('assessment', 'county')
    op.drop_column('assessment', 'city')
    op.drop_column('assessment', 'address')
    # ### end Alembic commands ###
