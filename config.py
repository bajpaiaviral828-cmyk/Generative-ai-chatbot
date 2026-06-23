import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    MAX_HISTORY_TURNS = int(os.getenv("MAX_HISTORY_TURNS", 10))
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME", "chatbot_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            raise EnvironmentError(
                "GEMINI_API_KEY is missing!\n"
                "Copy .env.example to .env and add your key from https://aistudio.google.com/app/apikey"
            )

    @classmethod
    def postgres_dsn(cls):
        return (
            f"host={cls.DB_HOST} port={cls.DB_PORT} "
            f"dbname={cls.DB_NAME} user={cls.DB_USER} password={cls.DB_PASSWORD}"
        )
