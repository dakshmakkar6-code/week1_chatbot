"""Tests for the ChatBot class."""

import pytest
from unittest.mock import Mock, patch
from chatbot.bot import ChatBot
from chatbot.config import Config


class TestChatBot:
    """Test cases for ChatBot class."""

    @pytest.fixture
    def mock_config(self):
        """Create a mock config for testing."""
        config = Mock(spec=Config)
        config.api_key = "test_api_key"
        config.base_url = "https://api.openai.com/v1"
        config.system_prompt = "You are a helpful assistant."
        return config

    @pytest.fixture
    def chatbot(self, mock_config):
        """Create a ChatBot instance for testing."""
        with patch('openai.OpenAI'):
            return ChatBot(mock_config)

    def test_chatbot_initialization(self, mock_config):
        """Test ChatBot initialization."""
        with patch('openai.OpenAI') as mock_openai:
            chatbot = ChatBot(mock_config)
            
            assert chatbot.config == mock_config
            assert len(chatbot.conversation_history) == 1
            assert chatbot.conversation_history[0]["role"] == "system"
            assert chatbot.conversation_history[0]["content"] == mock_config.system_prompt
            assert chatbot.message_count == 0

    def test_register_tool(self, chatbot):
        """Test tool registration."""
        mock_tool = Mock()
        chatbot.register_tool(mock_tool)
        
        # Verify tool was registered with the registry
        chatbot.tool_registry.register.assert_called_once_with(mock_tool)

    def test_auto_discover_tools(self, chatbot):
        """Test auto-discovery of tools."""
        with patch.object(chatbot.tool_registry, 'auto_discover_tools') as mock_discover:
            chatbot.auto_discover_tools()
            mock_discover.assert_called_once()

    @patch('chatbot.bot.console')
    def test_show_help(self, mock_console, chatbot):
        """Test help command."""
        chatbot.show_help()
        mock_console.print.assert_called()

    @patch('chatbot.bot.console')
    def test_show_tools(self, chatbot):
        """Test tools listing."""
        with patch.object(chatbot.tool_registry, 'show_tool_details') as mock_show:
            chatbot.show_tools()
            mock_show.assert_called_once()

    def test_clear_history(self, chatbot):
        """Test conversation history clearing."""
        # Add some messages to history
        chatbot.conversation_history.append({"role": "user", "content": "test"})
        chatbot.message_count = 5
        
        chatbot.clear_history()
        
        assert len(chatbot.conversation_history) == 1  # Only system message remains
        assert chatbot.message_count == 0

    def test_show_stats(self, chatbot):
        """Test statistics display."""
        chatbot.message_count = 10
        with patch('chatbot.bot.console') as mock_console:
            chatbot.show_stats()
            mock_console.print.assert_called()

    @patch('json.dump')
    @patch('builtins.open', create=True)
    def test_save_conversation(self, mock_open, mock_dump, chatbot):
        """Test conversation saving."""
        chatbot.conversation_history = [
            {"role": "system", "content": "test"},
            {"role": "user", "content": "hello"}
        ]
        
        chatbot.save_conversation()
        
        mock_open.assert_called_once()
        mock_dump.assert_called_once()
