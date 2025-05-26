from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API 
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Анализ качества воды API"
    
    # CORS 
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Model paths
    MODELS_DIR: str = "../models_for_water-main/models"
    DATASETS_DIR: str = "../models_for_water-main/datasets"
    
    class Config:
        case_sensitive = True

settings = Settings() 