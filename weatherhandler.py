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


    def get_weather_json(self, latitude, longitude):
        """
            Makes an API call to the OpenWeatherMAP API and retrieves the
            weather information.

            :param latitude: The user's latitude.
            :type latitdue: str
            :param longitude: The user's longitude.
            :type longitude: str
            :returns: json dict of weather information

        """
        try:
            base_url = 'http://api.openweathermap.org/data/2.5/weather?'
            query = f'lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_API_KEY}&units=imperial'
            url = base_url + query
            response = requests.get(url)
            data = response.json()
            return data
        except Exception as e:
            print("Cannot retrieve weather information.")

    
    def check_weather(self):
        """
            Parses the json response from the API call and constructs
            a forecast which is returned to the user.
            
            :returns: str

        """
        city, country, latitude, longitude = self.get_location()
        weather_data = self.get_weather_json(latitude, longitude)

        temperature = str(round(weather_data['main']['temp'])) #in Fahrenheit
        condition = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        humidity = str(weather_data['main']['humidity']) + '%'
        wind_speed = round(weather_data['wind']['speed'])

        forecast = f"The weather in {city} is {condition} with {description}. "\
                    f"It is currently {temperature} degrees Fahrenheit with a humidity "\
                    f"of {humidity} and wind speeds of {wind_speed} miles per hour."

        return forecast


