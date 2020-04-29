"""added new columns to images table

Revision ID: 2f1343520543
Revises: 18f95f69199b
Create Date: 2020-04-29 15:09:47.385787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f1343520543'
down_revision = '18f95f69199b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('original_filename', sa.Text(), nullable=False))
    op.add_column('images', sa.Column('version', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_images_original_filename'), 'images', ['original_filename'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_images_original_filename'), table_name='images')
    op.drop_column('images', 'version')
    op.drop_column('images', 'original_filename')
    # ### end Alembic commands ###