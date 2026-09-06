import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


# Keycloal credits
# user: aditya
# pass: Aditya1988!

class Settings(BaseSettings):

    KEYCLOAK_SERVER :str
    KEYCLOAK_PUBLIC_SERVER :str
    KEYCLOAK_REALM :str
    KEYCLOAK_CLIENT_ID :str
    KEYCLOAK_CLIENT_SECRET:str
    KEYCLOAK_REDIRECT_URI : str 
    BACKEND_URL:str
    KEYCLOAK_POST_LOGOUT_REDIRECT_URI:str

    model_config = SettingsConfigDict(
        env_file=".env"
    )
    PG_USER: str
    PG_PASSWORD: str
    PG_PORT: str
    PG_HOST: str
    PG_DB: str


   


env_settings = Settings()

