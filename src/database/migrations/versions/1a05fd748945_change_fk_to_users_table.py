"""Change FK to users table

Revision ID: 1a05fd748945
Revises: 956f5dc43293
Create Date: 2023-12-01 16:47:07.526446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a05fd748945'
down_revision: Union[str, None] = '956f5dc43293'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auth_sessions', sa.Column('username', sa.String(length=50), nullable=True))
    op.create_foreign_key(None, 'auth_sessions', 'users', ['username'], ['username'])
    op.drop_column('auth_sessions', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auth_sessions', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'auth_sessions', type_='foreignkey')
    op.drop_column('auth_sessions', 'username')
    # ### end Alembic commands ###
