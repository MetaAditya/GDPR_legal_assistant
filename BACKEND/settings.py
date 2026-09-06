import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):

    API_KEY: SecretStr
    LANGSMITH_API_KEY:SecretStr

    model: str
    PG_USER: str
    PG_PASSWORD: str
    PG_PORT: str
    PG_HOST: str
    PG_DB: str
    newsapi_key: str
    agent_memory_db:str
    LANGSMITH_ENDPOINT:str
    LANGSMITH_PROJECT:str
    LANGSMITH_TRACING:str
    



    model_config = SettingsConfigDict(
        env_file=".env"
    )





env_settings = Settings()

