from enum import Enum
from functools import lru_cache
from pydantic import BaseSettings, PostgresDsn
import os
from dotenv import load_dotenv
load_dotenv(".env")

def get_root_dir():
    root_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
    return root_dir


class Env(Enum):
    dev = 'dev'
    tst = 'tst'
    pre = 'pre'
    prd = 'prd'

class Settings(BaseSettings):
    app_name:str = "Opalizer"
    version:str = "0.0.2"
    environment:Env = os.environ.get("environment")
    log_file:str = "log.log"
    root_dir = get_root_dir()

    db_url:PostgresDsn = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        user=os.environ.get("SQL_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("SQL_HOST"),
        port="5432",
        path=f"/{os.environ.get('SQL_DB') or ''}",
    )
    test_db_url:PostgresDsn = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        user=os.environ.get("SQL_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("SQL_HOST"),
        port="5432",
        path=f"/{os.environ.get('SQL_TEST_DB') or ''}",
    )
    sql_echo:str = False
    items_per_page = 10
    gmaps_key:str = os.environ.get("GMAPS_KEY")
    class Config:
        env_file = '/home/lowkey/opalizer/.env'
        env_file_encoding = 'utf-8'

@lru_cache
def get_settings()-> Settings:
    return Settings()

settings = get_settings()