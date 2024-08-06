import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
CLIENT_SECRETS_FILE = os.getenv('CLIENT_SECRET_PATH')