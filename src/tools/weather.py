"""
Weather Tool
Gets current weather for a location using Open-Meteo API (free, no key needed)

ANALOGY: A window the agent can look out of.
Except this window can show any city in the world.
"""
import requests

def get_weather(location):
    """
    Get current weather for a location

    Input:  "Paris"
    Output: {"location": "Paris", "temperature_f": 64.4, "temperature_c": 18.0, ...}
    """
    try:
        # Step 1: Geocode the location name to coordinates
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1}
        )
        geo_data = geo_response.json()

        if "results" not in geo_data:
            return {"error": f"Location '{location}' not found"}

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        name = geo_data["results"][0]["name"]
        country = geo_data["results"][0].get("country", "")

        # Step 2: Get weather at those coordinates
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True
            }
        )
        weather_data = weather_response.json()
        current = weather_data["current_weather"]

        temp_c = current["temperature"]
        temp_f = round((temp_c * 9 / 5) + 32, 1)

        return {
            "location": f"{name}, {country}",
            "temperature_c": temp_c,
            "temperature_f": temp_f,
            "windspeed_kmh": current["windspeed"],
            "description": _weather_code(current["weathercode"])
        }
    except Exception as e:
        return {"error": str(e)}


def _weather_code(code):
    """Convert WMO weather code to description"""
    codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy",
        3: "Overcast", 45: "Foggy", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        80: "Slight rain showers", 81: "Moderate rain showers",
        82: "Violent rain showers", 95: "Thunderstorm"
    }
    return codes.get(code, f"Unknown ({code})")
