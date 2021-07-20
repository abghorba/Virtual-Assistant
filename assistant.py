from bs4 import BeautifulSoup
from googlehandler import GoogleHandler
from gtts import gTTS
from playsound import playsound

import json
import os
import requests
import speech_recognition as sr
import time


class VirtualAssistant():
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()


    def greet(self):
        """
            Responds with a greeting depending on the time of day.
            
            :returns: None

        """
        current_time = time.localtime()
        current_hour = current_time.tm_hour
        if 6 <= current_hour <= 11:
            self.respond("Good morning! I'm Marius, your virtual assistant. What can I do for you?")
        elif 12 <= current_hour <= 16:
            self.respond("Good afternoon! I'm Marius, your virtual assistant. What can I do for you?")
        elif 17 <= current_hour < 20:
            self.respond("Good evening! I'm Marius, your virtual assistant. What can I do for you?")
        else:
            self.respond("Good night! I'm Marius, your virtual assistant. What can I do for you?")


    def listen(self):
        """
            Activates user's microphone and takes in the user's response.
            
            :returns: None

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


    def respond(self, audio_string):
        """
            Activates the voice response.
            
            :param audio_string: The audio string from the user.
            :type audio_string: str
            :returns: None
            
        """
        print(audio_string)
        tts = gTTS(text=audio_string, lang='en')
        tts.save("speech.mp3")
        playsound("speech.mp3")


    def digital_assistant(self, data):
        """
            Handles the responses for user commands.

            :param data: The spoken user command.
            :type data: str
            :returns: None
            
        """
        if data:
            if "how are you" in data:
                listening = True
                self.respond("I am well, thanks!")

            if "what time is it" in data:
                listening = True
                current_time = time.strftime("%I:%M %p")
                self.respond(f"The time is {current_time}")
                
            if "stop listening" in data:
                listening = False
                self.respond("Goodbye!")

            if "where is" in data:
                listening = True
                data = data.split(" ")
                location = data[2]

                self.respond(f"Hold on, I will show you where {location} is.")

                googl = GoogleHandler()
                googl.google_maps_search(location)

            if "search for" in data:
                listening = True
                data = data.split(" ")
                query = data[2:]
                query = " ".join(query)

                self.respond(f"Hold on, I am conducting a Google search for {query}")

                googl = GoogleHandler()
                googl.google_search(query)                

        else:
            listening = True

        return listening


def main():
    assistant = VirtualAssistant()
    assistant.greet()
    listening = True
    while listening == True:
        data = assistant.listen()
        listening = assistant.digital_assistant(data)


if __name__ == "__main__":
    main()