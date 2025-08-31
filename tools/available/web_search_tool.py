"""
Web search tool for real-time web search results.
"""

import json
from datetime import datetime
from typing import List

import requests

from tools.base import BaseTool, ToolParameter


class WebSearchTool(BaseTool):
    @property
    def name(self) -> str:
        return "web_search"

    @property
    def description(self) -> str:
        return "Search the web for current information and real-time data."

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="query",
                type="string",
                description="Search query to look up on the web",
                required=True,
            ),
            ToolParameter(
                name="num_results",
                type="string",
                description="Number of results to return (1-10, default: 5)",
                required=False,
            ),
        ]

    def execute(self, query: str, num_results: str = "5") -> str:
        """Execute the web search tool."""
        try:
            # Use DuckDuckGo Instant Answer API (free, no API key needed)
            # For demo purposes, we'll use mock search results
            # In production, you would use: f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"

            try:
                result_count = int(num_results)
                result_count = min(max(result_count, 1), 10)  # Limit between 1-10
            except ValueError:
                result_count = 5

            # Mock search results for demonstration
            mock_results = {
                "python programming": [
                    {
                        "title": "Python Programming Language - Official Website",
                        "url": "https://www.python.org",
                        "snippet": "Python is a programming language that lets you work quickly and integrate systems more effectively.",
                    },
                    {
                        "title": "Python Tutorial - W3Schools",
                        "url": "https://www.w3schools.com/python",
                        "snippet": "Learn Python programming with our comprehensive tutorial covering basics to advanced concepts.",
                    },
                    {
                        "title": "Python Documentation",
                        "url": "https://docs.python.org",
                        "snippet": "Official Python documentation with tutorials, library references, and language reference.",
                    },
                    {
                        "title": "Real Python - Tutorials",
                        "url": "https://realpython.com",
                        "snippet": "Learn Python programming with practical examples and real-world projects.",
                    },
                    {
                        "title": "Python for Beginners",
                        "url": "https://wiki.python.org/moin/BeginnersGuide",
                        "snippet": "A comprehensive guide for beginners to start learning Python programming.",
                    },
                ],
                "artificial intelligence": [
                    {
                        "title": "What is Artificial Intelligence (AI)?",
                        "url": "https://www.ibm.com/ai",
                        "snippet": "Artificial intelligence leverages computers and machines to mimic the problem-solving and decision-making capabilities of the human mind.",
                    },
                    {
                        "title": "AI Research - OpenAI",
                        "url": "https://openai.com/research",
                        "snippet": "OpenAI conducts research on artificial intelligence and develops AI systems for the benefit of humanity.",
                    },
                    {
                        "title": "Machine Learning - Google",
                        "url": "https://ai.google",
                        "snippet": "Google's approach to artificial intelligence and machine learning research and development.",
                    },
                    {
                        "title": "AI Ethics and Safety",
                        "url": "https://futureoflife.org",
                        "snippet": "Research and advocacy for AI safety and beneficial artificial intelligence development.",
                    },
                    {
                        "title": "Deep Learning Fundamentals",
                        "url": "https://deeplearning.ai",
                        "snippet": "Learn the fundamentals of deep learning and neural networks.",
                    },
                ],
                "weather": [
                    {
                        "title": "Weather.com - Current Weather",
                        "url": "https://weather.com",
                        "snippet": "Get current weather conditions, forecasts, and weather maps for locations worldwide.",
                    },
                    {
                        "title": "AccuWeather - Weather Forecast",
                        "url": "https://accuweather.com",
                        "snippet": "Accurate weather forecasts and current weather conditions for your location.",
                    },
                    {
                        "title": "National Weather Service",
                        "url": "https://weather.gov",
                        "snippet": "Official weather forecasts and warnings from the National Weather Service.",
                    },
                    {
                        "title": "Weather Underground",
                        "url": "https://wunderground.com",
                        "snippet": "Weather forecasts, reports, maps and tropical weather conditions for locations worldwide.",
                    },
                    {
                        "title": "Weather Radar and Maps",
                        "url": "https://radar.weather.gov",
                        "snippet": "Interactive weather radar maps and current weather conditions.",
                    },
                ],
                "stock market": [
                    {
                        "title": "Yahoo Finance - Stock Market",
                        "url": "https://finance.yahoo.com",
                        "snippet": "Get real-time stock quotes, financial news, and market data.",
                    },
                    {
                        "title": "MarketWatch - Financial Markets",
                        "url": "https://marketwatch.com",
                        "snippet": "Latest stock market news, financial data, and market analysis.",
                    },
                    {
                        "title": "Bloomberg - Markets",
                        "url": "https://bloomberg.com/markets",
                        "snippet": "Real-time financial market data, stock quotes, and business news.",
                    },
                    {
                        "title": "CNBC - Stock Market News",
                        "url": "https://cnbc.com/markets",
                        "snippet": "Latest stock market news and financial information.",
                    },
                    {
                        "title": "Reuters - Markets",
                        "url": "https://reuters.com/markets",
                        "snippet": "Financial market news, stock quotes, and economic data.",
                    },
                ],
            }

            # Find matching results or use general search
            search_results = []
            query_lower = query.lower()

            for key, results in mock_results.items():
                if key in query_lower or query_lower in key:
                    search_results = results
                    break

            if not search_results:
                # Default results for any query
                search_results = [
                    {
                        "title": f"Search Results for: {query}",
                        "url": "https://duckduckgo.com",
                        "snippet": f"Find information about {query} on the web.",
                    },
                    {
                        "title": "Wikipedia",
                        "url": "https://wikipedia.org",
                        "snippet": "Free encyclopedia with articles on various topics.",
                    },
                    {
                        "title": "Google Search",
                        "url": "https://google.com",
                        "snippet": "Search the web for information and resources.",
                    },
                    {
                        "title": "Bing Search",
                        "url": "https://bing.com",
                        "snippet": "Web search engine with news, images, and videos.",
                    },
                    {
                        "title": "DuckDuckGo",
                        "url": "https://duckduckgo.com",
                        "snippet": "Privacy-focused search engine that doesn't track users.",
                    },
                ]

            selected_results = search_results[:result_count]

            result = f"🔍 Web Search Results for: **{query}**\n\n"

            for i, item in enumerate(selected_results, 1):
                result += f"{i}. **{item['title']}**\n"
                result += f"   🔗 {item['url']}\n"
                result += f"   📝 {item['snippet']}\n\n"

            result += f"*Showing {len(selected_results)} of {len(search_results)} available results*"

            return result.strip()

        except Exception as e:
            return f"Error performing web search: {str(e)}"
