from pydantic_settings import BaseSettings
from pydantic import model_validator


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str

    DATABASE_URL: str = ""


    @model_validator(mode="before")
    def get_database_url(cls, values: dict):
        values["DATABASE_URL"] = (
            f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}@"
            f"{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        )
        return values


    model_config = {
        "env_file": ".env"
    }


settings = Settings()
