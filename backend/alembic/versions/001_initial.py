"""Initial migration - create products table

Revision ID: 001_initial
Revises: 
Create Date: 2024-11-09 22:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create products table
    op.create_table(
        'products',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('bot_username', sa.String(length=255), nullable=True),
        sa.Column('website_link', sa.String(length=500), nullable=True),
        sa.Column('contract_months', sa.Integer(), nullable=False),
        sa.Column('contract_start_date', sa.DateTime(), nullable=False),
        sa.Column('contract_end_date', sa.DateTime(), nullable=False),
        sa.Column('is_renewed', sa.Boolean(), nullable=True),
        sa.Column('status', sa.Enum('Active', 'Expired', 'ExpiringSoon', name='productstatus'), nullable=False),
        sa.Column('customer_telegram', sa.String(length=255), nullable=True),
        sa.Column('customer_link', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for performance
    op.create_index('idx_products_id', 'products', ['id'])
    op.create_index('idx_products_status', 'products', ['status'])
    op.create_index('idx_products_end_date', 'products', ['contract_end_date'])
    op.create_index('idx_products_customer', 'products', ['customer_telegram'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_products_customer', table_name='products')
    op.drop_index('idx_products_end_date', table_name='products')
    op.drop_index('idx_products_status', table_name='products')
    op.drop_index('idx_products_id', table_name='products')
    
    # Drop table
    op.drop_table('products')
    
    # Drop enum type
    sa.Enum(name='productstatus').drop(op.get_bind(), checkfirst=True)
