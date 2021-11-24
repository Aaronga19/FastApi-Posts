import os
from pydantic import BaseSettings

# Settings
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str  
    algorithm: str
    access_token_expires_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()

print(settings.database_password)