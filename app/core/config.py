from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiric LLM Service"
    API_V1_STR: str = "/api/v1"
    ENV: str = "production"
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8', 
        extra='ignore', 
        case_sensitive=False
    )

settings = Settings()