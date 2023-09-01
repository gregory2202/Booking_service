from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_HOST}/{self.DB_NAME}"

    JWT_KEY: str
    JWT_ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
