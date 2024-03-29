import os

from dotenv import load_dotenv

# Configure environment variables
load_dotenv()

# OpenWeather API Key
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

# Constants
HTTP_STATUS_OK = 200

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/71.0.3578.98 Safari/537.36"
}
