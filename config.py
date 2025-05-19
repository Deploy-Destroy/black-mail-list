import os

class Config:
#   SQLALCHEMY_DATABASE_URI = 'sqlite:///blacklist.db'
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:postgres@database-1.cgxmos68q6oe.us-east-1.rds.amazonaws.com:5432/postgres"       
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    API_TOKEN = os.environ.get('API_TOKEN') or 'blacklist-secret-token-2024' 



