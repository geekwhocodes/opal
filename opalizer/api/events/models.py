import sqlalchemy as sa
from sqlalchemy.orm import relationship
from uuid import uuid4
from opalizer.api.store.models import Store
from opalizer.api.tenants.models import Tenant
from opalizer.database import Base


class Events(Base):
    __tablename__ = "events"
    # REGEXP_MATCHES('', '.*[&?]zzz=([^&]+).*')
    id = sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=uuid4(), nullable=False)
    latitude = sa.Column("latitude", sa.Float(), nullable=False)
    longitude = sa.Column("longitude", sa.Float(), nullable=False)
    accuracy = sa.Column("accuracy", sa.Float(), nullable=True)
    ip_addr = sa.Column("ip_addr", sa.String(64), nullable=True)
    ga_user_id = sa.Column("ga_user_id", sa.String(256), nullable= True)

    utm_medium = sa.Column("utm_medium", sa.String(512), nullable= True)
    utm_source = sa.Column("utm_source", sa.String(512), nullable= True)
    utm_campaign = sa.Column("utm_campaign", sa.String(512), nullable= True)
    utm_term = sa.Column("utm_term", sa.String(512), nullable= True)
    utm_content = sa.Column("utm_content", sa.String(512), nullable= True)

    window_location_json = sa.Column("window_location_json", sa.JSON(), nullable=True)
    browser_json = sa.Column("browser_json", sa.JSON(), nullable=True)
    address_json = sa.Column("address_json", sa.JSON(), nullable=True)

    tenant_id = sa.Column("tenant_id", sa.UUID(), sa.ForeignKey(Tenant.id), nullable=False)
    tenant = relationship(Tenant)

    store_id = sa.Column("store_id", sa.UUID(), sa.ForeignKey(Store.id), nullable=True)
    store = relationship(Store)

    created_at = sa.Column(
        sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()
    )
    updated_at = sa.Column(sa.TIMESTAMP(timezone=True), default=None, onupdate=sa.func.now())
    #created_date = sa.Column(sa.Date(), sa.Computed("date(created_at)"))

    # __table_args__ = {
    #     'postgresql_partition_by': 'RANGE(created_date)',
    # }