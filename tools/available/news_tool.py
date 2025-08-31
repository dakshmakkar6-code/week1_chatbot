"""
News tool for real-time news data.
"""

import json
from datetime import datetime
from typing import List

import requests

from tools.base import BaseTool, ToolParameter


class NewsTool(BaseTool):
    @property
    def name(self) -> str:
        return "news"

    @property
    def description(self) -> str:
        return "Get real-time news headlines and articles from various sources."

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="topic",
                type="string",
                description="News topic or category (e.g., 'technology', 'business', 'sports', 'general')",
                required=False,
            ),
            ToolParameter(
                name="country",
                type="string",
                description="Country code for news (e.g., 'us', 'gb', 'jp') - optional",
                required=False,
            ),
            ToolParameter(
                name="count",
                type="string",
                description="Number of articles to fetch (1-10, default: 5)",
                required=False,
            ),
        ]

    def execute(
        self, topic: str = "general", country: str = "us", count: str = "5"
    ) -> str:
        """Execute the news tool."""
        try:
            # Use NewsAPI (free tier available)
            # api_key = "YOUR_NEWS_API_KEY"  # You'll need to get a free API key

            # For demo purposes, we'll use mock news data
            # In production, you would use: f"https://newsapi.org/v2/top-headlines?country={country}&category={topic}&apiKey={api_key}"

            try:
                article_count = int(count)
                article_count = min(max(article_count, 1), 10)  # Limit between 1-10
            except ValueError:
                article_count = 5

            # Mock news data for demonstration
            mock_news = {
                "technology": [
                    {
                        "title": "AI Breakthrough in Natural Language Processing",
                        "source": "TechNews",
                        "published": "2 hours ago",
                    },
                    {
                        "title": "New Quantum Computing Milestone Achieved",
                        "source": "ScienceDaily",
                        "published": "4 hours ago",
                    },
                    {
                        "title": "Major Tech Company Announces Revolutionary Product",
                        "source": "TechCrunch",
                        "published": "6 hours ago",
                    },
                    {
                        "title": "Cybersecurity Experts Warn of New Threats",
                        "source": "SecurityWeekly",
                        "published": "8 hours ago",
                    },
                    {
                        "title": "Startup Raises $50M for Green Technology",
                        "source": "VentureBeat",
                        "published": "10 hours ago",
                    },
                ],
                "business": [
                    {
                        "title": "Stock Market Reaches New All-Time High",
                        "source": "FinancialTimes",
                        "published": "1 hour ago",
                    },
                    {
                        "title": "Major Merger Announced in Tech Sector",
                        "source": "Bloomberg",
                        "published": "3 hours ago",
                    },
                    {
                        "title": "Central Bank Announces New Policy Changes",
                        "source": "Reuters",
                        "published": "5 hours ago",
                    },
                    {
                        "title": "Startup Ecosystem Shows Strong Growth",
                        "source": "Forbes",
                        "published": "7 hours ago",
                    },
                    {
                        "title": "Global Supply Chain Improvements Reported",
                        "source": "WSJ",
                        "published": "9 hours ago",
                    },
                ],
                "sports": [
                    {
                        "title": "Championship Game Ends in Dramatic Victory",
                        "source": "ESPN",
                        "published": "30 minutes ago",
                    },
                    {
                        "title": "Olympic Athlete Breaks World Record",
                        "source": "Olympics",
                        "published": "2 hours ago",
                    },
                    {
                        "title": "Team Announces Major Roster Changes",
                        "source": "SportsCenter",
                        "published": "4 hours ago",
                    },
                    {
                        "title": "New Stadium Construction Begins",
                        "source": "LocalNews",
                        "published": "6 hours ago",
                    },
                    {
                        "title": "Sports League Announces Rule Changes",
                        "source": "LeagueOffice",
                        "published": "8 hours ago",
                    },
                ],
                "general": [
                    {
                        "title": "Global Climate Summit Reaches Historic Agreement",
                        "source": "WorldNews",
                        "published": "1 hour ago",
                    },
                    {
                        "title": "New Medical Breakthrough Announced",
                        "source": "HealthNews",
                        "published": "3 hours ago",
                    },
                    {
                        "title": "Education Reform Bill Passes Senate",
                        "source": "PoliticsDaily",
                        "published": "5 hours ago",
                    },
                    {
                        "title": "Cultural Festival Draws Record Crowds",
                        "source": "CultureMag",
                        "published": "7 hours ago",
                    },
                    {
                        "title": "Space Mission Successfully Launched",
                        "source": "SpaceNews",
                        "published": "9 hours ago",
                    },
                ],
            }

            news_list = mock_news.get(topic.lower(), mock_news["general"])
            selected_news = news_list[:article_count]

            result = f"📰 Latest {topic.title()} News ({country.upper()}):\n\n"

            for i, article in enumerate(selected_news, 1):
                result += f"{i}. **{article['title']}**\n"
                result += f"   📰 {article['source']} • {article['published']}\n\n"

            result += (
                f"*Showing {len(selected_news)} of {len(news_list)} available articles*"
            )

            return result.strip()

        except Exception as e:
            return f"Error fetching news: {str(e)}"
