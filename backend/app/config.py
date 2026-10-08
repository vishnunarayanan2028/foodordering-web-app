import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Load .env from backend directory or project root
backend_env = Path(__file__).resolve().parent.parent / '.env'
if backend_env.exists():
    load_dotenv(backend_env)
else:
    load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'foodmunch-secret-key-2026'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://root:root@localhost/foodmunch_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'foodmunch-jwt-secret-2026'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

