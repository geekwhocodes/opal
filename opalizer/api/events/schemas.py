import datetime
from typing import Optional, Union

from pydantic import UUID4, Extra, Field
from opalizer.schemas import ORJSONModel

class WindowLocation(ORJSONModel):
    href: Optional[str] = None
    origin: Optional[str] = None
    protocol: Optional[str] = None
    host: Optional[str] = None
    hostname: Optional[str] = None
    port: Optional[str] = None
    pathname: Optional[str] = None
    search: Optional[str] = None
    hash: Optional[str] = None

class Browser(ORJSONModel):
    app_code_name: str
    app_name: str
    userAgent: str

class EventSchemaIn(ORJSONModel):
    latitude:   float
    longitude:  float
    accuracy:   Union[float, None] = None
    ga_user_id: Union[str, None] = None
    window_location_json:   WindowLocation
    browser_json: Optional[Browser]
    
    class Config:
        extra = Extra.forbid