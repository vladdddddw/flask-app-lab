"""Add Simulation category and game

Revision ID: 49d113d1ed6f
Revises: 50a4573412d8
Create Date: 2025-11-07 ...
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Float, Boolean


revision = '49d113d1ed6f'
down_revision = '50a4573412d8'
branch_labels = None
depends_on = None


def upgrade():

    categories_table = table('categories',
                             column('id', Integer),
                             column('name', String)
                             )

    products_table = table('products',
                           column('name', String),
                           column('price', Float),
                           # column('active', Boolean),
                           column('category_id', Integer)
                           )


    op.bulk_insert(categories_table, [
        {'name': 'Simulators'}
    ])


    op.execute("""
        INSERT INTO products (name, price, category_id)
        SELECT 'The Sims 4', 0.0, id FROM categories WHERE name = 'Simulators'
    """)


def downgrade():

    op.execute("DELETE FROM products WHERE name = 'The Sims 4'")
    op.execute("DELETE FROM categories WHERE name = 'Simulators'")