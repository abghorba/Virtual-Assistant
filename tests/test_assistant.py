import pytest

from src.virtual_assistant.assistant import VirtualAssistant


class TestVirtualAssistant():

    virtual_assistant = VirtualAssistant()

    @pytest.mark.parametrize(
        "command", 
        [
            "Hi, how are you?",
            "Hey, how are you doing today?",
        ]
    )
    def test_response_to_greeting_command(self, command):
        """Tests if the command routes to greeting responses."""

        keep_listening = self.virtual_assistant.respond_to_command(command)
        response = self.virtual_assistant.last_response

        assert keep_listening
        assert response == "I am well, thanks!"

    @pytest.mark.parametrize(
        "command", 
        [
            "Hi, what time is it?",
            # "Hey, what is the current time?",
            # "Tell me the time."
            "What time is it right now?"
            # "What's the time?"
        ]
    )
    def test_response_to_time_command(self, command):
        """Tests if the command routes to time responses."""

        keep_listening = self.virtual_assistant.respond_to_command(command)
        response = self.virtual_assistant.last_response

        assert keep_listening
        assert "The time is" in response

    @pytest.mark.parametrize(
        "command,expected", 
        [
            (
                "Where is Los Angeles",
                "Hold on, I will show you where Los Angeles is."
            ),
            (
                "Where is New York City",
                "Hold on, I will show you where New York City is."
            ),
        ]
    )
    def test_response_to_location_command(self, command, expected):
        """Tests if the command routes to location responses."""

        keep_listening = self.virtual_assistant.respond_to_command(command)
        response = self.virtual_assistant.last_response

        assert keep_listening
        assert response == expected

    @pytest.mark.parametrize(
        "command,expected", 
        [
            (
                "Search for Elon Musk's Wikipedia page",
                "Hold on, I am conducting a Google search for Elon Musk's Wikipedia page."
            ),
            (
                "Search for Leetcode",
                "Hold on, I am conducting a Google search for Leetcode."
            ),
        ]
    )
    def test_response_to_search_command(self, command, expected):
        """Tests if the command routes to search responses."""

        keep_listening = self.virtual_assistant.respond_to_command(command)
        response = self.virtual_assistant.last_response

        assert keep_listening
        assert response == expected

    @pytest.mark.parametrize(
        "command", 
        [
            "Hey, can you check the weather?",
            "Check the weather for me.",
            # "Give me the weather forecast.",
            # "What is the current weather?",
            # "Tell me the current weather forecast.",
        ]
    )
    def test_response_to_weather_command(self, command):
        """Tests if the command routes to weather responses."""

        keep_listening = self.virtual_assistant.respond_to_command(command)
        response = self.virtual_assistant.last_response

        assert keep_listening
        assert "The weather in" in response

    @pytest.mark.parametrize(
        "command,expected", 
        [
            (
                "Check ratings for The Karate Kid",
                "The Karate Kid (1984) has an IMDB Score of 7.3 and a Metascore of 60."
            ),
            (
                "Check ratings for The Silence of the Lambs",
                "The Silence of the Lambs (1991) has an IMDB Score of 8.6 and a Metascore of 85."
            ),
        ]
    )
    def test_response_to_ratings_command(self, command, expected):
        """Tests if the command routes to ratings responses."""

        keep_listening = self.virtual_assistant.respond_to_command(command)
        response = self.virtual_assistant.last_response

        assert keep_listening
        assert response == expected

    @pytest.mark.parametrize(
        "command,expected", 
        [
            (
                "Define sun",
                "The star that is the source of light and heat for the planets in the solar system"
            ),
            (
                "Define bug",
                "General term for any insect or similar creeping or crawling invertebrate"
            ),
        ]
    )
    def test_response_to_define_command(self, command, expected):
        """Tests if the command routes to define responses."""

        keep_listening = self.virtual_assistant.respond_to_command(command)
        response = self.virtual_assistant.last_response

        assert keep_listening
        assert expected in response

    @pytest.mark.parametrize(
        "command", 
        [
            "Perform a speed test",
        ]
    )
    def test_response_to_speedtest_command(self, command):
        """Tests if the command routes to speedtest responses."""

        keep_listening = self.virtual_assistant.respond_to_command(command)
        response = self.virtual_assistant.last_response

        assert keep_listening
        assert "megabytes per second" in response

    @pytest.mark.parametrize(
        "command", 
        [
            "Tell me the stock price of Tesla",
            "What is the current stock price of Apple",
        ]
    )
    def test_response_to_stock_price_command(self, command):
        """Tests if the command routes to stock price responses."""

        keep_listening = self.virtual_assistant.respond_to_command(command)
        response = self.virtual_assistant.last_response

        assert keep_listening
        assert "The stock price is $" in response

    @pytest.mark.parametrize(
        "command,expected", 
        [
            (
                "Translate Hello world to Spanish",
                "Hola Mundo"
            ),
            (
                "Translate Hello world to French",
                "Bonjour le monde"
            ),
        ]
    )
    def test_response_to_translate_command(self, command, expected):
        """Tests if the command routes to translate responses."""

        keep_listening = self.virtual_assistant.respond_to_command(command)
        response = self.virtual_assistant.last_response

        assert keep_listening
        assert response == expected

    @pytest.mark.parametrize(
        "command", 
        [
            "Print me the available commands.",
            "Hey can you print supported commands again?"
        ]
    )
    def test_response_to_print_command(self, command):
        """Tests if the command routes to print commands responses."""

        keep_listening = self.virtual_assistant.respond_to_command(command)
        response = self.virtual_assistant.last_response
        
        assert keep_listening
        assert response == "Okay, I will re-print available commands for you."

    @pytest.mark.parametrize(
        "command", 
        [
            "Thank you, goodbye!",
            "Okay, stop listening."
        ]
    )
    def test_response_to_goodbye_command(self, command):
        """Tests if the command routes to goodbye responses."""

        keep_listening = self.virtual_assistant.respond_to_command(command)
        response = self.virtual_assistant.last_response

        assert not keep_listening
        assert response == "Okay, goodbye!"
