from pydantic_settings import BaseSettings

class Settings(BaseSettings):
<<<<<<< HEAD
    GROQ_API_KEY: str
    OPENAI_API_KEY: str
    API_KEY: str
=======
    API_KEY: str
    OPENAI_API_KEY: str
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def QDRANT_URL(self):
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    class Config:
        env_file = ".env"
<<<<<<< HEAD
        extra = "ignore"

settings = Settings()
=======

settings = Settings()
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca
