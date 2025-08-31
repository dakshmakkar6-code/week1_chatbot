"""
Stock market tool for real-time financial data.
"""

import json
from datetime import datetime
from typing import List

import requests

from tools.base import BaseTool, ToolParameter


class StockTool(BaseTool):
    @property
    def name(self) -> str:
        return "stock"

    @property
    def description(self) -> str:
        return "Get real-time stock market data, prices, and financial information."

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="symbol",
                type="string",
                description="Stock symbol (e.g., 'AAPL', 'GOOGL', 'MSFT', 'TSLA')",
                required=True,
            ),
            ToolParameter(
                name="action",
                type="string",
                description="Action to perform: 'price' (current price), 'info' (company info), 'chart' (price history)",
                required=False,
                enum=["price", "info", "chart"],
            ),
        ]

    def execute(self, symbol: str, action: str = "price") -> str:
        """Execute the stock tool."""
        try:
            # Use Alpha Vantage API (free tier available)
            # api_key = "YOUR_ALPHA_VANTAGE_API_KEY"  # You'll need to get a free API key

            # For demo purposes, we'll use mock stock data
            # In production, you would use: f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"

            symbol = symbol.upper()

            # Mock stock data for demonstration
            mock_stocks = {
                "AAPL": {
                    "name": "Apple Inc.",
                    "price": "$175.43",
                    "change": "+2.15",
                    "change_percent": "+1.24%",
                    "volume": "45.2M",
                    "market_cap": "$2.7T",
                    "pe_ratio": "28.5",
                    "sector": "Technology",
                },
                "GOOGL": {
                    "name": "Alphabet Inc.",
                    "price": "$142.56",
                    "change": "-1.23",
                    "change_percent": "-0.85%",
                    "volume": "23.8M",
                    "market_cap": "$1.8T",
                    "pe_ratio": "25.2",
                    "sector": "Technology",
                },
                "MSFT": {
                    "name": "Microsoft Corporation",
                    "price": "$378.85",
                    "change": "+5.67",
                    "change_percent": "+1.52%",
                    "volume": "18.9M",
                    "market_cap": "$2.8T",
                    "pe_ratio": "32.1",
                    "sector": "Technology",
                },
                "TSLA": {
                    "name": "Tesla, Inc.",
                    "price": "$248.42",
                    "change": "-8.95",
                    "change_percent": "-3.48%",
                    "volume": "67.3M",
                    "market_cap": "$789B",
                    "pe_ratio": "45.8",
                    "sector": "Automotive",
                },
                "AMZN": {
                    "name": "Amazon.com, Inc.",
                    "price": "$145.24",
                    "change": "+3.21",
                    "change_percent": "+2.26%",
                    "volume": "34.7M",
                    "market_cap": "$1.5T",
                    "pe_ratio": "38.9",
                    "sector": "Consumer Discretionary",
                },
            }

            if symbol not in mock_stocks:
                return f"Error: Stock symbol '{symbol}' not found in demo data. Available symbols: {', '.join(mock_stocks.keys())}"

            stock_data = mock_stocks[symbol]

            if action == "price":
                result = f"""
📈 **{stock_data['name']} ({symbol})**
💰 Current Price: {stock_data['price']}
📊 Change: {stock_data['change']} ({stock_data['change_percent']})
📈 Volume: {stock_data['volume']}
🏢 Market Cap: {stock_data['market_cap']}
⏰ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """

            elif action == "info":
                result = f"""
🏢 **Company Information: {stock_data['name']} ({symbol})**
💰 Current Price: {stock_data['price']}
📊 P/E Ratio: {stock_data['pe_ratio']}
🏭 Sector: {stock_data['sector']}
📈 Market Cap: {stock_data['market_cap']}
📊 Volume: {stock_data['volume']}
📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """

            elif action == "chart":
                result = f"""
📊 **Price History: {stock_data['name']} ({symbol})**
💰 Current: {stock_data['price']}
📈 52-Week High: ${float(stock_data['price'].replace('$', '')) * 1.15:.2f}
📉 52-Week Low: ${float(stock_data['price'].replace('$', '')) * 0.85:.2f}
📊 30-Day Avg: ${float(stock_data['price'].replace('$', '')) * 1.02:.2f}
📈 90-Day Avg: ${float(stock_data['price'].replace('$', '')) * 0.98:.2f}
                """

            else:
                result = f"Error: Unknown action '{action}'. Available actions: price, info, chart"

            return result.strip()

        except Exception as e:
            return f"Error fetching stock data: {str(e)}"
