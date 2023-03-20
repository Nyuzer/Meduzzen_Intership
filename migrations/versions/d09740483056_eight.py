"""Eight

Revision ID: d09740483056
Revises: 0654f3959082
Create Date: 2023-03-13 18:26:32.124376

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'd09740483056'
down_revision = '0654f3959082'
branch_labels = None
depends_on = None

TYPES = [
    ('general-user', 'General user'),
    ('owner', 'Owner')
]

TYPES2 = [
    ('invited', 'Invited to company'),
    ('accession-request', 'Accession request to company')
]


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('type_of_request', sqlalchemy_utils.types.choice.ChoiceType(TYPES2), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_actions_id'), 'actions', ['id'], unique=True)
    op.create_table('companies_members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role', sqlalchemy_utils.types.choice.ChoiceType(TYPES), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_companies_members_id'), 'companies_members', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_companies_members_id'), table_name='companies_members')
    op.drop_table('companies_members')
    op.drop_index(op.f('ix_actions_id'), table_name='actions')
    op.drop_table('actions')
    # ### end Alembic commands ###
