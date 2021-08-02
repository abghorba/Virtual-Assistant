from features import GoogleHandler, SpeedTester, IMDbScraper, TranslatorHandler, WeatherHandler, YahooFinanceScraper, DictionarySearcher

class TestGoogleHandler():

    def test_google_maps_search(self):
        google = GoogleHandler()

        location = "Santa Barbara"
        location_url = google.google_maps_search(location)
        assert isinstance(location_url, str)
        assert location_url == "https://www.google.com/maps/place/Santa%20Barbara"
        opened_webpage = google.open_webpage(location_url)
        assert opened_webpage == True

        location = "Sacramento"
        location_url = google.google_maps_search(location)
        assert isinstance(location_url, str)
        assert location_url == "https://www.google.com/maps/place/Sacramento"
        opened_webpage = google.open_webpage(location_url)
        assert opened_webpage == True


    def test_google_search(self):
        google = GoogleHandler()

        query = "Tesla stock price Yahoo Finance"
        query_url = google.google_search(query)
        assert isinstance(query_url, str)
        assert query_url == "https://finance.yahoo.com/quote/TSLA/"
        opened_webpage = google.open_webpage(query_url)
        assert opened_webpage == True

        query = "Elon Musk Wikipedia"
        query_url = google.google_search(query)
        assert isinstance(query_url, str)
        assert query_url == "https://en.wikipedia.org/wiki/Elon_Musk"
        opened_webpage = google.open_webpage(query_url)
        assert opened_webpage == True


class TestIMDbScraper():

    def test_imdb_url(self):
        scraper = IMDbScraper()

        movie = "the karate kid"
        imdb_url = scraper.get_imdb_url(movie)
        assert isinstance(imdb_url, str)
        assert imdb_url == "https://www.imdb.com/title/tt0087538/"
        
        movie = "silence of the lambs"
        imdb_url = scraper.get_imdb_url(movie)
        assert isinstance(imdb_url, str)
        assert imdb_url == "https://www.imdb.com/title/tt0102926/"       


    def test_find_imdb(self):
        scraper = IMDbScraper()

        movie = "the karate kid"
        imdb_url = scraper.get_imdb_url(movie)
        imdb_info = scraper.find_imdb(imdb_url)
        assert isinstance(imdb_info, dict)
        assert len(imdb_info) == 2
        assert imdb_info == {"title": "The Karate Kid (1984)", "metascore": "60"}

        movie = "silence of the lambs"
        imdb_url = scraper.get_imdb_url(movie)
        imdb_url = scraper.get_imdb_url(movie)
        imdb_info = scraper.find_imdb(imdb_url)
        assert isinstance(imdb_info, dict)
        assert len(imdb_info) == 2
        assert imdb_info == {"title": "The Silence of the Lambs (1991)", "metascore": "85"}        


    def test_get_movie_info(self):
        scraper = IMDbScraper()

        movie = "the karate kid"
        movie_review = scraper.get_movie_review(movie)
        assert isinstance(movie_review, str)
        assert movie_review ==  "The Karate Kid (1984) has an IMDB Score of 7.3 and a Metascore of 60."

        movie = "silence of the lambs"
        movie_review = scraper.get_movie_review(movie)
        assert isinstance(movie_review, str)
        assert movie_review ==  "The Silence of the Lambs (1991) has an IMDB Score of 8.6 and a Metascore of 85."


class TestWeatherHandler():

    def test_get_location(self):
        weather = WeatherHandler()

        # This works for my personal location.
        # I am in Irvine, CA, USA.
        location = weather.get_location()
        assert isinstance(location, list)
        assert location[0] == "Irvine"
        assert location[1] == "United States"
        assert location[2] == "33.6607"
        assert location[3] == "-117.8264"

    def test_get_weather_json(self):
        weather = WeatherHandler()

        latitude = '33.6607'
        longitude = '-117.8264'
        json_data = weather.get_weather_json(latitude, longitude)
        assert isinstance(json_data, dict)
        assert 'main' in json_data
        assert 'weather' in json_data
        assert 'wind' in json_data

    def test_check_weather(self):
        weather = WeatherHandler()

        forecast = weather.check_weather()
        assert isinstance(forecast, str)
        assert "The weather in Irvine is" in forecast
        assert "degrees Fahrenheit with a humidity of" in forecast
        assert "wind speeds of" in forecast
        print(forecast)


class TestYahooFinanceScraper():
    def test_get_yahoo_finance_url(self):
        yahoo = YahooFinanceScraper()

        query = "stock price of Tesla"
        yahoo_finance_url = yahoo.get_yahoo_finance_url(query)
        assert isinstance(yahoo_finance_url, str)
        assert yahoo_finance_url == "https://finance.yahoo.com/quote/TSLA/"

        query = "stock price of McDonald's"
        yahoo_finance_url = yahoo.get_yahoo_finance_url(query)
        assert isinstance(yahoo_finance_url, str)
        assert yahoo_finance_url == "https://finance.yahoo.com/quote/MCD/"


    def test_get_stock_price(self):
        yahoo = YahooFinanceScraper()

        query = "stock price of Tesla"
        stock_price_info = yahoo.get_stock_price(query)
        assert isinstance(stock_price_info, str)
        assert stock_price_info == "The stock price is $687.20 per share."
        print(stock_price_info)

        query = "stock price of McDonald's"
        stock_price_info = yahoo.get_stock_price(query)
        assert isinstance(stock_price_info, str)
        assert stock_price_info == "The stock price is $242.71 per share."
        print(stock_price_info)


    def test_get_stock_statistics_url(self):
        yahoo = YahooFinanceScraper()

        query = "stock price of Tesla"
        yahoo_finance_stats_url = yahoo.get_stock_statistics_url(query)
        assert isinstance(yahoo_finance_stats_url, str)
        assert yahoo_finance_stats_url == "https://finance.yahoo.com/quote/TSLA/key-statistics?p=TSLA"

        query = "stock price of McDonald's"
        yahoo_finance_stats_url = yahoo.get_stock_statistics_url(query)
        assert isinstance(yahoo_finance_stats_url, str)
        assert yahoo_finance_stats_url == 'https://finance.yahoo.com/quote/MCD/key-statistics?p=MCD'


class TestDictionarySearcher():

    def test_search_definition(self):
        dictionary = DictionarySearcher()

        word = "bitter"
        definition = dictionary.search_definition(word)
        assert isinstance(definition, str)
        print(definition)

        word = "finance"
        definition = dictionary.search_definition(word)
        assert isinstance(definition, str)
        print(definition)

        word = "Tesla"
        definition = dictionary.search_definition(word)
        assert isinstance(definition, str)
        print(definition)


class TestTranslator():
    
    def test_translate(self):
        translator = TranslatorHandler()
        text = 'Hello, world!'
        translated_text = translator.translate(text, 'spanish')
        assert translated_text[0] == '¡Hola Mundo!'
        assert translated_text[1] is None
        assert translated_text[2] == 'es'
        translated_text = translator.translate(text, 'french')
        assert translated_text[0] == 'Bonjour le monde!'
        assert translated_text[1] is None
        assert translated_text[2] == 'fr'

        text = 'Thank you for testing the virtual assistant.'
        translated_text = translator.translate(text, 'russian')
        assert translated_text[0] == 'Спасибо за тестирование виртуального помощника.'
        assert translated_text[1] == 'Spasibo za testirovaniye virtual\'nogo pomoshchnika.'
        assert translated_text[2] == 'ru' 

class TestSpeedTester():

    def test_speed_test(self):
        speedtest_ = SpeedTester()
        speedtest_result = speedtest_.speed_check()
        assert isinstance(speedtest_result, str)
        print(speedtest_result)