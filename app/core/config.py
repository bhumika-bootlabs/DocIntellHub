from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Document AI Hub")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
2
