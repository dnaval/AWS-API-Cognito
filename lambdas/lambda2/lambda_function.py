import json
import os
import urllib.request

def lambda_handler(event, context):

    city = "Calgary"
    api_key = os.environ['OPENWEATHER_API_KEY']

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())

        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        result = {
            "city": city,
            "weather": weather,
            "temperature_celsius": temperature,
            "humidity": humidity,
            "wind_speed": wind,
            "message": f"The weather in {city} is {weather} with temperature {temperature}°C."
        }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }