from typing import Optional

from pydantic import UUID4, Extra, Field
from opalizer.api.tenants.schemas import TenantSchema
from opalizer.schemas import ORJSONModel

class StoreSchema(ORJSONModel):
    id: Optional[UUID4]
    name:   str = Field(min_length=3, max_length=200)
    owner: str = Field(default="owner", max_length=64)
    latitude: float = Field(description="Latitude of the store location.")
    longitude: float = Field(description="Longitude of the store location.")
    radius: float = Field(description="Acceptable radius from the store location.")
    #tenant_id: UUID4
    
    #tanant: Optional[TenantSchema]

    class Config:
        extra = Extra.forbid