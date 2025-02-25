import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB settings
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/whtesting')
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this')
    JWT_ACCESS_TOKEN_EXPIRES = 24 * 3600  # 24 hours in seconds
    
    # OTP settings
    OTP_WINDOW_SIZE = 6  # Allow 3 minutes (6 * 30 seconds)
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:9000').split(',') 