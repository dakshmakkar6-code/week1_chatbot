# Advanced CLI Chatbot with OpenAI Integration

A powerful, modular CLI chatbot that connects to OpenAI's Chat API with comprehensive tool support and real-time data capabilities. Features beautiful formatting using Rich and a modular architecture for easy tool registration.

## 🌟 Features

* 🤖 **OpenAI/OpenRouter Integration** - Support for both OpenAI and OpenRouter APIs
* 🎨 **Beautiful CLI Interface** - Rich formatting with panels, tables, and markdown
* 🔧 **Modular Tool System** - Easy extensibility with auto-discovery
* 📁 **Auto-discovery of Tools** - Automatically finds tools from directory structure
* ⚙️ **Environment-based Configuration** - Flexible configuration management
* 💬 **Interactive Chat** - Full conversation history and context
* 🔍 **Real-time Data Access** - Weather, news, stocks, web search
* 📊 **Advanced Tool Registry** - Comprehensive tool management and validation
* 🛡️ **Error Handling** - Robust error handling throughout the system

## 🚀 Quick Start

### Option 1: Using uv (Recommended)

1. **Install uv:**
   ```bash
   pip install uv
   ```

2. **Clone and set up:**
   ```bash
   git clone <your-repo-url>
   cd week1-chatbot
   uv sync --dev
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

4. **Run the chatbot:**
   ```bash
   uv run python main.py
   ```

### Option 2: Using pip

1. **Clone and install dependencies:**
   ```bash
   git clone <your-repo-url>
   cd week1-chatbot
   pip install -e ".[dev]"
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

3. **Run the chatbot:**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

Configure the chatbot using environment variables in your `.env` file:

* `OPENROUTER_API_KEY` or `OPENAI_API_KEY`: Your API key (required)
* `OPENAI_MODEL`: Model to use (default: gpt-4o-mini)
* `MAX_TOKENS`: Maximum tokens per response (default: 1000)
* `TEMPERATURE`: Response creativity (0.0-2.0, default: 0.7)
* `SYSTEM_PROMPT`: Custom system prompt

## 🛠️ Available Tools

The chatbot comes with several powerful built-in tools:

### 🌤️ Weather Tool
* **Function**: `weather`
* **Description**: Get real-time weather information for any city
* **Example**: "What's the weather in Tokyo?"

### 📰 News Tool
* **Function**: `news`
* **Description**: Get latest news headlines by category
* **Example**: "Show me latest technology news"

### 📈 Stock Tool
* **Function**: `stock`
* **Description**: Get real-time stock prices and financial data
* **Example**: "Stock price for AAPL"

### 🧮 Calculator Tool
* **Function**: `calculator`
* **Description**: Perform complex mathematical calculations
* **Example**: "Calculate 2^10 + sqrt(144)"

### 📅 DateTime Tool
* **Function**: `datetime`
* **Description**: Get current time, timezone conversions, date calculations
* **Example**: "Current time in New York"

### 📁 File Operations Tool
* **Function**: `file_operations`
* **Description**: Read, write, list files, get file information
* **Example**: "List files in current directory"

### 🔍 Web Search Tool
* **Function**: `web_search`
* **Description**: Search the web for current information
* **Example**: "Search for Python programming tutorials"

## 🎯 Commands

While chatting, you can use these special commands:

* `help` - Show available commands and tools
* `tools` - List all registered tools
* `tool-details` - Show detailed tool information
* `clear` - Clear conversation history
* `stats` - Show conversation statistics
* `save` - Save conversation to file
* `config` - Show current configuration
* `reset` - Reset chatbot to initial state
* `quit` or `exit` - Exit the chatbot

## 🔧 Creating Custom Tools

To create a custom tool:

1. Create a new Python file in `tools/available/`
2. Inherit from `BaseTool` and implement required methods:

```python
from typing import List
from tools.base import BaseTool, ToolParameter

class MyCustomTool(BaseTool):
    @property
    def name(self) -> str:
        return "my_tool"
    
    @property
    def description(self) -> str:
        return "Description of what my tool does"
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="param1",
                type="string",
                description="Description of parameter",
                required=True
            )
        ]
    
    def execute(self, param1: str) -> str:
        # Your tool logic here
        return f"Result: {param1}"
```

The tool will be automatically discovered and registered when the chatbot starts.

## 🏗️ Architecture

```
week1_chatbot/
├── chatbot/           # Main chatbot logic
│   ├── __init__.py
│   ├── bot.py         # ChatBot class
│   └── config.py      # Configuration management
├── tools/             # Tool system
│   ├── __init__.py
│   ├── base.py        # BaseTool abstract class
│   ├── registery.py   # Tool registry
│   └── available/     # Available tools directory
│       ├── calculator.py
│       ├── datetime_tool.py
│       ├── file_operations.py
│       ├── news_tool.py
│       ├── stock_tool.py
│       ├── weather_tool.py
│       └── web_search_tool.py
├── utils/             # Utilities
│   ├── __init__.py
│   ├── formatting.py  # Rich formatting functions
│   └── validators.py  # Validation utilities
├── main.py            # Entry point
├── .env.example       # Environment variables template
├── requirements.txt   # Dependencies
├── API_KEYS_SETUP.md  # API setup guide
└── README.md          # This file
```

## 📋 Requirements

* Python 3.8+
* OpenAI API key or OpenRouter API key
* Modern Python development tools (uv recommended)

## 🛠️ Development

### Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Run tests
make test

# Run all checks
make check
```

### Using uv (Modern Python Tooling)

```bash
# Install uv
pip install uv

# Sync dependencies
uv sync --dev

# Run commands
uv run python main.py
uv run pytest
uv run black .
```

### Using Make

```bash
# Show all available commands
make help

# Setup development environment
make setup

# Run the chatbot
make run

# Clean build artifacts
make clean
```

## 🔑 API Keys Setup

To enable real-time data access, you'll need API keys from these services:

### 🌤️ Weather Data (OpenWeatherMap)
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key
4. Replace `YOUR_OPENWEATHER_API_KEY` in `tools/available/weather_tool.py`

### 📰 News Data (NewsAPI)
1. Go to [NewsAPI](https://newsapi.org/)
2. Sign up for a free account (1000 requests/day)
3. Get your API key
4. Replace `YOUR_NEWS_API_KEY` in `tools/available/news_tool.py`

### 📈 Stock Data (Alpha Vantage)
1. Go to [Alpha Vantage](https://www.alphavantage.co/)
2. Sign up for a free account (500 requests/day)
3. Get your API key
4. Replace `YOUR_ALPHA_VANTAGE_API_KEY` in `tools/available/stock_tool.py`

## 🚀 Advanced Features

### Tool Registry
- **Auto-discovery**: Automatically finds and registers tools
- **Validation**: Comprehensive parameter validation
- **Error Handling**: Robust error handling and reporting
- **Statistics**: Detailed tool registry statistics

### Real-time Data
- **Weather**: Current conditions for any city
- **News**: Latest headlines by category
- **Stocks**: Real-time market data
- **Web Search**: Current web information

### Enhanced UI
- **Rich Formatting**: Beautiful tables and panels
- **Markdown Support**: Rich text formatting
- **Color Coding**: Intuitive color scheme
- **Progress Indicators**: Visual feedback

## 🔒 Security

Never commit your API keys to version control. Use environment variables:

```python
import os
api_key = os.getenv("OPENWEATHER_API_KEY")
```

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Built with ❤️ using OpenAI, Rich, and Python**
