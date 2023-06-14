from functools import lru_cache
from pydantic import BaseSettings, PostgresDsn
import os

class Settings(BaseSettings):
    app_name:str = "Opalizer"
    env:str = "dev"
    log_file:str = "log.log"

    db_url:PostgresDsn = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        user=os.getenv("SQL_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("SQL_HOST"),
        port="5432",
        path=f"/{os.getenv('SQL_DB') or ''}",
    )
    db_test_url:PostgresDsn = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        user=os.getenv("SQL_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("SQL_HOST"),
        port="5432",
        path=f"/{os.getenv('SQL_TEST_DB') or ''}",
    )
    sql_echo:str = os.getenv('SQL_ECHO')
    items_per_page = 10

@lru_cache
def get_settings()-> Settings:
    return Settings()


settings = get_settings()