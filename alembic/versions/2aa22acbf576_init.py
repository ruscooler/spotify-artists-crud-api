"""init

Revision ID: 2aa22acbf576
Revises: 
Create Date: 2023-03-09 16:26:12.722147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2aa22acbf576'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('spotify_id', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('followers', sa.Integer(), nullable=True),
    sa.Column('popularity', sa.Integer(), nullable=True),
    sa.Column('genres', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('is_api_managed', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_artist_id'), 'artist', ['id'], unique=True)
    op.create_index(op.f('ix_artist_spotify_id'), 'artist', ['spotify_id'], unique=True)
    op.create_table('background_task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_name', sa.String(), nullable=False),
    sa.Column('is_success', sa.Boolean(), nullable=True),
    sa.Column('data', sa.String(), nullable=True),
    sa.Column('last_finished_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'task_name')
    )
    op.create_index(op.f('ix_background_task_id'), 'background_task', ['id'], unique=False)
    op.create_index(op.f('ix_background_task_task_name'), 'background_task', ['task_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_background_task_task_name'), table_name='background_task')
    op.drop_index(op.f('ix_background_task_id'), table_name='background_task')
    op.drop_table('background_task')
    op.drop_index(op.f('ix_artist_spotify_id'), table_name='artist')
    op.drop_index(op.f('ix_artist_id'), table_name='artist')
    op.drop_table('artist')
    # ### end Alembic commands ###
