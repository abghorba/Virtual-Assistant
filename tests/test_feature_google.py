import pytest

from src.features.google import GoogleHandler


class TestGoogleHandler():

    @pytest.mark.parametrize(
        "location,expected_url,expected_result",
        [
            (
                "Santa Barbara",
                "https://www.google.com/maps/place/Santa%20Barbara",
                True,
            ),
            (
                "Miami",
                "https://www.google.com/maps/place/Miami",
                True
            ),
            (
                "New York City",
                "https://www.google.com/maps/place/New%20York%20City",
                True,
            ),
            (
                "",
                "",
                "Parameter 'location' cannot be blank."
            ),
        ],
    )
    def test_google_maps_search(self, location, expected_url, expected_result):
        """Tests the google_maps_search function."""

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
                True,
            ),
            (
                "Elon Musk Wikipedia",
                "https://en.wikipedia.org/wiki/Elon_Musk",
                True
            ),
            (
                "PewDiePie Youtube Channel",
                "https://www.youtube.com/user/pewdiepie",
                True,
            ),
            (
                "",
                "",
                "Parameter 'query' cannot be blank."
            ),
        ],
    )
    def test_google_search(self, query, expected_url, expected_result):
        """Tests the google_search function."""

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
