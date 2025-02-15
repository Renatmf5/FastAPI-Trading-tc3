from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Configurations
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Trading system API"
    # Logging
    LOG_LEVEL: str = "info"
    # Environment
    ENV: str = "development"

    class Config:
        env_file = ".env"

if os.getenv('ENV') == 'production':
    """
    settings = Settings(
        JWT_SECRET=get_ssm_parameter("/my-fastApi-app/JWT_SECRET"),
        DATABASE_URL=get_ssm_parameter("/my-fastApi-app/DATABASE_URL"),
        BUCKET_NAME=get_ssm_parameter("/my-fastApi-app/BUCKET_NAME")
    )
    """
else:
    settings = Settings()