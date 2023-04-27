import requests
from bs4 import BeautifulSoup

from src.features.utilities import HTTP_STATUS_OK, OPEN_WEATHER_API_KEY, REQUEST_HEADERS


class WeatherHandler:
    def get_location(self):
        """
        Scrapes information from www.iplocation.com to
        retrieve the user's location by using the user's
        IP Address

        return: List [city, latitude, longitude]
        """

        location = []

        try:
            url = "https://iplocation.com/"
            page = requests.get(url, headers=REQUEST_HEADERS)

            if page.status_code != HTTP_STATUS_OK:
                print(f"GET: {url} return status code {page.status_code}")

            soup = BeautifulSoup(page.content, "html.parser")
            city = soup.find(class_="city").get_text()
            latitude = soup.find(class_="lat").get_text()
            longitude = soup.find(class_="lng").get_text()
            location = [city, latitude, longitude]

        except Exception:
            print("Location could not be retrieved.")

        return location

    def get_weather_json(self, latitude, longitude):
        """
        Makes an API call to the OpenWeatherMAP API and
        retrieves the weather information

        :param latitude: The user's latitude
        :param longitude : The user's longitude
        :return: JSON containing local weather information.
        """

        data = {}

        try:
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            query = f"lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_API_KEY}&units=imperial"
            url = base_url + query
            response = requests.get(url)
            data = response.json()

        except Exception:
            print("Cannot retrieve weather information.")

        return data

    def check_weather(self):
        """
        Parses the json response from the API call
        and constructs a forecast which is returned
        to the user

        :return: String containing local weather forecast
        """

        city, latitude, longitude = self.get_location()
        weather_data = self.get_weather_json(latitude, longitude)

        temperature = str(round(weather_data["main"]["temp"]))  # in Fahrenheit
        condition = weather_data["weather"][0]["main"]
        description = weather_data["weather"][0]["description"]
        humidity = str(weather_data["main"]["humidity"]) + "%"
        wind_speed = round(weather_data["wind"]["speed"])

        forecast = (
            f"The weather in {city} is {condition} with {description}. "
            f"It is currently {temperature} degrees Fahrenheit with a humidity "
            f"of {humidity} and wind speeds of {wind_speed} miles per hour."
        )

        return forecast
