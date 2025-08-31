"""
Tests for the config module.
"""

import os
import pytest
from unittest.mock import patch
from chatbot.config import Config


class TestConfig:
    """Test cases for Config class."""

    def test_config_from_env_openrouter(self):
        """Test Config.from_env with OpenRouter API key."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test_key"}):
            config = Config.from_env()
            assert config.api_key == "test_key"
            assert config.base_url == "https://openrouter.ai/api/v1"
            assert "openai/gpt-4o-mini" in config.model

    def test_config_from_env_openai(self):
        """Test Config.from_env with OpenAI API key."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
            config = Config.from_env()
            assert config.api_key == "test_key"
            assert config.base_url is None
            assert config.model == "gpt-4o-mini"

    def test_config_from_env_no_key(self):
        """Test Config.from_env with no API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Set OPENROUTER_API_KEY or OPENAI_API_KEY"):
                Config.from_env()

    def test_config_custom_values(self):
        """Test Config with custom values."""
        config = Config(
            api_key="test_key",
            base_url="https://test.com",
            model="test-model",
            max_tokens=500,
            temperature=0.5
        )
        assert config.api_key == "test_key"
        assert config.base_url == "https://test.com"
        assert config.model == "test-model"
        assert config.max_tokens == 500
        assert config.temperature == 0.5

    def test_config_default_values(self):
        """Test Config default values."""
        config = Config(api_key="test_key", base_url=None)
        assert config.model == "gpt-4o-mini"
        assert config.max_tokens == 1000
        assert config.temperature == 0.7
        assert "You are a helpful AI assistant" in config.system_prompt
