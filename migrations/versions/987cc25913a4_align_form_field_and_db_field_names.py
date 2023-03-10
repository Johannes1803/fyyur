"""align form field and db field names

Revision ID: 987cc25913a4
Revises: 443628631df2
Create Date: 2022-12-14 15:38:08.341983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '987cc25913a4'
down_revision = '443628631df2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website_link', sa.String(length=120), nullable=True))
        batch_op.drop_column('website')

    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website_link', sa.String(length=120), nullable=True))
        batch_op.drop_column('website')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
        batch_op.drop_column('website_link')

    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
        batch_op.drop_column('website_link')

    # ### end Alembic commands ###
