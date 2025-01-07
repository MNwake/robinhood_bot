import logging

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to terminal
    ],
)

# Create a logger object
logger = logging.getLogger("trading_bot")