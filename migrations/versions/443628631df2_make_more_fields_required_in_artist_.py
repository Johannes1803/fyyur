"""make more fields required in artist model

Revision ID: 443628631df2
Revises: ee67336ff606
Create Date: 2022-12-14 13:57:12.879641

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '443628631df2'
down_revision = 'ee67336ff606'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###
