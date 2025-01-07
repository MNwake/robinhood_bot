import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class Config:
    """Configuration class to manage environment variables."""

    API_KEY = os.getenv("API_KEY")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")

    @classmethod
    def validate(cls):
        """Ensure all required environment variables are set."""
        missing_vars = [var for var in ["API_KEY", "PRIVATE_KEY"] if not getattr(cls, var)]
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

        return True


# Validate configuration at import
Config.validate()
