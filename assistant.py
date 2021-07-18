from gtts import gTTS
from mpyg321.mpyg321 import MPyg321Player
from time import ctime, sleep

import json
import requests
import speech_recognition as sr


class VirtualAssistant():
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.audio_player = MPyg321Player()


    def listen(self):
        """
        Activates user's machine and takes in the user's response.
        
        :returns: None

        """
        with sr.Microphone() as source:
            self.respond("I'm listening...", 2)
            audio = self.recognizer.listen(source)
        data = ""
        try:
            data = self.recognizer.recognize_google(audio)
            print("You said: " + data)
        except sr.UnknownValueError:
            print("Google Speech Recognition did not understand audio")
        except sr.RequestError as e:
            print("Request Failed; {0}".format(e))
        return data


    def respond(self, audio_string, seconds=1):
        """
        Activates the voice response.
        
        :param audio_string: The audio string from the user.
        :type audio_string: str
        :param seconds: Number of seconds to wait.
        :type seconds: int
        :returns: None
        
        """
        print(audio_string)
        tts = gTTS(text=audio_string, lang='en')
        tts.save("speech.mp3")
        self.audio_player.play_song("speech.mp3")
        sleep(seconds)


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
                self.respond("I am well, thanks!", 3)

            if "what time is it" in data:
                listening = True
                self.respond(ctime(), 5)
                
            if "stop listening" in data:
                listening = False
                self.respond("Listening stopped. Goodbye!", 3)
        else:
            self.respond("Not a valid command. Please try again.", 3)
            listening = True

        return listening


def main():
    assistant = VirtualAssistant()
    assistant.respond("Hi, what can I do for you?", 3)
    listening = True
    while listening == True:
        data = assistant.listen()
        listening = assistant.digital_assistant(data)


if __name__ == "__main__":
    main()