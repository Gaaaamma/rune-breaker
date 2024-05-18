from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    name: str

    class Config:
        env_file: str = ".env"
    
SETTINGS: Settings = Settings()