
#!/bin/sh

if [ ! -d "env" ]; then

    echo "Creating virtual environment: env"
    python3 -m venv env

    # Need homebrew to install portaudio
    which -s brew
    if [ $? != 0 ] ; then
        echo "Homebrew not found on system. Installing..."
        # Install Homebrew
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        echo "Homebrew installed!"
    fi

    echo "Installing dependencies..."
    brew install portaudio
    source env/bin/activate
    pip install -r requirements.txt
    echo "Done!"
fi

OPEN_WEATHER_API_KEY=""
if [ ! -f ".env" ]; then
    echo "Creating .env file to store environment variables..."
    touch .env
    echo "OPEN_WEATHER_API_KEY = \"$OPEN_WEATHER_API_KEY\"" >> .env
    echo "Done!"
fi