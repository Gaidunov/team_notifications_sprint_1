from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    redis_url: str
    broker_url: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
