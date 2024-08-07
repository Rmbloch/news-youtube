import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
CLIENT_SECRETS_FILE = os.getenv('CLIENT_SECRET_PATH')
WORLD_NEWS_KEY = os.getenv('WORLD_NEWS_API_KEY')
GNEWS_KEY = os.getenv('GNEWS_API_KEY')