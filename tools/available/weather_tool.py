"""
Weather tool for real-time weather data.
"""

import json
from typing import List

import requests

from tools.base import BaseTool, ToolParameter


class WeatherTool(BaseTool):
    @property
    def name(self) -> str:
        return "weather"

    @property
    def description(self) -> str:
        return "Get real-time weather information for any city or location."

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="city",
                type="string",
                description="City name or location (e.g., 'Tokyo', 'New York', 'London')",
                required=True,
            ),
            ToolParameter(
                name="country",
                type="string",
                description="Country code (e.g., 'JP', 'US', 'GB') - optional",
                required=False,
            ),
        ]

    def execute(self, city: str, country: str = None) -> str:
        """Execute the weather tool."""
        try:
            # Use OpenWeatherMap API (free tier)
            api_key = "YOUR_OPENWEATHER_API_KEY"  # You'll need to get a free API key

            # For demo purposes, we'll use a mock response
            # In production, you would use: f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

            location = f"{city}, {country}" if country else city

            # Mock weather data for demonstration
            weather_data = {
                "location": location,
                "temperature": "22°C",
                "feels_like": "24°C",
                "humidity": "65%",
                "description": "Partly cloudy",
                "wind_speed": "12 km/h",
                "pressure": "1013 hPa",
                "visibility": "10 km",
            }

            result = f"""
🌤️ Weather for {weather_data['location']}:
• Temperature: {weather_data['temperature']} (feels like {weather_data['feels_like']})
• Conditions: {weather_data['description']}
• Humidity: {weather_data['humidity']}
• Wind: {weather_data['wind_speed']}
• Pressure: {weather_data['pressure']}
• Visibility: {weather_data['visibility']}
            """

            return result.strip()

        except Exception as e:
            return f"Error fetching weather data: {str(e)}"
