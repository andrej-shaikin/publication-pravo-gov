"""remove npa document name unique

Revision ID: 8d40da51fdfd
Revises: 1b568f025b42
Create Date: 2022-09-15 22:20:03.984698

"""
from alembic import op
import sqlalchemy as sa
import ormar


# revision identifiers, used by Alembic.
revision = '8d40da51fdfd'
down_revision = '1b568f025b42'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('npa_documents_name_key', 'npa_documents', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('npa_documents_name_key', 'npa_documents', ['name'])
    # ### end Alembic commands ###