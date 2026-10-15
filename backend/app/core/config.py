import os
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "AI Skin Intelligence & Personalized Skincare Planner"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "skincare_ai_super_secret_jwt_key_development_2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))
    
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "skiniq_prod_db")
    
    BACKEND_CORS_ORIGINS: List[str] = [
        origin.strip()
        for origin in os.getenv("BACKEND_CORS_ORIGINS", "*").split(",")
        if origin.strip()
    ]
    SEED_DEMO_DATA: bool = os.getenv("SEED_DEMO_DATA", "false").lower() == "true"

settings = Settings()
