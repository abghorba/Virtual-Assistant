
#!/bin/sh

if [ ! -d "env" ]; then
    echo "Creating virtual environment: env"
    python3 -m venv env
    source env/bin/activate
    echo "Installing dependencies..."
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