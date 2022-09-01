"""Init

Revision ID: 7199607f4b3f
Revises:
Create Date: 2022-09-01 16:18:02.203721

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7199607f4b3f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document_types',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True, comment='Активен'),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True, comment='Уникальный идентификатор'),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True, comment='Дата создания'),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, comment='Дата последнего изменения'),
    sa.Column('name', sa.String(length=512), nullable=True, comment='Наименование'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_document_types_id'), 'document_types', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_document_types_id'), table_name='document_types')
    op.drop_table('document_types')
    # ### end Alembic commands ###