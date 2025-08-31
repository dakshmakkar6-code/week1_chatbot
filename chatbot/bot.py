"""
Advanced ChatBot class with OpenAI integration, tool support, and rich formatting.
"""

import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.table import Table

from tools.registry import ToolRegistry
from utils.formatting import (
    format_error,
    format_help,
    format_message,
    format_tool_call,
    format_tool_result,
    format_welcome,
)

from .config import Config

console = Console()


class ChatBot:
    """Advanced chatbot class with OpenAI integration and tool support."""

    def __init__(self, config: Config):
        self.config = config

        # Set up default headers for OpenRouter
        default_headers = {}
        if config.base_url and "openrouter.ai" in config.base_url:
            default_headers = {
                "HTTP-Referer": os.getenv("HTTP_REFERER", "http://localhost"),
                "X-Title": os.getenv("X_TITLE", "Week1 Advanced Chatbot"),
            }

        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            default_headers=default_headers,
        )
        self.tool_registry = ToolRegistry()
        self.conversation_history: List[Dict[str, Any]] = []
        self.message_count = 0

        # Initialize with system message
        self.conversation_history.append(
            {"role": "system", "content": config.system_prompt}
        )

    def register_tool(self, tool) -> None:
        """Register a tool with the chatbot."""
        self.tool_registry.register(tool)

    def auto_discover_tools(self) -> None:
        """Auto-discover tools from the tools/available directory."""
        try:
            self.tool_registry.auto_discover_tools()
        except Exception as e:
            console.print(f"[yellow]Tool discovery warning: {e}[/yellow]")

    def _handle_tool_calls(self, tool_calls) -> List[Dict[str, Any]]:
        """Handle tool calls from the assistant."""
        tool_results = []

        for tool_call in tool_calls:
            try:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Display the tool call
                format_tool_call(function_name, function_args)

                # Execute the tool
                result = self.tool_registry.execute_tool(function_name, **function_args)

                # Display the result
                format_tool_result(function_name, result)

                # Add tool call and result to conversation
                self.conversation_history.append(
                    {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": tool_call.id,
                                "type": "function",
                                "function": {
                                    "name": function_name,
                                    "arguments": tool_call.function.arguments,
                                },
                            }
                        ],
                    }
                )

                tool_results.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(result),
                    }
                )

            except Exception as e:
                console.print(f"[red]Error executing tool: {e}[/red]")
                tool_results.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": f"Error: {e}",
                    }
                )

        return tool_results

    def chat(self, message: str) -> str:
        """Send a message to the chatbot and get a response."""
        self.message_count += 1

        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})

        try:
            # Get available tools
            tools = self.tool_registry.get_openai_tools()

            # Make API call
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=self.conversation_history,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None,
            )

            assistant_message = response.choices[0].message

            # Handle tool calls if present
            if assistant_message.tool_calls:
                tool_results = self._handle_tool_calls(assistant_message.tool_calls)

                # Add tool results to conversation
                self.conversation_history.extend(tool_results)

                # Get final response after tool calls
                response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=self.conversation_history,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                )
                assistant_message = response.choices[0].message

            # Add assistant response to history
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_message.content}
            )

            return assistant_message.content or "I don't have a response for that."

        except Exception as e:
            error_msg = f"Error communicating with AI: {str(e)}"
            console.print(f"[red]Error: {error_msg}[/red]")
            return f"Sorry, I encountered an error: {str(e)}"

    def handle_command(self, user_input: str) -> bool:
        """Handle special commands. Returns True if command was handled."""
        user_input = user_input.strip().lower()

        if user_input in ["quit", "exit"]:
            console.print("[yellow]Goodbye! 👋[/yellow]")
            return True
        elif user_input == "help":
            self.show_help()
            return False
        elif user_input == "tools":
            self.show_tools()
            return False
        elif user_input == "tool-details":
            self.show_tool_details()
            return False
        elif user_input == "clear":
            self.clear_history()
            return False
        elif user_input == "stats":
            self.show_stats()
            return False
        elif user_input == "save":
            self.save_conversation()
            return False
        elif user_input == "config":
            self.show_config()
            return False
        elif user_input == "reset":
            self.reset_chatbot()
            return False

        return False

    def show_help(self):
        """Display help information."""
        help_text = """
**Available Commands:**
- `help` - Show this help message
- `tools` - List all available tools
- `tool-details` - Show detailed tool information
- `clear` - Clear conversation history
- `stats` - Show conversation statistics
- `save` - Save conversation to file
- `config` - Show current configuration
- `reset` - Reset chatbot to initial state
- `exit` - Quit the chatbot

**Available Tools:** """ + (
            ", ".join(self.tool_registry.list_tools())
            if self.tool_registry.list_tools()
            else "none"
        )

        console.print(
            Panel(
                Markdown(help_text),
                title="[bold cyan]Help[/bold cyan]",
                border_style="cyan",
            )
        )

    def show_tools(self):
        """Display available tools."""
        self.tool_registry.show_tool_details()

    def show_tool_details(self):
        """Show detailed information about all tools."""
        tools = self.tool_registry.list_tools()
        if not tools:
            console.print("[yellow]No tools available[/yellow]")
            return

        for tool_name in tools:
            self.tool_registry.show_tool_details(tool_name)
            console.print()  # Add spacing between tools

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = [
            {"role": "system", "content": self.config.system_prompt}
        ]
        self.message_count = 0
        console.print("[green]Conversation history cleared![/green]")

    def show_stats(self):
        """Show conversation statistics."""
        registry_stats = self.tool_registry.get_registry_stats()

        stats_text = f"""
**Conversation Statistics:**
- Messages exchanged: {self.message_count}
- Model: {self.config.model}
- API: {'OpenRouter' if 'openrouter.ai' in self.config.base_url else 'OpenAI'}
- Tools available: {registry_stats['total_tools']}
- Tool discovery errors: {registry_stats['errors']}

**Tool Registry:**
- Total tools: {registry_stats['total_tools']}
- Tool names: {', '.join(registry_stats['tool_names'])}
        """
        console.print(
            Panel(
                stats_text,
                title="[bold magenta]Statistics[/bold magenta]",
                border_style="magenta",
            )
        )

    def save_conversation(self):
        """Save conversation to a file."""
        try:
            import time

            timestamp = int(time.time())
            filename = f"conversation_{self.message_count}_{timestamp}.json"

            # Create a clean version of the conversation for saving
            save_data = {
                "metadata": {
                    "timestamp": timestamp,
                    "message_count": self.message_count,
                    "model": self.config.model,
                    "api": (
                        "OpenRouter"
                        if "openrouter.ai" in self.config.base_url
                        else "OpenAI"
                    ),
                },
                "conversation": self.conversation_history,
            }

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            console.print(f"[green]Conversation saved to {filename}[/green]")

        except Exception as e:
            console.print(f"[red]Error saving conversation: {e}[/red]")

    def show_config(self):
        """Show current configuration."""
        config_text = f"""
**Current Configuration:**
- Model: {self.config.model}
- API Provider: {'OpenRouter' if 'openrouter.ai' in self.config.base_url else 'OpenAI'}
- Base URL: {self.config.base_url or 'Default OpenAI'}
- Max Tokens: {self.config.max_tokens}
- Temperature: {self.config.temperature}
- System Prompt: {len(self.config.system_prompt)} characters
        """
        console.print(
            Panel(
                config_text,
                title="[bold blue]Configuration[/bold blue]",
                border_style="blue",
            )
        )

    def reset_chatbot(self):
        """Reset the chatbot to initial state."""
        self.clear_history()
        self.tool_registry = ToolRegistry()
        self.auto_discover_tools()
        console.print("[green]Chatbot reset to initial state![/green]")

    def run(self) -> None:
        """Run the interactive chatbot."""
        format_welcome()

        # Auto-discover tools
        console.print("[cyan]🔍 Discovering tools...[/cyan]")
        self.auto_discover_tools()

        try:
            while True:
                user_input = Prompt.ask("\n[bold blue]You[/bold blue]")

                if not user_input:
                    continue

                # Handle special commands
                if self.handle_command(user_input):
                    break

                # Display user message
                format_message("user", user_input)

                # Get and display bot response
                response = self.chat(user_input)
                if response:
                    format_message("assistant", response)

        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye! 👋[/yellow]")
        except Exception as e:
            console.print(f"[red]Unexpected error: {str(e)}[/red]")
