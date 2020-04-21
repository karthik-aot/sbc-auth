"""Create invitation type table

Revision ID: 7b0cde979ba5
Revises: 8b49eb83f064
Create Date: 2020-04-06 13:32:32.130313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b0cde979ba5'
down_revision = '8b49eb83f064'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    invitation_type_table = op.create_table('invitation_type',
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('code', sa.String(length=15), nullable=False),
    sa.Column('desc', sa.String(length=100), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('modified_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['modified_by_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('code')
    )

    op.bulk_insert(
    invitation_type_table,
    [
        {'code': 'DIRECTOR_SEARCH', 'desc': 'An invitation to activate a Director\'s Search account', 'default': False},
        {'code': 'STANDARD', 'desc': 'A standard invitation via email that must be approved by an administrator', 'default': True}
    ]
    )

    op.add_column('invitation', sa.Column('type', sa.String(length=15), nullable=True))
    op.create_foreign_key('invitation_type_fkey', 'invitation', 'invitation_type', ['type'], ['code'])
    op.execute("UPDATE invitation SET type = 'DIRECTOR_SEARCH' WHERE invitation_type IS NOT NULL")
    op.execute("UPDATE invitation SET type = 'STANDARD' WHERE invitation_type IS NULL")
    op.alter_column('invitation', 'type', nullable=False)
    op.drop_column('invitation', 'invitation_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('payment_type_code_key', 'payment_type', ['code'])
    op.create_unique_constraint('org_type_code_key', 'org_type', ['code'])
    op.add_column('invitation', sa.Column('invitation_type', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_constraint('invitation_type_fkey', 'invitation', type_='foreignkey')
    op.drop_column('invitation', 'type')
    op.drop_table('invitation_type')
    # ### end Alembic commands ###