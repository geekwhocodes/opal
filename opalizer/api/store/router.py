from typing import List, Sequence
import uuid
from fastapi import APIRouter, Depends, Request, Response, Security
from fastapi import status as HttpStatus
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from pydantic import parse_obj_as
from opalizer.api.tenants.models import Tenant

from opalizer.auth.key import validate_api_key
from opalizer.core.rate_limiter import limiter
from opalizer.schemas import SingleResponse, CollectionResponse, RequestStatus
from opalizer.api.store.schemas import StoreSchema
from opalizer.api.store.models import Store
import opalizer.api.store.service as ss
from opalizer.database import get_async_db, get_tanant


stores_router = APIRouter(
    prefix="/v1/stores",
    dependencies=list([Security(validate_api_key)])
)


@stores_router.get("/{id}", status_code=HttpStatus.HTTP_200_OK)
@limiter.limit("10/second")
async def get_store(request:Request, response:Response, 
                    id:uuid.UUID,
                    db:Session=Depends(get_async_db)):
    try:
        store = await ss.get_by_id(session=db, id=id)
        if store:
            return SingleResponse(status=RequestStatus.success, value=StoreSchema.from_orm(store))
        return SingleResponse(status=RequestStatus.success, value=None)
    except Exception as e:
        return SingleResponse(status=RequestStatus.error, value=None, error="Internal error")

@stores_router.get("/", status_code=HttpStatus.HTTP_200_OK)
async def get_all_stores(request:Request, response:Response,
                          db:Session=Depends(get_async_db)):
    try:
        stores = await ss.get_all(db)
        return CollectionResponse(status=RequestStatus.success, value=parse_obj_as(List[StoreSchema], stores))
    except Exception as e:
        return SingleResponse(status=RequestStatus.error, value=None, error="Internal error")

@stores_router.post("/", status_code=HttpStatus.HTTP_200_OK)
@limiter.limit("10/second")
async def create_store(request:Request, response:Response, 
                     payload: StoreSchema,
                     tenant:Tenant=Depends(get_tanant),
                     db:Session=Depends(get_async_db)) -> SingleResponse:
    try:
        store = await ss.get_by_name(session=db, name=payload.name)
        if store:
            response.status_code = HttpStatus.HTTP_409_CONFLICT
            return SingleResponse(status=RequestStatus.error, 
                                  value=None,
                                  error=f"Store name '{payload.name}' is not available. Please use different store name.")
        new_store = await ss.create_store(db,payload, tenant)
        return SingleResponse(status=RequestStatus.success, value=StoreSchema.from_orm(new_store))
    except Exception as e:
        return SingleResponse(status=RequestStatus.error, value=None, error="Internal error")
    
