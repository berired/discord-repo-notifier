import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER")
    GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME")
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', "")
    PORT = int(os.getenv("PORT", 10000))
    DATABASE_PATH = 'bot_data.db'
    
    @classmethod
    def validate(cls):
        required = ['DISCORD_TOKEN', 'GITHUB_REPO_OWNER', 'GITHUB_REPO_NAME']
        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")