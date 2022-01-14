import imdb, os, requests, speedtest, time
from bs4 import BeautifulSoup
from config import OPEN_WEATHER_API_KEY
from googlesearch import search
from googletrans import Translator, LANGCODES
from PyDictionary import PyDictionary


class WeatherHandler:
    def get_location(self):
        """
        Scrapes information from www.iplocation.com to
        retrieve the user's location by using the user's
        IP Address. If user is using a VPN, then this will
        not work, as the IP Address will be the VPN Server's.

        Parameters
        ----------
        None

        Returns
        -------
        location : list
            A list containing the city, latitude,
            and longitude of the user.
        """
        location = []
        try:
            url = "https://iplocation.com/"
            page = requests.get(url)
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
        retrieves the weather information.

        Parameters
        ----------
        latitude : str
            The user's latitude.
        longitude : str
            The user's longitude.

        Returns
        -------
        data : json
            JSON containing the weather information.
        """
        data = {}
        try:
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            query = f"lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_API_KEY}&units=imperial"
            url = base_url + query
            response = requests.get(url)
            data = response.json()
            return data
        except Exception:
            print("Cannot retrieve weather information.")

        return data

    def check_weather(self):
        """
        Parses the json response from the API call
        and constructs a forecast which is returned
        to the user.

        Parameters
        ----------
        None

        Returns
        -------
        forecast : str
            A string containing the weather forecast.
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


class GoogleHandler:
    def open_webpage(self, url):
        """
        Opens a url webpage on Google Chrome.

        Parameters
        ----------
        None

        Returns
        -------
        success : boolean
            Returns true if the webpage opens
            in Google Chrome successfully.
        """
        if not url:
            raise ValueError("Parameter 'url' cannot be blank.")

        success = False
        try:
            webpage = '/usr/bin/open -a "/Applications/Google Chrome.app" ' + url
            os.system(webpage)
            time.sleep(3)
            success = True
        except Exception:
            print("Could not open webpage.")

        return success

    def google_search(self, query):
        """
        Conducts a Google search with the given query.
        Relies heavily on Google's PageRank to supply the
        correct url as the first item returned in the search.

        Parameters
        ----------
        query : str
            The query that is to be Google searched.

        Returns
        -------
        url_link : str
            A string containing first url from the Google search.
        """
        if not query:
            raise ValueError("Parameter 'query' cannot be blank.")

        url_link = ""
        try:
            links = []
            for url in search(query, tld="ca", num=10, stop=10, pause=2):
                links.append(url)
            url_link = links[0]
        except Exception:
            print("Could not conduct Google search.")

        return url_link

    def google_maps_search(self, location):
        """
        Conducts a Google Maps search with the given query.

        Parameters
        ----------
        location : str
            The location that is to be searched on Google Maps.

        Returns
        -------
        location_url : str
            A string containing the Google maps url.
        """
        if not location:
            raise ValueError("Parameter 'location' cannot be blank.")

        location = location.replace(" ", "%20")
        location_url = "https://www.google.com/maps/place/" + location

        return location_url


class IMDbScraper:
    def get_imdb_url(self, movie_title):
        """
        Takes in a movie name and conducts a Google
        search to retrieve the correct url.

        Parameters
        ----------
        movie_title: str
            The movie to search.

        Returns
        -------
        imdb_url : str
            A string containing the IMDb URL.
        """
        if not movie_title:
            raise ValueError("Parameter 'movie_title' cannot be blank.")

        imdb_url = ""
        try:
            movie_title += " IMDb"
            google = GoogleHandler()
            imdb_url = google.google_search(movie_title)
        except Exception:
            print("Movie cannot be found.")

        return imdb_url

    def find_imdb(self, imdb_url):
        """
        Takes in the movie url and scrapes the
        necessary information from IMDb.

        Parameters
        ----------
        imdb_url : str
            The url of the IMDb website.

        Returns
        -------
        location_url : str
            A string containing the Google maps url.
        """
        rating = {"title": "", "metascore": ""}
        try:
            page = requests.get(imdb_url)
            html_content = page.text
            soup = BeautifulSoup(html_content, "html.parser")
            title = soup.find(
                attrs={"data-testid": "hero-title-block__title"}
            ).get_text()
            year = soup.find(
                class_="TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex"
            ).get_text()
            title = f"{title} ({year})"
            metascore = soup.find(class_="score-meta").get_text()
            rating["title"] = title
            rating["metascore"] = metascore
        except Exception:
            print("Movie cannot be found.")

        return rating

    def get_movie_review(self, movie_title):
        """
        Driver function to retrieve the movie review scores.

        Parameters
        ----------
        movie_title : str
            Movie being searched.

        Returns
        -------
        review : str
            A string containing the movie review.
        """
        if not movie_title:
            raise ValueError("Parameter 'movie_title' cannot be blank.")

        review = ""
        try:
            imdb_url = self.get_imdb_url(movie_title)
            imdb_info = self.find_imdb(imdb_url)
            imdb_title = imdb_info["title"]
            metascore = imdb_info["metascore"]

            moviesDB = imdb.IMDb()
            movies = moviesDB.search_movie(imdb_title)
            id = movies[0].getID()
            movie_info = moviesDB.get_movie(id)
            title = movie_info["title"]
            year = movie_info["year"]
            imdb_score = movie_info["rating"]

            review = f"{title} ({year}) has an IMDB Score of {imdb_score} and a Metascore of {metascore}."
        except Exception:
            print("Movie cannot be found.")

        return review


class SpeedTester:
    def speed_check(self):
        """
        Performs a speed test, which tests for the
        upload, download, and ping.

        Parameters
        ----------
        None

        Returns
        -------
        speedtest_result : str
            The results of the speed test.
        """
        speedtest_result = ""
        try:
            print("Testing...")
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
            speed.append((round((res["download"] / ONE_MB), 2)))
            speed.append((round((res["upload"] / ONE_MB), 2)))
            speed.append((round((res["ping"]), 2)))

            print(f"IP address : {client[0]}\nService Provider : {client[1]}")
            print(
                f"Connected to {server[2]} server\nLocation : {server[0]}, {server[1]}"
            )
            print(
                f"Download speed  : {speed[0]} mpbs\nUpload speed : {speed[1]} mpbs\nPing : {speed[2]} ms "
            )

            speedtest_result = f"Download speed is {speed[0]} megabytes per second. Upload speed is {speed[1]} megabytes per second. Ping is {speed[2]} milliseconds."
        except Exception:
            print("Could not execute speedtest.")

        return speedtest_result


class YahooFinanceScraper:
    def get_yahoo_finance_url(self, query):
        """
        Takes in a raw query and conducts a Google
        search to retrieve the correct url.

        Parameters
        ----------
        query : str
            Company whose stock price to search for.

        Returns
        -------
        yahoo_finance_url : str
            The URL of the company's Yahoo Finance
            webpage.
        """
        if not query:
            raise ValueError("Parameter 'query' cannot be blank.")

        yahoo_finance_url = ""
        try:
            query += " Yahoo Finance"
            google = GoogleHandler()
            yahoo_finance_url = google.google_search(query)
        except Exception:
            print("This company is not found on Yahoo Finance.")

        return yahoo_finance_url

    def get_stock_price(self, query):
        """
        Scrapes the Yahoo Finance website for the stock price.

        Parameters
        ----------
        query : str
            Company whose stock price to search for.

        Returns
        -------
        stock_price_information : str
            String containg the company's stock price.
        """
        if not query:
            raise ValueError("Parameter 'query' cannot be blank.")

        stock_price_information = ""
        try:
            yahoo_finance_url = self.get_yahoo_finance_url(query)
            page = requests.get(yahoo_finance_url)
            html_content = page.text
            soup = BeautifulSoup(html_content, "html.parser")
            stock_price = soup.find(
                class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"
            ).get_text()
            stock_price_information = f"The stock price is ${stock_price} per share."
        except Exception:
            print("Stock price cannot be retrieved.")

        return stock_price_information


class DictionarySearcher:
    def search_definition(self, word):
        """
        Looks for the definition of a word and
        returns all the definitions.

        Parameters
        ----------
        word : str
            The word we want to define.

        Returns
        -------
        definition : str
            String containg word's definition.
        """
        if not word:
            raise ValueError("Parameter 'word' cannot be blank.")

        definition = ""
        dictionary = PyDictionary()
        try:
            definitions = dictionary.meaning(word)

            definition_number = 1
            definitions_text = []
            for type in definitions:
                for meaning in definitions[type]:
                    current_meaning = (
                        f"{str(definition_number)}) {type}: {meaning.capitalize()}.\n"
                    )
                    definitions_text.append(current_meaning)
                    definition_number += 1

            definition = "".join(definitions_text)
        except Exception:
            print("This word does not exist in the English dictionary.")

        return definition


class TranslatorHandler:
    def translate(self, text, language):
        """
        Takes a text string and translates to
        language of choice.

        Parameters
        ----------
        text : str
            The English text to translate.
        language : str
            The language to translate to.

        Returns
        -------
        translated : list
            Details of the translation.
        """
        if not text:
            raise ValueError("Text cannot be blank.")
        if not language:
            raise ValueError("Language cannot be blank.")

        translated = []
        try:
            translator = Translator()
            language_code = LANGCODES[language]
            translated_text = translator.translate(text, src="en", dest=language_code)
            translated = [
                translated_text.text,
                translated_text.pronunciation,
                language_code,
            ]
        except Exception:
            print("This text cannot be translated.")

        return translated
