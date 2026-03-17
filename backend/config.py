import os
from dotenv import load_dotenv

load_dotenv()

DOMAIN_CLIENT_ID = os.getenv("DOMAIN_CLIENT_ID", "")
DOMAIN_CLIENT_SECRET = os.getenv("DOMAIN_CLIENT_SECRET", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
