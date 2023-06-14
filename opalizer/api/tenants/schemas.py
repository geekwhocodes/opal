from typing import Optional

from pydantic import UUID4, Extra
from opalizer.schemas import ORJSONModel

class TenantSchema(ORJSONModel):
    id: Optional[UUID4]
    name:   str

    class Config:
        extra = Extra.forbid