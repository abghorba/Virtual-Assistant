import pytest

from src.features.weather import WeatherHandler


class TestWeatherHandler:
    def test_get_location(self):
        """Tests the get_location function."""

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
        """Tests the get_weather_json function."""
        weather = WeatherHandler()
        latitude = "33.6600"
        longitude = "-117.8300"
        json_data = weather.get_weather_json(latitude, longitude)

        assert isinstance(json_data, dict)
        assert "main" in json_data
        assert "weather" in json_data
        assert "wind" in json_data

    def test_check_weather(self):
        """Tests the check_weather function."""

        weather = WeatherHandler()
        forecast = weather.check_weather()

        assert isinstance(forecast, str)
        assert "The weather in Irvine is" in forecast
        assert "degrees Fahrenheit with a humidity of" in forecast
        assert "wind speeds of" in forecast
