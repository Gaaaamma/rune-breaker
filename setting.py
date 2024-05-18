from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    name: str = "ffgg"
    
SETTINGS: Settings = Settings()