from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_URL: str

    REDIS_HOST: str
    REDIS_PORT: str

    SMTP_PORT: str
    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PASS: str

    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"

settings = Settings()