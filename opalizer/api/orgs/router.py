from fastapi import APIRouter
from fastapi import status
from opalizer.schemas import BaseSchema, CreatedResponseSchema, ResponseStatus

orgs_router = APIRouter()

@orgs_router.get("/{id}", status_code=status.HTTP_200_OK)
async def create_org(id:int):
    
    return CreatedResponseSchema(status=ResponseStatus.success, data=BaseSchema(id=id))