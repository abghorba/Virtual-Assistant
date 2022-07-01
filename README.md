# Virtual Assistant
A virtual assistant built in Python which allows the user to speak commands and receive voice responses.

<h2> Setting Up </h2>
In order to use the full features of the virtual assistant, you must get an API key from https://openweathermap.org/api
and replace the following in initialize.sh

        OPEN_WEATHER_API_KEY=""

After this is done, you can create a virtual environment, install dependencies, and create your .env file by running:

        sh initialize.sh


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
        translate [text] to [language]

Make sure you have a microphone to speak into! You will be able to speak the commands and will get a voice response along with a transcript on the command line.

Have fun!