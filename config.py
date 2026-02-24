import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configurações base do sistema."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-padrao-fallback'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/'