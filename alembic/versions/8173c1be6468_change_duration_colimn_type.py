"""change duration colimn type

Revision ID: 8173c1be6468
Revises: 184b0689009a
Create Date: 2026-02-23 17:40:42.135600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8173c1be6468'
down_revision = '184b0689009a'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'services',
        'duration',
        type_=sa.Integer(),
        existing_type=sa.Interval(),
        postgresql_using='EXTRACT(EPOCH FROM duration)::integer'
    )


def downgrade():
    op.alter_column(
        'services',
        'duration',
        type_=sa.Interval(),
        existing_type=sa.Integer(),
        postgresql_using="make_interval(secs => duration)"
    )
