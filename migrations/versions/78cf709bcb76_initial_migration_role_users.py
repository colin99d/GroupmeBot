"""initial migration - Role Users

Revision ID: 78cf709bcb76
Revises:
Create Date: 2021-11-25 20:51:48.999556

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "78cf709bcb76"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "post",
        sa.Column("pk", sa.Integer(), nullable=False),
        sa.Column("avatar_url", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.String(length=350), nullable=True),
        sa.Column("group_id", sa.String(length=350), nullable=True),
        sa.Column("id", sa.String(length=350), nullable=True),
        sa.Column("name", sa.String(length=350), nullable=True),
        sa.Column("sender_id", sa.String(length=350), nullable=True),
        sa.Column("sender_type", sa.String(length=350), nullable=True),
        sa.Column("source_guid", sa.String(length=350), nullable=True),
        sa.Column("system", sa.Boolean(), nullable=True),
        sa.Column("text", sa.String(length=10000), nullable=True),
        sa.Column("user_id", sa.String(length=350), nullable=True),
        sa.PrimaryKeyConstraint("pk"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("post")
    # ### end Alembic commands ###
