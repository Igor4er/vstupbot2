from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    TOKEN: str = "DEFAULT"
    DB_KEY: str = "DEFAULT"
    DB_URL: str = "https://tqaqvhepgpsjyetgpzwo.supabase.co/rest/v1"
    LOGCHAT: str = "DEFAULT"

    class Config:
        env_prefix: str = "VB_"


load_dotenv()
settings = Settings()
