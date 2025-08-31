"""Tests for the tool system."""

import pytest
from unittest.mock import Mock, patch
from tools.base import BaseTool, ToolParameter
from tools.registry import ToolRegistry
from tools.available.calculator import CalculatorTool
from tools.available.file_operations import FileOperationsTool


class TestBaseTool:
    """Test cases for BaseTool class."""

    def test_tool_parameter_creation(self):
        """Test ToolParameter creation."""
        param = ToolParameter(
            name="test_param",
            type="string",
            description="Test parameter",
            required=True
        )
        
        assert param.name == "test_param"
        assert param.type == "string"
        assert param.description == "Test parameter"
        assert param.required is True

    def test_base_tool_abstract_methods(self):
        """Test that BaseTool is abstract and requires implementation."""
        with pytest.raises(TypeError):
            BaseTool()


class TestToolRegistry:
    """Test cases for ToolRegistry class."""

    @pytest.fixture
    def registry(self):
        """Create a ToolRegistry instance."""
        return ToolRegistry()

    @pytest.fixture
    def mock_tool(self):
        """Create a mock tool."""
        tool = Mock(spec=BaseTool)
        tool.name = "test_tool"
        tool.description = "Test tool description"
        tool.parameters = []
        return tool

    def test_registry_initialization(self, registry):
        """Test ToolRegistry initialization."""
        assert registry._tools == {}
        assert registry._tool_errors == []

    def test_register_tool(self, registry, mock_tool):
        """Test tool registration."""
        with patch('tools.registry.console') as mock_console:
            registry.register(mock_tool)
            
            assert mock_tool.name in registry._tools
            assert registry._tools[mock_tool.name] == mock_tool
            mock_console.print.assert_called()

    def test_register_invalid_tool(self, registry):
        """Test registering invalid tool."""
        invalid_tool = "not a tool"
        
        with patch('tools.registry.console') as mock_console:
            registry.register(invalid_tool)
            
            assert len(registry._tool_errors) == 1
            mock_console.print.assert_called()

    def test_get_tool(self, registry, mock_tool):
        """Test getting a tool by name."""
        registry._tools[mock_tool.name] = mock_tool
        
        retrieved_tool = registry.get_tool(mock_tool.name)
        assert retrieved_tool == mock_tool

    def test_get_nonexistent_tool(self, registry):
        """Test getting a tool that doesn't exist."""
        with pytest.raises(ValueError, match="Tool 'nonexistent' not found"):
            registry.get_tool("nonexistent")

    def test_list_tools(self, registry, mock_tool):
        """Test listing all tools."""
        registry._tools[mock_tool.name] = mock_tool
        
        tools = registry.list_tools()
        assert tools == [mock_tool.name]


class TestCalculatorTool:
    """Test cases for CalculatorTool."""

    @pytest.fixture
    def calculator(self):
        """Create a CalculatorTool instance."""
        return CalculatorTool()

    def test_calculator_properties(self, calculator):
        """Test CalculatorTool properties."""
        assert calculator.name == "calculator"
        assert "mathematical" in calculator.description.lower()
        assert len(calculator.parameters) > 0

    def test_calculator_execute(self, calculator):
        """Test calculator execution."""
        result = calculator.execute(expression="2 + 2")
        assert "4" in result

    def test_calculator_invalid_expression(self, calculator):
        """Test calculator with invalid expression."""
        result = calculator.execute(expression="invalid expression")
        assert "error" in result.lower() or "invalid" in result.lower()


class TestFileOperationsTool:
    """Test cases for FileOperationsTool."""

    @pytest.fixture
    def file_tool(self):
        """Create a FileOperationsTool instance."""
        return FileOperationsTool()

    def test_file_tool_properties(self, file_tool):
        """Test FileOperationsTool properties."""
        assert file_tool.name == "file_operations"
        assert "file operations" in file_tool.description.lower()
        assert len(file_tool.parameters) > 0

    @patch('builtins.open', create=True)
    def test_file_tool_read(self, mock_open, file_tool):
        """Test file reading operation."""
        mock_open.return_value.__enter__.return_value.read.return_value = "test content"
        
        result = file_tool.execute(action="read", filepath="test.txt")
        
        assert "test content" in result
        mock_open.assert_called_once_with("test.txt", "r", encoding="utf-8")

    def test_file_tool_list_directory(self, file_tool):
        """Test directory listing operation."""
        with patch('os.listdir') as mock_listdir:
            mock_listdir.return_value = ["file1.txt", "file2.py"]
            
            result = file_tool.execute(action="list", directory=".")
            
            assert "file1.txt" in result
            assert "file2.py" in result
            mock_listdir.assert_called_once_with(".")
