#!/usr/bin/env python3
"""
Main entry point for the CLI Chatbot.
A powerful chatbot with OpenAI/OpenRouter integration and modular tool support.
"""

import sys
import traceback

from chatbot import ChatBot, Config
from utils.formatting import format_error


def setup_environment():
    """Set up environment variables and validate configuration."""
    try:
        config = Config.from_env()
        return config
    except ValueError as e:
        format_error(f"Configuration Error: {e}")
        print("\nPlease set up your API key in a .env file:")
        print("For OpenRouter: OPENROUTER_API_KEY=your_key_here")
        print("For OpenAI: OPENAI_API_KEY=your_key_here")
        return None
    except Exception as e:
        format_error(f"Unexpected configuration error: {e}")
        return None


def create_chatbot(config):
    """Create and initialize the chatbot instance."""
    try:
        bot = ChatBot(config)
        return bot
    except Exception as e:
        format_error(f"Failed to initialize chatbot: {e}")
        return None


def run_chatbot(bot):
    """Run the main chatbot loop."""
    try:
        print(f"\n🤖 ChatBot initialized successfully!")
        print(f"📡 Using model: {bot.config.model}")
        print(
            f"🌐 API: {'OpenRouter' if 'openrouter.ai' in bot.config.base_url else 'OpenAI'}"
        )
        print("=" * 60)

        # Use the bot's built-in run method
        bot.run()

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using the chatbot.")
    except Exception as e:
        format_error(f"Chatbot runtime error: {e}")
        if __debug__:
            traceback.print_exc()


def main():
    """Main application entry point."""
    print("🚀 Starting CLI Chatbot...")

    # Set up configuration
    config = setup_environment()
    if not config:
        sys.exit(1)

    # Create chatbot instance
    bot = create_chatbot(config)
    if not bot:
        sys.exit(1)

    # Run the chatbot
    run_chatbot(bot)


if __name__ == "__main__":
    main()
