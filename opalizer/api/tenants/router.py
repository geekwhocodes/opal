from typing import List
from fastapi import APIRouter, Depends, Request, Response
from fastapi import status as HttpStatus
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4, parse_obj_as
from opalizer.exceptions import TenantNameNotAvailableError, UpgradeAlembicHeadError
from opalizer.api.tenants.utils import slugify, generate_api_key, generate_tenant_schema_name
from opalizer.core.rate_limiter import limiter
from opalizer.schemas import SingleResponse, CollectionResponse, RequestStatus
from opalizer.api.tenants.schemas import TenantSchema
from opalizer.api.tenants.models import Tenant
from opalizer.api.tenants import service as ts
from opalizer.database import get_public_async_db


tenants_router = APIRouter(
    prefix="/v1/tenants"
)

# @tenants_router.get("/{id}", status_code=HttpStatus.HTTP_200_OK)
# async def get_tenant(request:Request, response:Response,
#                   id:UUID4,
#                   db:Session=Depends(get_public_async_db)):
#     try:
#         tenant = await ts.get_by_id(session=db, id=id)
#         return SingleResponse(status=RequestStatus.success, value=TenantSchema.from_orm(tenant))
#     except Exception as e:
#         return SingleResponse(status=RequestStatus.error, value=None, error="Internal error")

@tenants_router.get("/{name}", status_code=HttpStatus.HTTP_200_OK)
async def get_tenant(request:Request, response:Response,
                  name:str,
                  db:AsyncSession=Depends(get_public_async_db)):
    try:
        tenant = await ts.get_by_name(session=db, tenant_name=name)
        return SingleResponse(status=RequestStatus.success, value=TenantSchema.from_orm(tenant))
    except Exception as e:
        return SingleResponse(status=RequestStatus.error, value=None, error="Internal error")


@tenants_router.get("/", status_code=HttpStatus.HTTP_200_OK)
async def get_all_tenants(request:Request, response:Response,
                          db:AsyncSession=Depends(get_public_async_db)):
    try:
        tenants = await ts.get_all(db)
        return CollectionResponse(status=RequestStatus.success, value=parse_obj_as(List[TenantSchema], tenants))
    except Exception as e:
        return SingleResponse(status=RequestStatus.error, value=None, error="Internal error")

@tenants_router.post("/", status_code=HttpStatus.HTTP_200_OK)
@limiter.limit("10/second")
async def create_tenant(request:Request, response:Response, 
                     payload: TenantSchema, 
                     db:AsyncSession=Depends(get_public_async_db)) -> SingleResponse:
    try:
        tenant = await ts.get_by_name(session=db, tenant_name=payload.name)
        if tenant:
            response.status_code = HttpStatus.HTTP_409_CONFLICT
            return SingleResponse(status=RequestStatus.error, 
                                  value=None,
                                  error=f"Tenant name '{payload.name}' is not available. Please use different tenant name.")
        
        new_tenant = await ts.create_tenant(payload)
        
        return SingleResponse(status=RequestStatus.success, value=TenantSchema.from_orm(new_tenant))
    
    except TenantNameNotAvailableError as e:
        response.status_code = HttpStatus.HTTP_409_CONFLICT
        return SingleResponse(status=RequestStatus.error, value=None, error=str(e))
    
    except Exception as e:
        return SingleResponse(status=RequestStatus.error, value=None, error="Internal error")
    
