"""empty message

Revision ID: 5435266e3929
Revises: 
Create Date: 2022-04-20 23:38:15.614898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5435266e3929'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.String(length=255), nullable=True),
    sa.Column('customer_name', sa.String(length=255), nullable=True),
    sa.Column('customer_email', sa.String(length=255), nullable=True),
    sa.Column('customer_password', sa.String(length=255), nullable=True),
    sa.Column('customer_address', sa.Text(length=2000), nullable=True),
    sa.Column('customer_cards', sa.Text(length=2000), nullable=True),
    sa.Column('customer_push_notofication_token', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customers_customer_email'), 'customers', ['customer_email'], unique=True)
    op.create_index(op.f('ix_customers_customer_id'), 'customers', ['customer_id'], unique=True)
    op.create_index(op.f('ix_customers_customer_name'), 'customers', ['customer_name'], unique=True)
    op.create_index(op.f('ix_customers_customer_password'), 'customers', ['customer_password'], unique=True)
    op.create_index(op.f('ix_customers_customer_push_notofication_token'), 'customers', ['customer_push_notofication_token'], unique=True)
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.String(length=255), nullable=True),
    sa.Column('order_user_id', sa.String(length=255), nullable=True),
    sa.Column('order_vendor_id', sa.String(length=255), nullable=True),
    sa.Column('order_product_id', sa.String(length=255), nullable=True),
    sa.Column('order_product_name', sa.String(length=255), nullable=True),
    sa.Column('order_product_price', sa.String(length=255), nullable=True),
    sa.Column('order_product_discount', sa.String(length=255), nullable=True),
    sa.Column('order_product_quantity', sa.String(length=255), nullable=True),
    sa.Column('order_product_total_price', sa.String(length=255), nullable=True),
    sa.Column('order_product_image', sa.String(length=255), nullable=True),
    sa.Column('order_product_description', sa.String(length=255), nullable=True),
    sa.Column('order_product_is_available', sa.Boolean(), nullable=True),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_order_id'), 'orders', ['order_id'], unique=True)
    op.create_index(op.f('ix_orders_order_product_description'), 'orders', ['order_product_description'], unique=True)
    op.create_index(op.f('ix_orders_order_product_discount'), 'orders', ['order_product_discount'], unique=True)
    op.create_index(op.f('ix_orders_order_product_id'), 'orders', ['order_product_id'], unique=True)
    op.create_index(op.f('ix_orders_order_product_image'), 'orders', ['order_product_image'], unique=True)
    op.create_index(op.f('ix_orders_order_product_name'), 'orders', ['order_product_name'], unique=True)
    op.create_index(op.f('ix_orders_order_product_price'), 'orders', ['order_product_price'], unique=True)
    op.create_index(op.f('ix_orders_order_product_quantity'), 'orders', ['order_product_quantity'], unique=True)
    op.create_index(op.f('ix_orders_order_product_total_price'), 'orders', ['order_product_total_price'], unique=True)
    op.create_index(op.f('ix_orders_order_user_id'), 'orders', ['order_user_id'], unique=True)
    op.create_index(op.f('ix_orders_order_vendor_id'), 'orders', ['order_vendor_id'], unique=True)
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.String(length=255), nullable=True),
    sa.Column('product_name', sa.String(length=255), nullable=True),
    sa.Column('product_description', sa.String(length=255), nullable=True),
    sa.Column('product_price', sa.String(length=255), nullable=True),
    sa.Column('product_image', sa.String(length=255), nullable=True),
    sa.Column('product_discount', sa.Integer(), nullable=True),
    sa.Column('product_is_available', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_product_description'), 'products', ['product_description'], unique=True)
    op.create_index(op.f('ix_products_product_discount'), 'products', ['product_discount'], unique=True)
    op.create_index(op.f('ix_products_product_id'), 'products', ['product_id'], unique=True)
    op.create_index(op.f('ix_products_product_image'), 'products', ['product_image'], unique=True)
    op.create_index(op.f('ix_products_product_name'), 'products', ['product_name'], unique=True)
    op.create_index(op.f('ix_products_product_price'), 'products', ['product_price'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.String(length=255), nullable=True),
    sa.Column('admin_name', sa.String(length=255), nullable=True),
    sa.Column('admin_email', sa.String(length=255), nullable=True),
    sa.Column('admin_password', sa.String(length=255), nullable=True),
    sa.Column('admin_push_notofication_token', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_admin_email'), 'users', ['admin_email'], unique=True)
    op.create_index(op.f('ix_users_admin_id'), 'users', ['admin_id'], unique=True)
    op.create_index(op.f('ix_users_admin_name'), 'users', ['admin_name'], unique=True)
    op.create_index(op.f('ix_users_admin_password'), 'users', ['admin_password'], unique=True)
    op.create_index(op.f('ix_users_admin_push_notofication_token'), 'users', ['admin_push_notofication_token'], unique=True)
    op.create_table('vendors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vendor_id', sa.String(length=255), nullable=True),
    sa.Column('vendor_name', sa.String(length=255), nullable=True),
    sa.Column('vendor_email', sa.String(length=255), nullable=True),
    sa.Column('vendor_password', sa.String(length=255), nullable=True),
    sa.Column('vendor_push_notofication_token', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vendors_vendor_email'), 'vendors', ['vendor_email'], unique=True)
    op.create_index(op.f('ix_vendors_vendor_id'), 'vendors', ['vendor_id'], unique=True)
    op.create_index(op.f('ix_vendors_vendor_name'), 'vendors', ['vendor_name'], unique=True)
    op.create_index(op.f('ix_vendors_vendor_password'), 'vendors', ['vendor_password'], unique=True)
    op.create_index(op.f('ix_vendors_vendor_push_notofication_token'), 'vendors', ['vendor_push_notofication_token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_vendors_vendor_push_notofication_token'), table_name='vendors')
    op.drop_index(op.f('ix_vendors_vendor_password'), table_name='vendors')
    op.drop_index(op.f('ix_vendors_vendor_name'), table_name='vendors')
    op.drop_index(op.f('ix_vendors_vendor_id'), table_name='vendors')
    op.drop_index(op.f('ix_vendors_vendor_email'), table_name='vendors')
    op.drop_table('vendors')
    op.drop_index(op.f('ix_users_admin_push_notofication_token'), table_name='users')
    op.drop_index(op.f('ix_users_admin_password'), table_name='users')
    op.drop_index(op.f('ix_users_admin_name'), table_name='users')
    op.drop_index(op.f('ix_users_admin_id'), table_name='users')
    op.drop_index(op.f('ix_users_admin_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_products_product_price'), table_name='products')
    op.drop_index(op.f('ix_products_product_name'), table_name='products')
    op.drop_index(op.f('ix_products_product_image'), table_name='products')
    op.drop_index(op.f('ix_products_product_id'), table_name='products')
    op.drop_index(op.f('ix_products_product_discount'), table_name='products')
    op.drop_index(op.f('ix_products_product_description'), table_name='products')
    op.drop_table('products')
    op.drop_index(op.f('ix_orders_order_vendor_id'), table_name='orders')
    op.drop_index(op.f('ix_orders_order_user_id'), table_name='orders')
    op.drop_index(op.f('ix_orders_order_product_total_price'), table_name='orders')
    op.drop_index(op.f('ix_orders_order_product_quantity'), table_name='orders')
    op.drop_index(op.f('ix_orders_order_product_price'), table_name='orders')
    op.drop_index(op.f('ix_orders_order_product_name'), table_name='orders')
    op.drop_index(op.f('ix_orders_order_product_image'), table_name='orders')
    op.drop_index(op.f('ix_orders_order_product_id'), table_name='orders')
    op.drop_index(op.f('ix_orders_order_product_discount'), table_name='orders')
    op.drop_index(op.f('ix_orders_order_product_description'), table_name='orders')
    op.drop_index(op.f('ix_orders_order_id'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_customers_customer_push_notofication_token'), table_name='customers')
    op.drop_index(op.f('ix_customers_customer_password'), table_name='customers')
    op.drop_index(op.f('ix_customers_customer_name'), table_name='customers')
    op.drop_index(op.f('ix_customers_customer_id'), table_name='customers')
    op.drop_index(op.f('ix_customers_customer_email'), table_name='customers')
    op.drop_table('customers')
    # ### end Alembic commands ###
