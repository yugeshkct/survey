import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SM_TOKEN = os.getenv("SM_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
    FRONTEND_URL = os.getenv("FRONTEND_URL")
    BASE_URL = "https://api.surveymonkey.com/v3"