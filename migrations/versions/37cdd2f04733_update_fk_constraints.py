"""update fk constraints

Revision ID: 37cdd2f04733
Revises: 83c1aefc80fe
Create Date: 2018-08-02 14:37:14.967085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37cdd2f04733'
down_revision = '83c1aefc80fe'
branch_labels = None
depends_on = None


def upgrade():
    # update services_groups foreign key constraint
    op.drop_constraint('project_fk', 'services_groups')
    op.create_foreign_key('project_fk', 'services_groups', 'projects', ['project_id'], ['id'], ondelete='SET NULL')
    # update metrics foreign key constraint
    op.drop_constraint('projects_fk', 'metrics')
    op.create_foreign_key('project_fk', 'metrics', 'projects', ['project_id'], ['id'], ondelete='SET NULL')


def downgrade():
    # return previous services_groups foreign key constraint
    op.drop_constraint('project_fk', 'services_groups')
    op.create_foreign_key('project_fk', 'services_groups', 'projects', ['project_id'], ['id'])
    # return previous metrics foreign key constraint
    op.drop_constraint('projects_fk', 'metrics')
    op.create_foreign_key('project_fk', 'metrics', 'projects', ['project_id'],['id'])