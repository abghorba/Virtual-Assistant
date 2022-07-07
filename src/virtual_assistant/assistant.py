import speech_recognition as sr
import time

from datetime import datetime
from gtts import gTTS
from playsound import playsound
from src.features.dictionary import DictionarySearcher
from src.features.google import GoogleHandler
from src.features.imdb import IMDbScraper
from src.features.speedtest import SpeedTester
from src.features.translate import TranslatorHandler
from src.features.weather import WeatherHandler
from src.features.yahoo_finance import YahooFinanceScraper


class VirtualAssistant():

    def __init__(self, audio_on=False, open_webpages=False):
        """
        Initializes the virtual assistant

        :param audio_on: Audio response will play if True; default False
        :param open_webpages: Webpages will open if True; default False
        """
        
        # Toggle audio
        self.audio_on = audio_on

        # Toggle opening webpages
        self.open_webpage = open_webpages

        # Initialize features
        self.recognizer = sr.Recognizer()
        self.dictionary = DictionarySearcher()
        self.google = GoogleHandler()
        self.imdb = IMDbScraper()
        self.speedtest = SpeedTester()
        self.translator = TranslatorHandler()
        self.weather = WeatherHandler()
        self.yahoo_finance = YahooFinanceScraper()

        self.ACCEPTED_COMMANDS = [
            "how are you?",
            "what time is it?",
            "where is <location>?",
            "search for <query>",
            "check the weather",
            "check ratings for <movie>",
            "perform a speed test",
            "define <English word>",
            "stock price of <company>",
            "translate <text> to <language>",
        ]

        # For testing purposes, save the last response.
        self.last_response = ""

    def print_commands(self):
        """Prints out the available commands to the user."""

        print("Here are the following commands you may ask: ")

        for command in self.ACCEPTED_COMMANDS:
            print(command)

        time.sleep(1)

    def respond(self, audio_string, language="en"):
        """
        Activates the voice response

        :param audio_string: Audio string from the user
        :param language: Chosen language code for responses, default English
        :return: None
        """

        self.last_response = audio_string   

        print("Marius: " + audio_string)
        tts = gTTS(text=audio_string, lang=language)
        tts.save("speech.mp3")

        if self.audio_on:
            playsound("speech.mp3")

    def greet(self):
        """Responds with a greeting depending on the time of day"""

        current_time = time.localtime()
        current_hour = current_time.tm_hour

        if 5 <= current_hour <= 11:
            time_of_day = "Morning"
        elif 12 <= current_hour <= 16:
            time_of_day = "Afternoon"
        else:
            time_of_day = "Evening"

        self.respond(f"Good {time_of_day}! I'm Marius, your virtual assistant. What can I do for you?")

    def listen(self):
        """Activates user's microphone and returns the user's command as a string"""

        with sr.Microphone() as source:
            self.respond("I'm listening...")
            self.recognizer.pause_threshold = 1
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)

        try:
            command_in_text = self.recognizer.recognize_google(audio)
            print("You said: " + command_in_text)
            return command_in_text

        except sr.UnknownValueError:
            self.respond("I didn't quite get that.")

        except sr.RequestError as e:
            self.respond("Say that again please.")

    def respond_to_command(self, command):
        """
        Handles the responses for user commands

        :param command: The spoken user command in text
        :return: True, if user wishes to continue; False otherwise
        """

        keep_listening = True

        if not command:
            raise Exception("No command given.")

        if "how are you" in command.lower():
            self.respond("I am well, thanks!")

        elif "what time is it" in command.lower():
            current_time = time.strftime("%I:%M %p")
            self.respond(f"The time is {current_time}.")

        elif "where is" in command.lower():
            command = command.split(" ")
            location = " ".join(command[2:])

            self.respond(f"Hold on, I will show you where {location} is.")

            try:
                url = self.google.google_maps_search(location)

                if self.open_webpage:
                    self.google.open_webpage(url)

            except Exception:
                self.respond(f"Sorry, I cannot find the location of {location}.")

        elif "search for" in command.lower():
            command = command.split(" ")
            query = command[2:]
            query = " ".join(query)

            self.respond(f"Hold on, I am conducting a Google search for {query}.")

            try:
                url = self.google.google_search(query)
                
                if self.open_webpage:
                    self.google.open_webpage(url)

            except Exception:
                self.respond(
                    f"Sorry, I cannot perform a Google search for {query}."
                )

        elif "check the weather" in command.lower():
            self.respond("Okay, I am checking the weather for you right now.")

            try:
                forecast = self.weather.check_weather()
                self.respond(forecast)

            except Exception:
                self.respond("Sorry, I cannot retrieve the weather information.")

        elif "check ratings for" in command.lower():
            command = command.split(" ")
            query = command[3:]
            query = " ".join(query)

            self.respond(f"Okay, I am checking the ratings for {query}.")

            try:
                review = self.imdb.get_movie_review(query)
                self.respond(review)

            except Exception:
                self.respond(f"Sorry, I cannot find the ratings for {query}.")

        elif "define" in command.lower():
            command = command.split(" ")
            word = command[1]

            self.respond(f"Okay, I am checking the definitions of {word}.")

            try:
                definitions = self.dictionary.search_definition(word)
                self.respond(definitions)

            except Exception:
                self.respond(
                    f"Sorry, I cannot find {word} in the English dictionary."
                )

        elif "speed test" in command.lower():
            self.respond("Okay, I will perform a speed test for you.")

            try:
                results = self.speedtest.speed_check()
                self.respond(results)

            except Exception:
                self.respond("Sorry, I cannot perform a speed test.")

        elif "stock price" in command.lower():
            stock = command.split(" ")[-1]

            self.respond(f"Okay, I will find the stock price of {stock}")

            try:
                stock_price_info = self.yahoo_finance.get_stock_price(command)
                self.respond(stock_price_info)

            except:
                self.respond(f"Sorry, I cannot find the stock price of {stock}.")

        elif "translate" in command.lower():

            command = command.split(" ")
            language = command[-1]
            text = " ".join(command[1:-2])

            self.respond(f"Okay, I will translate {text} to {language}.")

            try:
                translated, pronunciation, language_code = \
                    self.translator.translate(text, language.lower())

                if pronunciation is None:
                    print(translated)
                else:
                    print(pronunciation)

                self.respond(translated, language=language_code)

            except Exception as e:
                self.respond("Sorry, I cannot do this translation.")

        elif "stop listening" in command.lower() or "goodbye" in command.lower():
            self.respond("Okay, goodbye!")
            keep_listening = False

        elif "print" in command.lower() and "command" in command.lower():
            self.respond("Okay, I will re-print available commands for you.")
            self.print_commands()

        else:
            self.respond("That's not a valid command. Try again.")

        return keep_listening

    def activate(self):
        """Activates the virtual assistant"""

        keep_listening = True

        while keep_listening:
            command = self.listen()
            keep_listening = self.respond_to_command(command)


def main():
    assistant = VirtualAssistant(audio_on=True, open_webpages=True)
    assistant.greet()
    assistant.print_commands()
    assistant.activate()

if __name__ == "__main__":
    main()
