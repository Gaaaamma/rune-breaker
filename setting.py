from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    screenshot_widht: int = 800
    screenshot_height: int = 600
    raw_data_dir: str = "./data/raw/"
    laplace_data_dir: str = "./data/laplace/"
    
    left_bound: int = 50
    right_bonud: int = 400

    laplace_blue_threshold: int = 240
    laplace_blue_tolerantion: int = 50
    laplace_blue_height_start: int = 150
    laplace_blue_height_end: int = screenshot_height / 2

    captcha_height: int = 80

    class Config:
        env_file: str = ".env"
    
SETTINGS: Settings = Settings()