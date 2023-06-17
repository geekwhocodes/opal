import re
import secrets

from sqlalchemy import UUID
from unidecode import unidecode

def slugify(s):
    """ Slugify the string 
        :param s: string value 
    """
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s

def generate_api_key(suffix:str) -> str:
    return f"{suffix}_{secrets.token_hex(16)}"

def generate_tenant_schema_name(name: str) -> str:
    company = re.sub("[^A-Za-z0-9 _]", "", unidecode(name))
    return "".join([company[:28]]).lower().replace(" ", "_")