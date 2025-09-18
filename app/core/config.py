from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiric LLM Service"
    API_V1_STR: str = "/api/v1"
    ENV: str = Field("production", validation_alias="ENV")
    LOG_LEVEL: str = Field("INFO", validation_alias="LOG_LEVEL")
    
    # --- YENİ EKLENEN ALANLAR ---
    # Bu değişkenler Dockerfile'dan ENV olarak set edilir ve Pydantic tarafından okunur.
    SERVICE_VERSION: str = Field("0.0.0", validation_alias="SERVICE_VERSION")
    GIT_COMMIT: str = Field("unknown", validation_alias="GIT_COMMIT")
    BUILD_DATE: str = Field("unknown", validation_alias="BUILD_DATE")
    # --- DEĞİŞİKLİK SONU ---
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8', 
        extra='ignore', 
        case_sensitive=False
    )

settings = Settings()