from typing import Optional

from pydantic import UUID4, Extra, Field
from opalizer.schemas import ORJSONModel

class TenantSchema(ORJSONModel):
    id: Optional[UUID4]
    name:   str = Field(min_length=3)

    class Config:
        extra = Extra.forbid