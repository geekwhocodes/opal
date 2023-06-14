import re
import secrets

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