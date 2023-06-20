"""init

Revision ID: 192b914e7f19
Revises: 
Create Date: 2023-06-16 02:27:05.002952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '192b914e7f19'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    create_tenant = """
        CREATE TABLE IF NOT EXISTS public.tenants (
        id UUID NOT NULL, 
        name VARCHAR(256) NOT NULL, 
        schema VARCHAR(64) NOT NULL, 
        slug VARCHAR(32) NOT NULL, 
        api_key VARCHAR(256), 
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
        updated_at TIMESTAMP WITH TIME ZONE, 
        CONSTRAINT tenants_pkey PRIMARY KEY (id), 
        CONSTRAINT tenants_schema_key UNIQUE (schema), 
        CONSTRAINT tenants_slug_key UNIQUE (slug)
        )
    """

    create_geomap = """
        CREATE TABLE IF NOT EXISTS public.geomaps
        (
            id uuid NOT NULL,
            geohash character varying(256) COLLATE pg_catalog."default" NOT NULL,
            latitude double precision NOT NULL,
            longitude double precision NOT NULL,
            address json NOT NULL,
            created_at timestamp with time zone NOT NULL DEFAULT now(),
            updated_at timestamp with time zone,
            CONSTRAINT geomap_pkey PRIMARY KEY (id)
        )
    """

    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(create_tenant)

    api_key_index = """ CREATE UNIQUE INDEX IF NOT EXISTS public_tenants_api_key_idx ON public.tenants (api_key) """
    
    op.execute(api_key_index)

    name_index = """ CREATE UNIQUE INDEX IF NOT EXISTS public_tenants_name_idx ON public.tenants (name) """

    op.execute(name_index)

    op.execute(create_geomap)

    geohash_index = """ CREATE UNIQUE INDEX IF NOT EXISTS public_geomaps_geohash_idx
                        ON public.geomaps USING btree
                        (geohash COLLATE pg_catalog."default" ASC NULLS LAST)
                        TABLESPACE pg_default; 
    """

    op.execute(geohash_index)
    
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('alembic_version',
    # sa.Column('version_num', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
    # sa.PrimaryKeyConstraint('version_num', name='alembic_version_pkc')
    # )
    # op.drop_index(op.f('public_tenants_name_idx'), table_name='tenants', schema='public')
    # op.drop_index(op.f('public_tenants_api_key_idx'), table_name='tenants', schema='public')
    # op.drop_table('tenants', schema='public')
    # ### end Alembic commands ###
    pass
