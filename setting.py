from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    screenshot_widht: int = 800
    screenshot_height: int = 600
    raw_data_dir: str = "./data/raw/"
    laplace_data_dir: str = "./data/laplace/"
    laplace_blue_threshold: int = 300

    class Config:
        env_file: str = ".env"
    
SETTINGS: Settings = Settings()