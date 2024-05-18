from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    screenshot_widht: int = 800
    screenshot_height: int = 600
    raw_data_dir: str = "./data/raw/"

    class Config:
        env_file: str = ".env"
    
SETTINGS: Settings = Settings()