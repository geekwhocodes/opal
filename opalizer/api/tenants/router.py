from fastapi import APIRouter, Depends, Request, Response
from fastapi import status as HttpStatus
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from opalizer.api.tenants.utils import slugify, generate_api_key

from opalizer.core.rate_limiter import limiter
from opalizer.schemas import SingleResponse, CollectionResponse, RequestStatus
from opalizer.api.tenants.schemas import TenantSchema
from opalizer.api.tenants.models import Tenant
from opalizer.database import get_public_db

orgs_router = APIRouter(
    prefix="/v1/tenants"
)

@orgs_router.get("/{id}", status_code=HttpStatus.HTTP_200_OK)
async def get_org(id:int):
    return

@orgs_router.post("/", status_code=HttpStatus.HTTP_201_CREATED)
@limiter.limit("10/second")
async def create_tenant(request:Request, response:Response, 
                     payload: TenantSchema, 
                     db:Session=Depends(get_public_db)) -> SingleResponse:
    try:
        new_tenant = Tenant(**payload.dict())
        new_tenant.schema = payload.name
        new_tenant.slug = slugify(payload.name)
        new_tenant.api_key = generate_api_key(suffix=payload.name)
        db.add(new_tenant)
        await db.commit()
        await db.refresh(new_tenant)
        return SingleResponse(status=RequestStatus.success, value=TenantSchema.from_orm(new_tenant))
    except Exception as e:
        return SingleResponse(status=RequestStatus.error, value=None, error=str(e))
    
