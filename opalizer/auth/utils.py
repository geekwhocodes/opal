from fastapi import Depends, HTTPException, Header, status, Security
from fastapi.security import APIKeyHeader, APIKeyQuery

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="api-key", auto_error=False)


def ensure_api_key(
        api_key_query: str = Security(api_key_query),
        api_key_header: str = Security(api_key_header)
    ):
    """ Ensure's that api key is present in headers or query path """
    
    if api_key_header:
        return api_key_header
    if api_key_query:
        return api_key_query

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

def ensure_tenant_header(tenant: str = Header(alias="tenant-id", example="{'tenant:'tenant name' or 'tenant-id':'tenant id'}")) -> str:
    """ Ensure's that tenant name or id present in the headers """
    if (tenant == None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Tenant in headers. Please pass tanant name or id in the headers.",
        )
    return tenant