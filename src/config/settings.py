from pydantic import BaseSettings

class Settings(BaseSettings):
    # MongoDB Configuration
    MONGODB_URI: str
    DATABASE_NAME: str

    # Model Configuration
    MODEL_PATH: str
    CONFIDENCE_THRESHOLD: float = 0.7

    # Security
    API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()