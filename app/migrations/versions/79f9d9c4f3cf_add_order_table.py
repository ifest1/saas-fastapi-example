"""Add order table

Revision ID: 79f9d9c4f3cf
Revises: 26619122d81d
Create Date: 2022-06-21 16:49:01.352330

"""
from alembic import op
import sqlalchemy as sa
import ormar


# revision identifiers, used by Alembic.
revision = "79f9d9c4f3cf"
down_revision = "26619122d81d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "payments",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("method", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "orders",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=False),
        sa.Column(
            "payment", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=True
        ),
        sa.Column(
            "user_id", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=True
        ),
        sa.Column("total", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["payment"], ["payments.id"], name="fk_orders_payments_id_payment"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="fk_orders_users_id_user_id"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "orders_items",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("item", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=True),
        sa.Column(
            "order", ormar.fields.sqlalchemy_uuid.CHAR(32), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["item"],
            ["items.id"],
            name="fk_orders_items_items_item_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["order"],
            ["orders.id"],
            name="fk_orders_items_orders_order_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("orders_items")
    op.drop_table("orders")
    op.drop_table("payments")
    # ### end Alembic commands ###