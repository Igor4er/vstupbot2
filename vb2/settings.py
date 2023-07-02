from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    TOKEN: str = "DEFAULT"
    BASE_KEY: str = "DEFAULT"
    
    class Config:
        env_prefix: str = "VB_"


load_dotenv()
settings = Settings()
