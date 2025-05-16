
from dotenv import load_dotenv
from logging import config as logging_config
from pydantic import Field
from pydantic_settings import BaseSettings

from core.logger import LOGGING


load_dotenv()


logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = Field('project name', alias='PROJECT_NAME')

    pstg_user: str = Field('postgres_user', alias='POSTGRES_USER')
    pstg_password: str = Field('postgres_password', alias='POSTGRES_PASSWORD')
    pstg_host: str = Field('127.0.0.1', alias='POSTGRES_HOST')
    pstg_port: int = Field(5432, alias='POSTGRES_PORT')
    pstg_db_name: str = Field('postgres_db_name', alias='POSTGRES_DB')

    api_token: str = Field('token', alias='API_TOKEN')

    unprotected_urls: list[str] = [
        '/api/docs',
        '/api/docs.json',
    ]


settings = Settings()
