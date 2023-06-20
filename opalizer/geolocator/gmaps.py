from functools import lru_cache
from typing import Union
from geopy.geocoders import GoogleV3
from geopy.location import Location
from geopy.adapters import AioHTTPAdapter

from opalizer.geolocator.geocoder import GeoLocator
from opalizer.config import settings

GEO_HASH_PRECISION = 12

class Gmaps(GeoLocator):
    def __init__(self, api_key:str=None) -> None:
        super().__init__()
        
        self.api_key = settings.gmaps_key
        if api_key:
            self.api_key = api_key

    @lru_cache(maxsize=1000)
    async def get_address(self, lat: float, long: float) -> Union[Location, None]:
        async with GoogleV3(
            api_key=self.api_key,
            user_agent=f"{settings.app_name}/{settings.version}",
            adapter_factory=AioHTTPAdapter,
        ) as geolocator:
            address =  await geolocator.reverse(query=(lat, long), exactly_one=True)
            return address
    async def get_geocode(self, adsress: str):
        return await super().get_geocode(adsress)
        
gmaps = Gmaps()


