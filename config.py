import os

from dotenv import load_dotenv

# Configure environment variables
load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
