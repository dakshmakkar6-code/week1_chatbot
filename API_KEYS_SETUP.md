# API Keys Setup Guide

To enable real-time data access in your chatbot, you'll need to get free API keys from these services:

## 🌤️ Weather Data (OpenWeatherMap)
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key
4. Replace `YOUR_OPENWEATHER_API_KEY` in `tools/available/weather_tool.py`

## 📰 News Data (NewsAPI)
1. Go to [NewsAPI](https://newsapi.org/)
2. Sign up for a free account (1000 requests/day)
3. Get your API key
4. Replace `YOUR_NEWS_API_KEY` in `tools/available/news_tool.py`

## 📈 Stock Data (Alpha Vantage)
1. Go to [Alpha Vantage](https://www.alphavantage.co/)
2. Sign up for a free account (500 requests/day)
3. Get your API key
4. Replace `YOUR_ALPHA_VANTAGE_API_KEY` in `tools/available/stock_tool.py`

## 🔧 How to Update the Tools

For each tool, find the commented line with the API key and replace it:

```python
# Replace this line:
api_key = "YOUR_API_KEY_HERE"

# With your actual API key:
api_key = "your_actual_api_key_here"
```

## 🚀 Current Status

Your chatbot currently uses **mock data** for demonstration purposes. Once you add real API keys, you'll get:

- **Real-time weather** for any city
- **Live news headlines** from major sources
- **Current stock prices** and market data
- **Live financial information**

## 📊 Available Real-time Features

### Weather Tool
- Current temperature, humidity, wind speed
- Weather conditions and forecasts
- Support for any city worldwide

### News Tool
- Latest headlines by category (tech, business, sports, etc.)
- News from different countries
- Article summaries and sources

### Stock Tool
- Real-time stock prices
- Company information and financial data
- Price history and market trends

## 🔒 Security Note

Never commit your API keys to version control. Consider using environment variables:

```python
import os
api_key = os.getenv("OPENWEATHER_API_KEY")
```

Then add to your `.env` file:
```
OPENWEATHER_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
ALPHA_VANTAGE_API_KEY=your_key_here
```
