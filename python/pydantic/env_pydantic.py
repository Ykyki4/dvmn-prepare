from pydantic import (
    BaseSettings,
    RedisDsn,
    PostgresDsn,
)


class Settings(BaseSettings):
    auth_key: str
    api_key: str

    redis_dsn: RedisDsn
    pg_dsn: PostgresDsn

    domains: set[str] = set()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = "pydantic_"


if __name__ == "__main__":
    print(Settings().dict())
