"""initial

Revision ID: 95b30a96dbec
Revises: 
Create Date: 2022-01-05 08:40:11.975289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95b30a96dbec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('triebwagen',
    sa.Column('fahrgestellnummer', sa.String(length=64), nullable=False),
    sa.Column('spurweite', sa.Integer(), nullable=True),
    sa.Column('zugkraft', sa.DECIMAL(), nullable=True),
    sa.Column('zug_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['zug_id'], ['zug.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('fahrgestellnummer')
    )
    op.create_index(op.f('ix_triebwagen_spurweite'), 'triebwagen', ['spurweite'], unique=False)
    op.create_table('users',
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_table('zug',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('triebwagen', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['triebwagen'], ['triebwagen.fahrgestellnummer'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('maintenance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('zug_id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('duration', sa.DECIMAL(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['zug_id'], ['zug.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('personenwaggon',
    sa.Column('fahrgestellnummer', sa.String(length=64), nullable=False),
    sa.Column('spurweite', sa.Integer(), nullable=True),
    sa.Column('sitzanzahl', sa.Integer(), nullable=True),
    sa.Column('maxGewicht', sa.DECIMAL(), nullable=True),
    sa.Column('zug_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['zug_id'], ['zug.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('fahrgestellnummer')
    )
    op.create_index(op.f('ix_personenwaggon_spurweite'), 'personenwaggon', ['spurweite'], unique=False)
    op.create_table('maintenance_employee_association',
    sa.Column('maintenance_id', sa.Integer(), nullable=True),
    sa.Column('employee_id', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['users.email'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['maintenance_id'], ['maintenance.id'], ondelete='CASCADE')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('maintenance_employee_association')
    op.drop_index(op.f('ix_personenwaggon_spurweite'), table_name='personenwaggon')
    op.drop_table('personenwaggon')
    op.drop_table('maintenance')
    op.drop_table('zug')
    op.drop_table('users')
    op.drop_index(op.f('ix_triebwagen_spurweite'), table_name='triebwagen')
    op.drop_table('triebwagen')
    # ### end Alembic commands ###