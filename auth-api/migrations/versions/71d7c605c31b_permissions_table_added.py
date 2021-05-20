"""permissions table added

Revision ID: 71d7c605c31b
Revises: 437ce1f93861
Create Date: 2020-05-21 06:44:19.919598

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '71d7c605c31b'
down_revision = '437ce1f93861'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    permissions_table = op.create_table('permissions',
                                        sa.Column('created', sa.DateTime(), nullable=True),
                                        sa.Column('modified', sa.DateTime(), nullable=True),
                                        sa.Column('id', sa.Integer(), nullable=False),
                                        sa.Column('membership_type_code', sa.String(length=15), nullable=False),
                                        sa.Column('actions', sa.String(length=100), autoincrement=False,
                                                  nullable=False),
                                        sa.Column('created_by_id', sa.Integer(), nullable=True),
                                        sa.Column('modified_by_id', sa.Integer(), nullable=True),
                                        sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
                                        sa.ForeignKeyConstraint(['membership_type_code'], ['membership_type.code'], ),
                                        sa.ForeignKeyConstraint(['modified_by_id'], ['user.id'], ),
                                        sa.PrimaryKeyConstraint('id')
                                        )

    # Insert code values
    op.bulk_insert(
        permissions_table,
        [
            {'id': '1', 'membership_type_code': 'ADMIN', 'actions': 'REMOVE_BUSINESS'},
            {'id': '2', 'membership_type_code': 'ADMIN', 'actions': 'CHANGE_ADDRESS'},
            {'id': '3', 'membership_type_code': 'COORDINATOR', 'actions': 'CHANGE_ADDRESS'},
            {'id': '4', 'membership_type_code': 'ADMIN', 'actions': 'CHANGE_ORG_NAME'},
            {'id': '5', 'membership_type_code': 'COORDINATOR', 'actions': 'INVITE_MEMBERS'},
            {'id': '6', 'membership_type_code': 'ADMIN', 'actions': 'INVITE_MEMBERS'},
            {'id': '7', 'membership_type_code': 'ADMIN', 'actions': 'CHANGE_ACCOUNT_TYPE'},
            {'id': '8', 'membership_type_code': 'ADMIN', 'actions': 'CHANGE_ROLE'},
            {'id': '9', 'membership_type_code': 'COORDINATOR', 'actions': 'CHANGE_ROLE'},
        ]
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('permissions')
    # ### end Alembic commands ###
