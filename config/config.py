import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    "base config class"
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # PokeAPI
    POKEAPI_BASE_URL = os.getenv('POKEAPI_BASE_URL')
    POKEAPI_TIMEOUT = int(os.getenv('POKEAPI_TIMEOUT', '10'))