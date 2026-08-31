"""
Configuration management for Twitter Viral Bot
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Twitter API Configuration
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

    # App Settings
    APP_NAME = os.getenv("APP_NAME", "TwitterViralBot")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Content Settings
    MAX_THREAD_LENGTH = int(os.getenv("MAX_THREAD_LENGTH", "10"))
    RESEARCH_DEPTH = os.getenv("RESEARCH_DEPTH", "deep")
    VIRAL_OPTIMIZATION = os.getenv("VIRAL_OPTIMIZATION", "True").lower() == "true"

    # Engagement Settings
    AUTO_ENGAGE = os.getenv("AUTO_ENGAGE", "True").lower() == "true"
    ENGAGEMENT_LIMIT_PER_HOUR = int(os.getenv("ENGAGEMENT_LIMIT_PER_HOUR", "30"))
    TARGET_HASHTAGS = os.getenv("TARGET_HASHTAGS", "#AI,#Tech").split(",")

    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "twitter_viral_bot" / "data"
    OUTPUT_DIR = DATA_DIR / "output"
    CACHE_DIR = DATA_DIR / "cache"

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = [
            ("OPENAI_API_KEY", cls.OPENAI_API_KEY),
            ("TWITTER_API_KEY", cls.TWITTER_API_KEY),
            ("TWITTER_API_SECRET", cls.TWITTER_API_SECRET),
            ("TWITTER_ACCESS_TOKEN", cls.TWITTER_ACCESS_TOKEN),
            ("TWITTER_ACCESS_TOKEN_SECRET", cls.TWITTER_ACCESS_TOKEN_SECRET),
        ]

        missing = [name for name, value in required if not value]

        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}. "
                f"Please copy .env.example to .env and fill in your API keys."
            )

        # Create directories
        cls.DATA_DIR.mkdir(exist_ok=True, parents=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
        cls.CACHE_DIR.mkdir(exist_ok=True, parents=True)

        return True
