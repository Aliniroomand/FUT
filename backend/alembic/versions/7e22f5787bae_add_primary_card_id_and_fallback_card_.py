"""Add primary_card_id and fallback_card_id, remove player_id from card_ranges

Revision ID: 7e22f5787bae
Revises: a135a88c8674
Create Date: 2025-07-23 09:11:14.458268
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e22f5787bae'
down_revision: Union[str, Sequence[str], None] = 'a135a88c8674'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---- ۱) حذف player_id با batch_alter_table ----
    with op.batch_alter_table('card_ranges', schema=None) as batch_op:
        batch_op.drop_column('player_id')

    # ---- ۲) اضافه کردن primary_card_id ----
    op.add_column(
        'card_ranges',
        sa.Column('primary_card_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_card_ranges_primary_card_id_players',
        source_table='card_ranges',
        referent_table='players',
        local_cols=['primary_card_id'],
        remote_cols=['id']
    )

    # ---- ۳) اضافه کردن fallback_card_id ----
    op.add_column(
        'card_ranges',
        sa.Column('fallback_card_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_card_ranges_fallback_card_id_players',
        source_table='card_ranges',
        referent_table='players',
        local_cols=['fallback_card_id'],
        remote_cols=['id']
    )

    # ---- ۴) اصلاح جدول players ----
    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bid', sa.Float(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('buyNow', sa.Float(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('CardPrice', sa.Float(), nullable=False, server_default='0'))
        batch_op.drop_column('name')


def downgrade() -> None:
    # بازگردانی تغییرات players
    with op.batch_alter_table('players', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(), nullable=False, server_default=''))
        batch_op.drop_column('CardPrice')
        batch_op.drop_column('buyNow')
        batch_op.drop_column('bid')

    # حذف fallback_card_id و primary_card_id
    op.drop_constraint('fk_card_ranges_fallback_card_id_players', 'card_ranges', type_='foreignkey')
    op.drop_column('card_ranges', 'fallback_card_id')

    op.drop_constraint('fk_card_ranges_primary_card_id_players', 'card_ranges', type_='foreignkey')
    op.drop_column('card_ranges', 'primary_card_id')

    # افزودن مجدد player_id
    with op.batch_alter_table('card_ranges', schema=None) as batch_op:
        batch_op.add_column(sa.Column('player_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key(
            'fk_card_ranges_player_id_players',
            'players',
            ['player_id'],
            ['id']
        )
