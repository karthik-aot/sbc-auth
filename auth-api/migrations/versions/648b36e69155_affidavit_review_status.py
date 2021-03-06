"""affidavit_review_status

Revision ID: 648b36e69155
Revises: 23a3d94ee00d
Create Date: 2020-06-12 12:15:35.531881

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import Boolean, String
from sqlalchemy.sql import column, table


# revision identifiers, used by Alembic.
revision = '648b36e69155'
down_revision = '23a3d94ee00d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('org_status', 'code',
                    existing_type=sa.VARCHAR(length=15),
                    type_=sa.VARCHAR(length=30),
                    existing_nullable=False)
    op.alter_column('org', 'status_code',
                    existing_type=sa.VARCHAR(length=15),
                    type_=sa.VARCHAR(length=30),
                    existing_nullable=False)

    org_status_table = table('org_status',
                             column('code', String),
                             column('desc', String),
                             column('default', Boolean)
                             )
    op.bulk_insert(
        org_status_table,
        [
            {'code': 'PENDING_AFFIDAVIT_REVIEW', 'desc': 'Status for pending affidavit review',
             'default': False}
        ]
    )
    op.execute('update org set status_code = \'PENDING_AFFIDAVIT_REVIEW\' where status_code=\'PENDING\'')
    op.execute('delete from org_status where code=\'PENDING\'')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('update org set status_code = \'PENDING\' where status_code=\'PENDING_AFFIDAVIT_REVIEW\'')
    op.execute('delete from org_status where code=\'PENDING_AFFIDAVIT_REVIEW\'')
    op.alter_column('org_status', 'code',
                    existing_type=sa.VARCHAR(length=30),
                    type_=sa.VARCHAR(length=15),
                    existing_nullable=False)
    # ### end Alembic commands ###
