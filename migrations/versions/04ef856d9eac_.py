"""empty message

Revision ID: 04ef856d9eac
Revises: 962c9f9e9346
Create Date: 2022-05-02 00:43:02.671988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04ef856d9eac'
down_revision = '962c9f9e9346'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('order_id', sa.String(length=255), nullable=True))
    op.add_column('orders', sa.Column('order_vendor_id', sa.String(length=255), nullable=True))
    op.add_column('orders', sa.Column('order_customer_id', sa.String(length=255), nullable=True))
    op.add_column('orders', sa.Column('order_product_id', sa.String(length=255), nullable=True))
    op.add_column('orders', sa.Column('item_unique_id', sa.String(length=255), nullable=True))
    op.add_column('orders', sa.Column('order_product_name', sa.String(length=255), nullable=True))
    op.add_column('orders', sa.Column('order_product_price', sa.String(length=255), nullable=True))
    op.add_column('orders', sa.Column('order_product_discount', sa.String(length=255), nullable=True))
    op.add_column('orders', sa.Column('order_product_quantity', sa.String(length=255), nullable=True))
    op.add_column('orders', sa.Column('order_total_price', sa.String(length=255), nullable=True))
    op.add_column('orders', sa.Column('order_product_image', sa.String(length=255), nullable=True))
    op.add_column('orders', sa.Column('order_product_description', sa.String(length=255), nullable=True))
    op.add_column('orders', sa.Column('order_product_is_available', sa.Boolean(), nullable=True))
    op.add_column('orders', sa.Column('order_date', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_orders_item_unique_id'), 'orders', ['item_unique_id'], unique=True)
    op.create_index(op.f('ix_orders_order_id'), 'orders', ['order_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_orders_order_id'), table_name='orders')
    op.drop_index(op.f('ix_orders_item_unique_id'), table_name='orders')
    op.drop_column('orders', 'order_date')
    op.drop_column('orders', 'order_product_is_available')
    op.drop_column('orders', 'order_product_description')
    op.drop_column('orders', 'order_product_image')
    op.drop_column('orders', 'order_total_price')
    op.drop_column('orders', 'order_product_quantity')
    op.drop_column('orders', 'order_product_discount')
    op.drop_column('orders', 'order_product_price')
    op.drop_column('orders', 'order_product_name')
    op.drop_column('orders', 'item_unique_id')
    op.drop_column('orders', 'order_product_id')
    op.drop_column('orders', 'order_customer_id')
    op.drop_column('orders', 'order_vendor_id')
    op.drop_column('orders', 'order_id')
    # ### end Alembic commands ###