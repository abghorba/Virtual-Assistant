from gtts import gTTS
from playsound import playsound
from features import (
    GoogleHandler,
    SpeedTester,
    IMDbScraper,
    TranslatorHandler,
    WeatherHandler,
    YahooFinanceScraper,
    DictionarySearcher,
)

import speech_recognition as sr
import time


class VirtualAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.COMMANDS = [
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

    def get_commands(self):
        """
        Prints out the available commands to the user.

        :returns: None

        """
        print("Here are the following commands you may ask: ")
        for command in self.COMMANDS:
            print(command)
        time.sleep(1)

    def greet(self):
        """
        Responds with a greeting depending on the time of day.

        :returns: None

        """
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        if 6 <= current_hour <= 11:
            self.respond(
                "Good morning! I'm Marius, your virtual assistant. What can I do for you?"
            )
        elif 12 <= current_hour <= 16:
            self.respond(
                "Good afternoon! I'm Marius, your virtual assistant. What can I do for you?"
            )
        elif 17 <= current_hour < 20:
            self.respond(
                "Good evening! I'm Marius, your virtual assistant. What can I do for you?"
            )
        else:
            self.respond(
                "Good night! I'm Marius, your virtual assistant. What can I do for you?"
            )

    def listen(self):
        """
        Activates user's microphone and takes in the user's response.

        :returns: str

        """
        with sr.Microphone() as source:
            self.respond("I'm listening...")
            self.recognizer.pause_threshold = 1
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)
        data = ""
        try:
            data = self.recognizer.recognize_google(audio)
            print("You said: " + data)
        except sr.UnknownValueError:
            self.respond("I didn't quite get that.")
        except sr.RequestError as e:
            self.respond("Say that again please.")
        return data

    def respond(self, audio_string, language="en"):
        """
        Activates the voice response.

        :param audio_string: The audio string from the user.
        :type audio_string: str
        :returns: None

        """
        print(audio_string)
        tts = gTTS(text=audio_string, lang=language)
        tts.save("speech.mp3")
        playsound("speech.mp3")

    def digital_assistant(self, data):
        """
        Handles the responses for user commands.

        :param data: The spoken user command.
        :type data: str
        :returns: bool

        """
        listening = True

        if data:
            if "how are you" in data.lower():
                self.respond("I am well, thanks!")

            elif "what time is it" in data.lower():
                current_time = time.strftime("%I:%M %p")
                self.respond(f"The time is {current_time}.")

            elif "where is" in data.lower():
                data = data.split(" ")
                location = " ".join(data[2:])
                self.respond(f"Hold on, I will show you where {location} is.")

                try:
                    google = GoogleHandler()
                    url = google.google_maps_search(location)
                    google.open_webpage(url)
                except Exception as e:
                    self.respond(f"Sorry, I cannot find the location of {location}.")

            elif "search for" in data.lower():
                data = data.split(" ")
                query = data[2:]
                query = " ".join(query)
                self.respond(f"Hold on, I am conducting a Google search for {query}.")

                try:
                    google = GoogleHandler()
                    url = google.google_search(query)
                    google.open_webpage(url)
                except Exception as e:
                    self.respond(
                        f"Sorry, I cannot perform the Google search for {query}."
                    )

            elif "check the weather" in data.lower():
                self.respond("Okay, I am checking the weather for you right now.")
                try:
                    weather = WeatherHandler()
                    forecast = weather.check_weather()
                    self.respond(forecast)
                except Exception as e:
                    self.respond("Sorry, I cannot retrieve the weather information.")

            elif "check ratings for" in data.lower():
                data = data.split(" ")
                query = data[3:]
                query = " ".join(query)
                self.respond(f"Okay, I am checking the ratings for {query}.")
                try:
                    imdb = IMDbScraper()
                    review = imdb.get_movie_review(query)
                    self.respond(review)
                except Exception as e:
                    self.respond(f"Sorry, I cannot find the ratings for {query}.")

            elif "define" in data.lower():
                data = data.split(" ")
                word = data[1]
                self.respond(f"Okay, I am checking the definitions of {word}.")
                try:
                    dictionary = DictionarySearcher()
                    definitions = dictionary.search_definition(word)
                    self.respond(definitions)
                except Exception as e:
                    self.respond(
                        f"Sorry, I cannot find {word} in the English dictionary."
                    )

            elif "speed test" in data.lower():
                self.respond("Okay, I will perform a speed test for you.")
                try:
                    speedtest = SpeedTester()
                    results = speedtest.speed_check()
                    self.respond(results)
                except Exception as e:
                    self.respond("Sorry, I cannot perform a speed test.")

            elif "stock price" in data.lower():
                stock = data.split(" ")[-1]
                self.respond(f"Okay, I will find the stock price of {stock}")
                try:
                    yahoo = YahooFinanceScraper()
                    stock_price_info = yahoo.get_stock_price(data)
                    self.respond(stock_price_info)
                except:
                    self.respond(f"Sorry, I cannot find the stock price of {stock}.")

            elif "translate" in data.lower():
                data = data.split(" ")
                language = data[-1]
                text = " ".join(data[1:-2])
                self.respond(f"Okay, I will translate {text} to {language}.")
                try:
                    translator = TranslatorHandler()
                    translated, pronunciation, language_code = translator.translate(
                        text, language.lower()
                    )
                    if pronunciation is None:
                        print(translated)
                    else:
                        print(pronunciation)
                    self.respond(translated, language=language_code)
                except Exception as e:
                    self.respond("Sorry, I cannot do this translation.")

            elif "stop listening" in data.lower() or "goodbye" in data.lower():
                self.respond("Goodbye!")
                listening = False

        return listening


def main():
    assistant = VirtualAssistant()
    assistant.greet()
    listening = True
    assistant.get_commands()
    while listening == True:
        data = assistant.listen()
        listening = assistant.digital_assistant(data)


if __name__ == "__main__":
    main()
