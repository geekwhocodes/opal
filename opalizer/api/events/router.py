import logging
from typing import List, Sequence
import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response, Security
from fastapi import status as HttpStatus
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from pydantic import parse_obj_as
from opalizer.api.tenants.models import Tenant

from opalizer.auth.key import validate_api_key
from opalizer.core.rate_limiter import limiter
from opalizer.schemas import SingleResponse, CollectionResponse, RequestStatus
from opalizer.api.events.schemas import EventSchemaIn
from opalizer.api.events.models import Event
import opalizer.api.events.service as es
from opalizer.database import get_async_db, get_tanant, get_public_async_db

logger = logging.getLogger("opalizer.main")

events_router = APIRouter(
    prefix="/v1/events",
    dependencies=list([Security(validate_api_key)])
)


@events_router.post("/", status_code=HttpStatus.HTTP_200_OK)
@limiter.limit("50/second")
async def create_event(request:Request, response:Response, 
                     payload: EventSchemaIn,
                     background_tasks: BackgroundTasks,
                     tenant:Tenant=Depends(get_tanant),
                     public_session=Depends(get_public_async_db),
                     private_session=Depends(get_async_db)) -> SingleResponse:
    try:
        background_tasks.add_task(es.process_event, payload, tenant, public_session, private_session)
        background_tasks.add_task(es.process_impression, payload, tenant)
        return SingleResponse(status=RequestStatus.success, value=None)
    except Exception as e:
        return SingleResponse(status=RequestStatus.error, value=None, error="Internal error")
    
