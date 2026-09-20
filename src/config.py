from functools import lru_cache
from pathlib import Path
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

ROOT = Path(__file__).resolve().parent.parent  # Get the root directory of the project

class Settings(BaseModel):
    #OpenAI configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", "3072"))

    # Pinecode configuration
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "")
    PINECONE_NAMESPACE: str = os.getenv("PINECONE_NAMESPACE", "")
    PINECONE_CLOUD: str = os.getenv("PINECONE_CLOUD", "aws")
    PINECONE_REGION: str = os.getenv("PINECONE_REGION", "us-east-1")

    # Internet configuration
    TAVI_API_KEY: str = os.getenv("TAVI_API_KEY", "")

    # Self RAG controls
    TOP_K: int = int(os.getenv("TOP_K", "5"))
    MAX_SUPPORT_RETRIES: int = int(os.getenv("MAX_SUPPORT_RETRIES", "2"))
    MAX_RETRIEVAL_REWRITES: int = int(os.getenv("MAX_RETRIEVAL_REWRITES", "2"))
    MAX_WEB_REWRITES: int = int(os.getenv("MAX_WEB_REWRITES", "2"))
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "data/audit.db")

    @property
    def database_file(self) -> Path:
        p = Path(self.DATABASE_PATH)
        return p if p.is_absolute() else ROOT / p

@lru_cache()
def get_settings() -> Settings:
    return Settings()


