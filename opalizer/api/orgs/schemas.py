from typing import List
from opalizer.schemas import ORJSONModel, ResponseStatus

class OrgSchema(ORJSONModel):
    id: int
    name:   str

class OrgresponseSchema:
    status: ResponseStatus
    data: List[OrgSchema]