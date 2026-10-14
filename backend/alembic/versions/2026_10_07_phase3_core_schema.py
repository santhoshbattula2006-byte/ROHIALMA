"""phase3_core_schema

# ruff: noqa: E501

Revision ID: 0002_phase3_core_schema
Revises: 0001_initial_foundation
Create Date: 2026-10-07 01:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0002_phase3_core_schema'
down_revision: Union[str, None] = '0001_initial_foundation'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
        sa.Column('full_name', sa.String(length=100), nullable=True),
        sa.Column(
            'role',
            sa.Enum('FARMER', 'EXTENSION_OFFICER', 'ADMIN', name='userrole', native_enum=False),
            nullable=False,
        ),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_phone_number'), 'users', ['phone_number'], unique=True)

    # 2. locations
    op.create_table(
        'locations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('state', sa.String(length=100), nullable=False),
        sa.Column('district', sa.String(length=100), nullable=False),
        sa.Column('block', sa.String(length=100), nullable=False),
        sa.Column('village', sa.String(length=100), nullable=True),
        sa.Column('pincode', sa.String(length=10), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('state', 'district', 'block', 'village', name='uq_location_hierarchy'),
    )
    op.create_index(op.f('ix_locations_block'), 'locations', ['block'], unique=False)
    op.create_index(op.f('ix_locations_district'), 'locations', ['district'], unique=False)
    op.create_index(op.f('ix_locations_state'), 'locations', ['state'], unique=False)
    op.create_index(op.f('ix_locations_village'), 'locations', ['village'], unique=False)
    op.create_index(
        'ix_location_hierarchy', 'locations', ['state', 'district', 'block'], unique=False
    )

    # 3. crops
    op.create_table(
        'crops',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('scientific_name', sa.String(length=150), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('season', sa.String(length=50), nullable=True),
        sa.Column('min_duration_days', sa.Integer(), nullable=True),
        sa.Column('max_duration_days', sa.Integer(), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_crops_name'), 'crops', ['name'], unique=True)

    # 4. farmer_profiles
    op.create_table(
        'farmer_profiles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=True),
        sa.Column('primary_crop_id', sa.Integer(), nullable=True),
        sa.Column('land_area_acres', sa.Float(), nullable=True),
        sa.Column('preferred_language', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['primary_crop_id'], ['crops.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
    )
    op.create_index(
        op.f('ix_farmer_profiles_location_id'), 'farmer_profiles', ['location_id'], unique=False
    )
    op.create_index(
        op.f('ix_farmer_profiles_primary_crop_id'),
        'farmer_profiles',
        ['primary_crop_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_farmer_profiles_user_id'), 'farmer_profiles', ['user_id'], unique=True
    )

    # 5. crop_rules
    op.create_table(
        'crop_rules',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('crop_id', sa.Integer(), nullable=False),
        sa.Column('rule_name', sa.String(length=100), nullable=False),
        sa.Column('min_ph', sa.Float(), nullable=True),
        sa.Column('max_ph', sa.Float(), nullable=True),
        sa.Column('min_n', sa.Float(), nullable=True),
        sa.Column('max_n', sa.Float(), nullable=True),
        sa.Column('min_p', sa.Float(), nullable=True),
        sa.Column('max_p', sa.Float(), nullable=True),
        sa.Column('min_k', sa.Float(), nullable=True),
        sa.Column('max_k', sa.Float(), nullable=True),
        sa.Column('min_rainfall_mm', sa.Float(), nullable=True),
        sa.Column('max_rainfall_mm', sa.Float(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='1'),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['crop_id'], ['crops.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_crop_rules_crop_id'), 'crop_rules', ['crop_id'], unique=False)

    # 6. soil_profiles
    op.create_table(
        'soil_profiles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('farmer_profile_id', sa.Integer(), nullable=True),
        sa.Column('location_id', sa.Integer(), nullable=True),
        sa.Column('sample_date', sa.Date(), nullable=True),
        sa.Column('n_value', sa.Float(), nullable=True),
        sa.Column(
            'n_source',
            sa.Enum(
                'FARMER', 'BLOCK_DEFAULT', 'LAB_TEST', 'ESTIMATED', name='soilsource', native_enum=False
            ),
            nullable=True,
        ),
        sa.Column('p_value', sa.Float(), nullable=True),
        sa.Column(
            'p_source',
            sa.Enum(
                'FARMER', 'BLOCK_DEFAULT', 'LAB_TEST', 'ESTIMATED', name='soilsource', native_enum=False
            ),
            nullable=True,
        ),
        sa.Column('k_value', sa.Float(), nullable=True),
        sa.Column(
            'k_source',
            sa.Enum(
                'FARMER', 'BLOCK_DEFAULT', 'LAB_TEST', 'ESTIMATED', name='soilsource', native_enum=False
            ),
            nullable=True,
        ),
        sa.Column('ph_value', sa.Float(), nullable=True),
        sa.Column(
            'ph_source',
            sa.Enum(
                'FARMER', 'BLOCK_DEFAULT', 'LAB_TEST', 'ESTIMATED', name='soilsource', native_enum=False
            ),
            nullable=True,
        ),
        sa.Column('oc_value', sa.Float(), nullable=True),
        sa.Column(
            'oc_source',
            sa.Enum(
                'FARMER', 'BLOCK_DEFAULT', 'LAB_TEST', 'ESTIMATED', name='soilsource', native_enum=False
            ),
            nullable=True,
        ),
        sa.Column('ec_value', sa.Float(), nullable=True),
        sa.Column(
            'ec_source',
            sa.Enum(
                'FARMER', 'BLOCK_DEFAULT', 'LAB_TEST', 'ESTIMATED', name='soilsource', native_enum=False
            ),
            nullable=True,
        ),
        sa.Column('fe_value', sa.Float(), nullable=True),
        sa.Column(
            'fe_source',
            sa.Enum(
                'FARMER', 'BLOCK_DEFAULT', 'LAB_TEST', 'ESTIMATED', name='soilsource', native_enum=False
            ),
            nullable=True,
        ),
        sa.Column('zn_value', sa.Float(), nullable=True),
        sa.Column(
            'zn_source',
            sa.Enum(
                'FARMER', 'BLOCK_DEFAULT', 'LAB_TEST', 'ESTIMATED', name='soilsource', native_enum=False
            ),
            nullable=True,
        ),
        sa.Column('b_value', sa.Float(), nullable=True),
        sa.Column(
            'b_source',
            sa.Enum(
                'FARMER', 'BLOCK_DEFAULT', 'LAB_TEST', 'ESTIMATED', name='soilsource', native_enum=False
            ),
            nullable=True,
        ),
        sa.Column('s_value', sa.Float(), nullable=True),
        sa.Column(
            's_source',
            sa.Enum(
                'FARMER', 'BLOCK_DEFAULT', 'LAB_TEST', 'ESTIMATED', name='soilsource', native_enum=False
            ),
            nullable=True,
        ),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['farmer_profile_id'], ['farmer_profiles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_soil_profiles_farmer_profile_id'), 'soil_profiles', ['farmer_profile_id'], unique=False
    )
    op.create_index(
        op.f('ix_soil_profiles_location_id'), 'soil_profiles', ['location_id'], unique=False
    )

    # 7. soil_default_dataset_records
    op.create_table(
        'soil_default_dataset_records',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('state', sa.String(length=100), nullable=False),
        sa.Column('district', sa.String(length=100), nullable=False),
        sa.Column('block', sa.String(length=100), nullable=False),
        sa.Column('cycle', sa.String(length=50), nullable=False),
        sa.Column(
            'scheme_source',
            sa.String(length=150),
            nullable=False,
            server_default='Soil Health Card Scheme',
        ),
        sa.Column('n_category', sa.String(length=20), nullable=True),
        sa.Column('p_category', sa.String(length=20), nullable=True),
        sa.Column('k_category', sa.String(length=20), nullable=True),
        sa.Column('oc_category', sa.String(length=20), nullable=True),
        sa.Column('ph_category', sa.String(length=20), nullable=True),
        sa.Column('ec_category', sa.String(length=20), nullable=True),
        sa.Column('n_count_low', sa.Integer(), nullable=True),
        sa.Column('n_count_medium', sa.Integer(), nullable=True),
        sa.Column('n_count_high', sa.Integer(), nullable=True),
        sa.Column('p_count_low', sa.Integer(), nullable=True),
        sa.Column('p_count_medium', sa.Integer(), nullable=True),
        sa.Column('p_count_high', sa.Integer(), nullable=True),
        sa.Column('k_count_low', sa.Integer(), nullable=True),
        sa.Column('k_count_medium', sa.Integer(), nullable=True),
        sa.Column('k_count_high', sa.Integer(), nullable=True),
        sa.Column('oc_count_low', sa.Integer(), nullable=True),
        sa.Column('oc_count_medium', sa.Integer(), nullable=True),
        sa.Column('oc_count_high', sa.Integer(), nullable=True),
        sa.Column('ph_count_acidic', sa.Integer(), nullable=True),
        sa.Column('ph_count_neutral', sa.Integer(), nullable=True),
        sa.Column('ph_count_alkaline', sa.Integer(), nullable=True),
        sa.Column('total_samples_tested', sa.Integer(), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('state', 'district', 'block', 'cycle', name='uq_soil_block_cycle'),
    )
    op.create_index(
        op.f('ix_soil_default_dataset_records_block'),
        'soil_default_dataset_records',
        ['block'],
        unique=False,
    )
    op.create_index(
        op.f('ix_soil_default_dataset_records_cycle'),
        'soil_default_dataset_records',
        ['cycle'],
        unique=False,
    )
    op.create_index(
        op.f('ix_soil_default_dataset_records_district'),
        'soil_default_dataset_records',
        ['district'],
        unique=False,
    )
    op.create_index(
        op.f('ix_soil_default_dataset_records_state'),
        'soil_default_dataset_records',
        ['state'],
        unique=False,
    )
    op.create_index(
        'ix_soil_default_location',
        'soil_default_dataset_records',
        ['state', 'district', 'block'],
        unique=False,
    )

    # 8. weather_cache
    op.create_table(
        'weather_cache',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('forecast_date', sa.Date(), nullable=False),
        sa.Column('temperature_min', sa.Float(), nullable=True),
        sa.Column('temperature_max', sa.Float(), nullable=True),
        sa.Column('humidity', sa.Float(), nullable=True),
        sa.Column('rainfall_mm', sa.Float(), nullable=True),
        sa.Column('wind_speed_kmh', sa.Float(), nullable=True),
        sa.Column('weather_condition', sa.String(length=50), nullable=True),
        sa.Column('raw_response_json', sa.JSON(), nullable=True),
        sa.Column('fetched_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_weather_cache_forecast_date'), 'weather_cache', ['forecast_date'], unique=False
    )
    op.create_index(
        op.f('ix_weather_cache_location_id'), 'weather_cache', ['location_id'], unique=False
    )
    op.create_index(
        'ix_weather_coords_date',
        'weather_cache',
        ['latitude', 'longitude', 'forecast_date'],
        unique=False,
    )

    # 9. recommendations
    op.create_table(
        'recommendations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('farmer_profile_id', sa.Integer(), nullable=False),
        sa.Column('crop_id', sa.Integer(), nullable=True),
        sa.Column('recommendation_type', sa.String(length=50), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('input_snapshot_json', sa.JSON(), nullable=True),
        sa.Column('details_json', sa.JSON(), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['crop_id'], ['crops.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['farmer_profile_id'], ['farmer_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_recommendations_crop_id'), 'recommendations', ['crop_id'], unique=False
    )
    op.create_index(
        op.f('ix_recommendations_farmer_profile_id'),
        'recommendations',
        ['farmer_profile_id'],
        unique=False,
    )
    op.create_index(
        op.f('ix_recommendations_recommendation_type'),
        'recommendations',
        ['recommendation_type'],
        unique=False,
    )

    # 10. chat_sessions
    op.create_table(
        'chat_sessions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('context_snapshot_json', sa.JSON(), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_chat_sessions_user_id'), 'chat_sessions', ['user_id'], unique=False
    )

    # 11. chat_messages
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('sender', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('metadata_json', sa.JSON(), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['session_id'], ['chat_sessions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_chat_messages_session_id'), 'chat_messages', ['session_id'], unique=False
    )


def downgrade() -> None:
    op.drop_table('chat_messages')
    op.drop_table('chat_sessions')
    op.drop_table('recommendations')
    op.drop_table('weather_cache')
    op.drop_table('soil_default_dataset_records')
    op.drop_table('soil_profiles')
    op.drop_table('crop_rules')
    op.drop_table('farmer_profiles')
    op.drop_table('crops')
    op.drop_table('locations')
    op.drop_table('users')
