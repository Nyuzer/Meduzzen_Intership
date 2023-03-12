"""Seven_add_uniq

Revision ID: 0654f3959082
Revises: 347321010ced
Create Date: 2023-03-12 16:34:30.295852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0654f3959082'
down_revision = '347321010ced'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'companies', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'companies', type_='unique')
    # ### end Alembic commands ###
