from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from pathlib import Path
import os


class Settings(BaseSettings):
    # App settings
    APP_NAME: str = Field(default="app")
    APP_VERSION: str = Field(default="1.0.0")
    APP_ENV: str = Field(default="development")
    APP_SECRET_KEY: str = Field(default="")
    APP_TIMEZONE: str = Field(default="America/Mexico_City")
    NOTIFICATION_API_URL: str = Field(default="http://localhost")

    # Database settings
    DB_CONNECTION: str = Field(default="sqlite")
    DB_HOST: Optional[str] = Field(default=None)
    DB_PORT: Optional[str] = Field(default=None)
    DB_DATABASE: str = Field(default="database.sqlite")
    DB_USER: Optional[str] = Field(default=None)
    DB_PASSWORD: Optional[str] = Field(default=None)

    # Aquarius Database settings
    DB_AQUARIUS_CONNECTION: Optional[str] = Field(default=None)
    DB_AQUARIUS_HOST: Optional[str] = Field(default=None)
    DB_AQUARIUS_PORT: Optional[str] = Field(default=None)
    DB_AQUARIUS_DATABASE: Optional[str] = Field(default=None)
    DB_AQUARIUS_USER: Optional[str] = Field(default=None)
    DB_AQUARIUS_PASSWORD: Optional[str] = Field(default=None)

    # Redis settings
    REDIS_HOST: str = Field(default="127.0.0.1")
    REDIS_PORT: str = Field(default="6379")
    REDIS_USERNAME: str = Field(default="default")
    REDIS_PASSWORD: Optional[str] = Field(default=None)
    REDIS_DB: str = Field(default="0")

    # S3 settings
    S3_ACCESS_KEY: Optional[str] = Field(default=None)
    S3_SECRET_KEY: Optional[str] = Field(default=None)
    S3_REGION: Optional[str] = Field(default=None)
    S3_BUCKET: Optional[str] = Field(default=None)

    # External APIs
    CURP_API_URL: Optional[str] = Field(default=None)
    CURP_API_TOKEN: Optional[str] = Field(default=None)
    KYC_API_URL: Optional[str] = Field(default=None)
    KYC_API_TOKEN: Optional[str] = Field(default=None)

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def database_url(self) -> str:
        if self.DB_CONNECTION == "sqlite":
            base_path = Path(__file__).parents[2]
            return f"sqlite:///{base_path}/{self.DB_DATABASE}"
        elif self.DB_CONNECTION == "psql":
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
        else:
            raise ValueError(f"Unsupported database connection: {self.DB_CONNECTION}")

    @property
    def redis_config(self) -> dict:
        return {
            "HOST": self.REDIS_HOST,
            "PORT": self.REDIS_PORT,
            "USERNAME": self.REDIS_USERNAME,
            "PASSWORD": self.REDIS_PASSWORD,
            "DATABASE": self.REDIS_DB,
        }

    @property
    def s3_config(self) -> dict:
        return {
            "ACCESS_KEY": self.S3_ACCESS_KEY,
            "SECRET_KEY": self.S3_SECRET_KEY,
            "REGION": self.S3_REGION,
            "BUCKET": self.S3_BUCKET,
        }


settings = Settings()

