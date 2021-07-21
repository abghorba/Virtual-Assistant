from bs4 import BeautifulSoup
from config import OPEN_WEATHER_API_KEY

import requests

class WeatherHandler():
    def get_location(self):
        """
            Scrapes information from www.iplocation.com to retrieve the user's
            location by using the user's IP Address. If user is using a VPN, then
            this will not work, as the IP Address will be that of the VPN Server.

            :returns: List containing the city, country, and latitude/longitude
            coordinates.

        """
        try:
            url = 'https://iplocation.com/'
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            city = soup.find(class_='city').get_text()
            country = soup.find(class_='country_name').get_text()
            latitude = soup.find(class_='lat').get_text()
            longitude = soup.find(class_='lng').get_text()
            location = [city, country, latitude, longitude]
            return location
        except Exception as e:
            print('Location could not be retrieved.')


    def get_weather_json(self):
        """
            Makes an API call to the OpenWeatherMAP API and retrieves the
            weather information.

            :returns: json dict of weather information

        """
        location = self.get_location()
        latitude = location[2]
        longitude = location[3]
        try:
            base_url = 'http://api.openweathermap.org/data/2.5/weather?'
            query = f'lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_API_KEY}&units=imperial'
            url = base_url + query
            response = requests.get(url)
            data = response.json()
            return data
        except Exception as e:
            print("Cannot retrieve weather information.")

    
    def get_weather_information(self):
        """
            Sends the user the revelant weather information.

            :returns: str

        """
        weather_data = self.get_weather_json()