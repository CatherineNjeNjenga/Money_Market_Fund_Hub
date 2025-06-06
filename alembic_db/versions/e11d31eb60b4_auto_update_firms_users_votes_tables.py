"""auto update firms, users & votes tables

Revision ID: e11d31eb60b4
Revises: 657b81fa301a
Create Date: 2025-04-22 09:43:47.618797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e11d31eb60b4'
down_revision: Union[str, None] = '657b81fa301a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('firms', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
    # op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_column('users', 'created_at')
    # op.drop_column('firms', 'created_at')
    # ### end Alembic commands ###
