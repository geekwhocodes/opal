
from typing import List, Union
import uuid
from fastapi import Depends
from sqlalchemy import UUID, select
from sqlalchemy.ext.asyncio import AsyncSession
from geopy.distance import geodesic, Distance

from opalizer.api.events.models import Event
from opalizer.api.events.schemas import EventSchemaIn
from opalizer.api.events.utils import event_in_perimeter, parse_utm_values
from opalizer.api.store.models import Store
from opalizer.api.tenants.models import Tenant
from opalizer.database import get_async_db, get_public_async_db
import opalizer.api.store.service as ss


async def create_event(session:AsyncSession, payload: EventSchemaIn, tenant: Tenant) -> Event:
        new_event = Event(**payload.dict())
        new_event.tenant_id = tenant.id
        session.add(new_event)
        await session.commit()
        await session.refresh(new_event)
        return new_event


async def process_event(payload: EventSchemaIn, tenant:Tenant, 
                        public_session:AsyncSession,
                        private_session:AsyncSession):
        try:
            stores:List[Store] = await ss.get_all(session=private_session)
            if event_in_perimeter(stores=stores, e=payload):
                new_event = Event(**payload.dict())
                new_event.__dict__.update(**parse_utm_values(payload.window_location_json.search))
                new_event.tenant_id = tenant.id
                private_session.add(new_event)
                await private_session.commit()
        except Exception as e:
              print(e)
              raise

                
                

