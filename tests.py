from features import GoogleHandler, SpeedTester, IMDbScraper, TranslatorHandler, WeatherHandler, YahooFinanceScraper, DictionarySearcher
import pytest


class TestGoogleHandler():
    @pytest.mark.parametrize(
        "location,expected_url,expected_result",
        [
            (
                "Santa Barbara", 
                "https://www.google.com/maps/place/Santa%20Barbara",
                True
            ),
            (
                "Miami",
                "https://www.google.com/maps/place/Miami",
                True
            ),
            (
                "New York City",
                "https://www.google.com/maps/place/New%20York%20City",
                True
            ),
            (
                "",
                "",
                "Parameter 'location' cannot be blank."
            )
        ]
    )
    def test_google_maps_search(self, location, expected_url, expected_result):
        google = GoogleHandler()
        if not location:
            with pytest.raises(ValueError) as err_info:
                location_url = google.google_maps_search(location)
            assert expected_result in str(err_info.value)
        else:
            location_url = google.google_maps_search(location)
            assert isinstance(location_url, str)
            assert location_url == expected_url
            opened_webpage = google.open_webpage(location_url)
            assert opened_webpage == expected_result


    @pytest.mark.parametrize(
        "query,expected_url,expected_result",
        [
            (
                "Tesla stock price Yahoo Finance",
                "https://finance.yahoo.com/quote/TSLA/",
                True
            ),
            (
                "Elon Musk Wikipedia",
                "https://en.wikipedia.org/wiki/Elon_Musk",
                True
            ),
            (
                "PewDiePie Youtube Channel",
                "https://www.youtube.com/user/PewDiePie",
                True
            ),
            (
                "",
                "",
                "Parameter 'query' cannot be blank."
            )
        ]
    )
    def test_google_search(self, query, expected_url, expected_result):
        google = GoogleHandler()
        if not query:
            with pytest.raises(ValueError) as err_info:
                query_url = google.google_search(query)
            assert expected_result in str(err_info.value)
        else:
            query_url = google.google_search(query)
            assert isinstance(query_url, str)
            assert query_url == expected_url
            opened_webpage = google.open_webpage(query_url)
            assert opened_webpage == expected_result


class TestIMDbScraper():
    @pytest.mark.parametrize(
        "movie_title,expected",
        [
            (
                "the karate kid",
                "https://www.imdb.com/title/tt0087538/"
            ),
            (
                "the silence of the lambs",
                "https://www.imdb.com/title/tt0102926/"
            ),
            (
                "jobs",
                "https://www.imdb.com/title/tt2357129/"
            ),
            (
                "",
                "Parameter 'movie_title' cannot be blank."
            )
        ]
    )
    def test_imdb_url(self, movie_title, expected):
        scraper = IMDbScraper()
        if not movie_title:
            with pytest.raises(ValueError) as err_info:
                imdb_url = scraper.get_imdb_url(movie_title)
            assert expected in str(err_info.value)
        else:
            imdb_url = scraper.get_imdb_url(movie_title)
            assert isinstance(imdb_url, str)
            assert imdb_url == expected


    @pytest.mark.parametrize(
        "imdb_url,expected",
        [
            (
                "https://www.imdb.com/title/tt0087538/",
                {"title": "The Karate Kid (1984)", "metascore": "60"}
            ),
            (
                "https://www.imdb.com/title/tt0102926/",
                {"title": "The Silence of the Lambs (1991)", "metascore": "85"}
            ),
            (
                "https://www.imdb.com/title/tt2357129/",
                {"title": "Jobs (2013)", "metascore": "44"}  
            ),
            (
                "",
                {"title": "", "metascore": ""} 
            )
        ]
    )
    def test_find_imdb(self, imdb_url, expected):
        scraper = IMDbScraper()
        imdb_info = scraper.find_imdb(imdb_url)
        assert isinstance(imdb_info, dict)
        assert len(imdb_info) == 2
        assert imdb_info == expected

     
    @pytest.mark.parametrize(
        "movie_title,expected",
        [
            (
                "the karate kid",
                "The Karate Kid (1984) has an IMDB Score of 7.3 and a Metascore of 60."
            ),
            (
                "the silence of the lambs",
                "The Silence of the Lambs (1991) has an IMDB Score of 8.6 and a Metascore of 85."
            ),
            (
                "jobs",
                "Jobs (2013) has an IMDB Score of 6.0 and a Metascore of 44."
            ),
            (
                "",
                "Parameter 'movie_title' cannot be blank."
            )
        ]
    )
    def test_get_movie_info(self, movie_title, expected):
        scraper = IMDbScraper()
        if not movie_title:
            with pytest.raises(ValueError) as err_info:
                movie_review = scraper.get_movie_review(movie_title)
            assert expected in str(err_info.value)
        else:
            movie_review = scraper.get_movie_review(movie_title)
            assert isinstance(movie_review, str)
            assert movie_review ==  expected


class TestWeatherHandler():
    def test_get_location(self):
        weather = WeatherHandler()

        # This works for my personal location.
        # I am in Irvine, CA, USA.
        location = weather.get_location()
        assert isinstance(location, list)
        assert location[0] == "Irvine"
        # To protect personal privacy, just checking
        # the scraped location is close enough.
        assert (float(location[1]) - 33.6600) < 0.1
        assert (float(location[2]) - -117.8264) < 0.1


    def test_get_weather_json(self):
        weather = WeatherHandler()
        latitude = '33.6600'
        longitude = '-117.8300'
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
    @pytest.mark.parametrize(
        "query,expected",
        [
            (
                "stock price of Tesla",
                "https://finance.yahoo.com/quote/TSLA/"
            ),
            (
                "stock price of Costco",
                "https://finance.yahoo.com/quote/COST/"
            ),
            (
                "stock price of Apple",
                "https://finance.yahoo.com/quote/AAPL/"
            ),
            (
                "",
                "Parameter 'query' cannot be blank."
            )
        ]
    )
    def test_get_yahoo_finance_url(self, query, expected):
        yahoo = YahooFinanceScraper()
        if not query:
            with pytest.raises(ValueError) as err_info:
                yahoo_finance_url = yahoo.get_yahoo_finance_url(query)
            assert expected in str(err_info.value)
        else:
            yahoo_finance_url = yahoo.get_yahoo_finance_url(query)
            assert isinstance(yahoo_finance_url, str)
            assert yahoo_finance_url == expected


    #As of November 4, 2021.
    @pytest.mark.parametrize(
        "query,expected",
        [
            (
                "stock price of Tesla",
                "The stock price is $1,229.91 per share."
            ),
            (
                "stock price of Costco",
                "The stock price is $515.62 per share."
            ),
            (
                "stock price of Apple",
                "The stock price is $150.96 per share."
            ),
            (
                "",
                "Parameter 'query' cannot be blank."
            )
        ]
    )
    def test_get_stock_price(self, query, expected):
        yahoo = YahooFinanceScraper()
        if not query:
            with pytest.raises(ValueError) as err_info:
                stock_price_info = yahoo.get_stock_price(query)
            assert expected in str(err_info.value)
        else:
            stock_price_info = yahoo.get_stock_price(query)
            assert isinstance(stock_price_info, str)
            assert stock_price_info == expected


class TestDictionarySearcher():
    @pytest.mark.parametrize(
        "word,expected",
        [
            (
                "bitter",
                ("1) Noun: English term for a dry sharp-tasting ale with strong flavor of hops (usually on draft.\n"
                "2) Noun: The taste experience when quinine or coffee is taken into the mouth.\n"
                "3) Noun: The property of having a harsh unpleasant taste.\n"
                "4) Verb: Make bitter.\n"
                "5) Adjective: Marked by strong resentment or cynicism.\n"
                "6) Adjective: Very difficult to accept or bear.\n"
                "7) Adjective: Harsh or corrosive in tone.\n"
                "8) Adjective: Expressive of severe grief or regret.\n"
                "9) Adjective: Proceeding from or exhibiting great hostility or animosity.\n"
                "10) Adjective: Causing a sharp and acrid taste experience.\n"
                "11) Adjective: Causing a sharply painful or stinging sensation; used especially of cold.\n"
                "12) Adverb: Extremely and sharply.\n")
            ),
            (
                "finance",
                ("1) Noun: The commercial activity of providing funds and capital.\n"
                "2) Noun: The branch of economics that studies the management of money and other assets.\n"
                "3) Noun: The management of money and credit and banking and investments.\n"
                "4) Verb: Obtain or provide money for.\n"
                "5) Verb: Sell or provide on credit.\n")
            ),
            (
                "Tesla",
                ("1) Noun: A unit of magnetic flux density equal to one weber per square meter.\n"
                "2) Noun: United states electrical engineer and inventor (born in croatia but of serbian descent.\n"
                "3) Noun: 1856-1943.\n")
            ),
            (
                "",
                "Parameter 'word' cannot be blank."
            )
        ]
    )
    def test_search_definition(self, word, expected):
        dictionary = DictionarySearcher()
        if not word:
            with pytest.raises(ValueError) as err_info:
                definition = dictionary.search_definition(word)
            assert expected in str(err_info.value)
        else:
            definition = dictionary.search_definition(word)
            assert isinstance(definition, str)
            assert definition == expected


class TestTranslator():
    @pytest.mark.parametrize(
        "text,language,expected_translation,expected_pronounciation,expected_langcode",
        [
            (
                "Hello world!",
                "spanish",
                "¡Hola Mundo!",
                None,
                "es"
            ),
            (
                "Hello world!",
                "french",
                "Bonjour le monde!",
                None,
                "fr"
            ),
            (
                "Thank you for testing the virtual assistant.",
                "russian",
                "Спасибо за тестирование виртуального помощника.",
                "Spasibo za testirovaniye virtual\'nogo pomoshchnika.",
                "ru"
            ),
            (
                "",
                "spanish",
                "Text cannot be blank.",
                "",
                ""
            ),  
            (
                "I don't know what to translate to!",
                "",
                "Language cannot be blank.",
                "",
                ""
            ),             
        ]
    ) 
    def test_translate(self, text, language, expected_translation, expected_pronounciation, expected_langcode):
        translator = TranslatorHandler()
        if not (text and language):
            with pytest.raises(ValueError) as err_info:
                translated_text = translator.translate(text, language)
            assert expected_translation in str(err_info.value)
        else:
            translated_text = translator.translate(text, language)
            assert translated_text[0] == expected_translation
            assert translated_text[1] == expected_pronounciation
            assert translated_text[2] == expected_langcode


class TestSpeedTester():
    def test_speed_test(self):
        speedtest_ = SpeedTester()
        speedtest_result = speedtest_.speed_check()
        assert isinstance(speedtest_result, str)
        print(speedtest_result)
