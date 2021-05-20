"""added tasks table

Revision ID: 379f1d6b24d4
Revises: 2d71e7d7cc18
Create Date: 2021-03-31 11:53:00.954517

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '379f1d6b24d4'
down_revision = '2d71e7d7cc18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('date_submitted', sa.DateTime(), nullable=True),
    sa.Column('relationship_type', sa.String(length=50), nullable=False),
    sa.Column('relationship_id', sa.Integer(), nullable=False),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('task_type', sa.String(length=50), nullable=False),
    sa.Column('task_status', sa.String(length=50), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('modified_by_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['modified_by_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    op.create_index(op.f('ix_tasks_relationship_id'), 'tasks', ['relationship_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tasks_relationship_id'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    # ### end Alembic commands ###
