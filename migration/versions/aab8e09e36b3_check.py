"""check

Revision ID: aab8e09e36b3
Revises: 4b64e0d79743
Create Date: 2024-05-04 19:29:51.138347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aab8e09e36b3'
down_revision = '4b64e0d79743'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'purchase', 'wallet', ['wallet_id'], ['id'])
    op.alter_column('wallet', 'password',
               existing_type=sa.VARCHAR(),
               nullable=0)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('wallet', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint(None, 'purchase', type_='foreignkey')
    # ### end Alembic commands ###