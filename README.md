# Virtual Assistant
A virtual assistant built in Python which allows the user to speak commands and receive voice responses.

<h2> Setting Up </h2>
In order to use the full features of the virtual assistant, you must create a file called config.py and insert the following line of code,
replacing YOUR_API_KEY with an API key received from https://openweathermap.org/api

        OPEN_WEATHER_API_KEY = YOUR_API_KEY

Then, download the dependencies from requirements.txt:

        pip install -r requirements.txt

<h2> Usage </h2>
Now that we have everything set up, we are ready to go!

You can run the virtual assistant by using the command

        python assistant.py

The virtual assistant supports the following commands:

        how are you?
        what time is it?
        where is [location]
        search for [query]
        check the weather
        check ratings for [movie]
        perform a speed test
        define [English word]
        stock price of [company]

Make sure you have a microphone to speak into! You will be able to speak the commands and will get a voice response along with a transcript on the command line.

Have fun!