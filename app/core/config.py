from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "super-secret-key" # 실제는 환경변수에서 불러오게 설정해야 함. 테스트 용도로 일단 했음
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
