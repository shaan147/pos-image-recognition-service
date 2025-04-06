from pydantic_settings import BaseSettings
import os
class Settings(BaseSettings):
    # MongoDB Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "pos_inventory_system"
    
    # Model Configuration
    CONFIDENCE_THRESHOLD: float = 0.7
    
    # Security
    API_KEY: str = "default_api_key"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

settings = Settings()