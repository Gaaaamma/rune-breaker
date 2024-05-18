from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    name: str = "for test"
    
SETTINGS: Settings = Settings()