"""removed unique constraint from original_filename column

Revision ID: 1981d79cb05b
Revises: 8b6f999a7105
Create Date: 2020-04-29 17:05:32.390722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1981d79cb05b'
down_revision = '8b6f999a7105'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_images_original_filename', table_name='images')
    op.create_index(op.f('ix_images_original_filename'), 'images', ['original_filename'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_images_original_filename'), table_name='images')
    op.create_index('ix_images_original_filename', 'images', ['original_filename'], unique=True)
    # ### end Alembic commands ###
