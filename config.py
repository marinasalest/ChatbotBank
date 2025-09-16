"""
Configurações da aplicação Flask
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações da aplicação"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000


