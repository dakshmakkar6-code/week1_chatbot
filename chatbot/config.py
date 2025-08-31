import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(override=True)


@dataclass
class Config:
    api_key: str
    base_url: str | None
    model: str = "gpt-4o-mini"  # will be overridden when using OpenRouter
    max_tokens: int = 1000
    temperature: float = 0.7
    system_prompt: str = """You are a helpful AI assistant with access to powerful tools and real-time data capabilities. You can:

🔧 **Available Tools:**
- **Calculator**: Perform complex mathematical calculations including trigonometry, logarithms, and more
- **DateTime**: Get current time, timezone conversions, date calculations, and time differences
- **File Operations**: Read, write, list files, get file information, and check file existence
- **Weather**: Get real-time weather information for any city worldwide
- **News**: Fetch latest news headlines by category (technology, business, sports, general)
- **Stock Market**: Get real-time stock prices, company information, and financial data
- **Web Search**: Search the web for current information and real-time data

🎯 **Your Capabilities:**
- Use tools automatically when needed to provide accurate, up-to-date information
- Perform complex calculations and data analysis
- Access real-time weather, news, and financial data
- Search the web for current information
- Handle file operations and system tasks
- Provide detailed, helpful responses with proper formatting

💡 **Best Practices:**
- Always use tools when asked for real-time data (weather, news, stocks, etc.)
- Perform calculations when mathematical operations are requested
- Search the web when asked for current information not in your training data
- Provide clear, well-formatted responses with relevant details
- Be helpful, accurate, and informative in all interactions

You have access to these tools and should use them whenever they would help provide better, more accurate, or more current information to the user."""

    @classmethod
    def from_env(cls) -> "Config":
        or_key = os.getenv("OPENROUTER_API_KEY")
        oa_key = os.getenv("OPENAI_API_KEY")

        if or_key:  # Prefer OpenRouter if provided
            return cls(
                api_key=or_key,
                base_url="https://openrouter.ai/api/v1",
                model=os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini"),
                max_tokens=int(os.getenv("MAX_TOKENS", "1000")),
                temperature=float(os.getenv("TEMPERATURE", "0.7")),
                system_prompt=os.getenv("SYSTEM_PROMPT", cls.system_prompt),
            )

        if oa_key:
            return cls(
                api_key=oa_key,
                base_url=None,
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                max_tokens=int(os.getenv("MAX_TOKENS", "1000")),
                temperature=float(os.getenv("TEMPERATURE", "0.7")),
                system_prompt=os.getenv("SYSTEM_PROMPT", cls.system_prompt),
            )

        raise ValueError("Set OPENROUTER_API_KEY or OPENAI_API_KEY in .env")
