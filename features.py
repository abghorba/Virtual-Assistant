from bs4 import BeautifulSoup
from bs4.dammit import html_meta
from config import OPEN_WEATHER_API_KEY
from googlesearch import search

import imdb
import os
import requests
import speedtest
import time


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


class GoogleHandler():

    def open_webpage(self, url):
        """
            Opens a url webpage.

            :returns: bool

        """
        try:
            webpage = '/usr/bin/open -a "/Applications/Google Chrome.app" ' + url
            os.system(webpage)
            time.sleep(3)
            return True
        except Exception as e:
            print("Could not open webpage.")
            return False


    def google_search(self, query):
        """
            Conducts a Google search with the given query.
            Relies heavily on Google's PageRank to supply the
            correct url as the first item returned in the search.

            :returns: URL as a str

        """
        try:
            links = []
            for url in search(query, tld='ca', num=10, stop=10, pause=2):
                links.append(url)
            
            return links[0]
        except Exception as e:
            print("Could not conduct Google search.")


    def google_maps_search(self, location):
        """
            Conducts a Google maps search with the given query.

            :returns: URL as a str

        """
        location = location.replace(" ", "%20")
        location_url = "https://www.google.com/maps/place/" + location

        return location_url


class IMDbScraper():

    def get_imdb_url(self, query):
        """
            Takes in a raw query and conducts a Google search to retrieve
            the correct url.

            :param query: Movie/TV Show to search
            :type query: str
            :returns: str
        
        """
        try:
            query += ' IMDb'
            google = GoogleHandler()
            imdb_url = google.google_search(query)
            return imdb_url
        except Exception as e:
            print("Movie cannot be found.")


    def find_imdb(self, imdb_url):
        """
            Takes in the movie url and scrapes the necessary information from IMDb.

            :param imdb_url: The url of the IMDb website.
            :type imdb_url: str
            :returns: dict

        """
        try:
            page = requests.get(imdb_url)
            html_content = page.text
            soup = BeautifulSoup(html_content, 'html.parser')
            title = soup.find(attrs={"data-testid":"hero-title-block__title"}).get_text()
            year = soup.find(class_="TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex").get_text()
            title = f"{title} ({year})"
            metascore = soup.find(class_="score-meta").get_text()
            return {"title": title, "metascore": metascore}
        except Exception as e:
            print("Movie cannot be found.")


    def get_movie_review(self, movie):
        """
            Driver function to retrieve the movie review scores.

            :param movie: Movie/TV Show being searched.
            :type movie: str
            :returns: str

        """
        try:
            imdb_url = self.get_imdb_url(movie)
            imdb_info = self.find_imdb(imdb_url)
            imdb_title = imdb_info['title']
            metascore = imdb_info['metascore']

            moviesDB = imdb.IMDb()
            movies = moviesDB.search_movie(imdb_title)
            id = movies[0].getID()
            movie_info = moviesDB.get_movie(id)
            title = movie_info['title']
            year = movie_info['year']
            imdb_score = movie_info['rating']

            review = f"{title} ({year}) has an IMDB Score of {imdb_score} and a Metascore of {metascore}."
            return review
        except Exception as e:
            print("Movie cannot be found.")


class SpeedTester():

    def speed_check(self):
        try:
            print('Testing...')
            s = speedtest.Speedtest()
            s.get_best_server()
            s.download()
            s.upload()
            res = s.results.dict()

            server = []
            server.append(res["server"]["name"])
            server.append(res["server"]["country"])
            server.append(res["server"]["sponsor"])

            client = []
            client.append(res["client"]["ip"])
            client.append(res["client"]["isp"])

            speed = []
            ONE_MB = 1000000
            speed.append((round((res["download"]/ONE_MB), 2)))
            speed.append((round((res["upload"]/ONE_MB), 2)))
            speed.append((round((res["ping"]), 2)))

            print(f'IP address : {client[0]}\nService Provider : {client[1]}')
            print(f'Connected to {server[2]} server\nLocation : {server[0]}, {server[1]}')
            print(f'Download speed  : {speed[0]} mpbs\nUpload speed : {speed[1]} mpbs\nPing : {speed[2]} ms ')

            speedtest_result = f'Download speed is {speed[0]} megabytes per second. Upload speed is {speed[1]} megabytes per second. Ping is {speed[2]} milliseconds.'
            return speedtest_result
        except Exception as e:
            print("Could not execute speedtest.")


class YahooFinanceScraper():

    def get_yahoo_finance_url(self, query):
        """
            Takes in a raw query and conducts a Google search to retrieve
            the correct url.

            :param query: The company we are trying to find the stock price for.
            :type query: str
            :returns: str
        
        """
        try:
            query += ' Yahoo finance'
            google = GoogleHandler()
            yahoo_finance_url = google.google_search(query)
            return yahoo_finance_url
        except Exception as e:
            print("This company is not found on Yahoo finance.")


    def get_stock_price(self, query):
        """
            Scrapes the Yahoo Finance website for the stock price.

            :param query: The company we are trying to find the stock price for.
            :type query: str
            :returns: str
        
        """
        try:
            yahoo_finance_url = self.get_yahoo_finance_url(query)
            page = requests.get(yahoo_finance_url)
            html_content = page.text
            soup = BeautifulSoup(html_content, 'html.parser')
            stock_price = soup.find(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)").get_text()
            stock_price_information = f'The stock price is ${stock_price} per share.'
            return stock_price_information
        except Exception as e:
            print("Stock price cannot be retrieved.")


    def get_stock_statistics_url(self, query):
        try:
            yahoo_finance_url = self.get_yahoo_finance_url(query)
            yahoo_finance_url_list = yahoo_finance_url.split("/")
            ticker = yahoo_finance_url_list[4]
            yahoo_finance_statistics_url = yahoo_finance_url + f'key-statistics?p={ticker}'
            return yahoo_finance_statistics_url
        except Exception as e:
            print("The statistics url cannot be retrieved.")


    def get_stock_statistics_info(self, query):
        try:
            yahoo_finance_statistics_url = self.get_stock_statistics_url(query)
            page = requests.get(yahoo_finance_statistics_url)
            html_content = page.text
            soup = BeautifulSoup(html_content, 'html.parser')
            valuation_measures_df = pd.read_html(soup, attrs={'class': 'W(100%) Bdcl(c)  M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)'})
            pass
        except Exception as e:
            print("Cannot retrieve information from the statistics page.")