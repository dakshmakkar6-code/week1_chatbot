import importlib
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .base import BaseTool

console = Console()


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._tool_errors: List[str] = []

    def register(self, tool: BaseTool) -> None:
        """Register a tool with validation."""
        try:
            if not isinstance(tool, BaseTool):
                raise ValueError(f"Tool must inherit from BaseTool")

            if not tool.name:
                raise ValueError(f"Tool must have a valid name")

            if tool.name in self._tools:
                console.print(
                    f"[yellow]⚠️[/yellow] Tool '{tool.name}' already registered, overwriting"
                )

            self._tools[tool.name] = tool
            console.print(f"[green]✓[/green] Registered tool: {tool.name}")

        except Exception as e:
            error_msg = f"Failed to register tool: {str(e)}"
            self._tool_errors.append(error_msg)
            console.print(f"[red]✗[/red] {error_msg}")

    def get_tool(self, name: str) -> BaseTool:
        """Get a tool by name with error handling."""
        if name not in self._tools:
            available_tools = ", ".join(self._tools.keys())
            raise ValueError(
                f"Tool '{name}' not found. Available tools: {available_tools}"
            )
        return self._tools[name]

    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self._tools.keys())

    def get_tool_info(self, name: str) -> Dict[str, Any]:
        """Get detailed information about a tool."""
        tool = self.get_tool(name)
        return {
            "name": tool.name,
            "description": tool.description,
            "parameters": [p.dict() for p in tool.parameters],
        }

    def get_openai_tools(self) -> List[Dict[str, Any]]:
        """Get tools in OpenAI function calling format."""
        tools = []
        for tool in self._tools.values():
            try:
                tools.append(tool.to_openai_tool())
            except Exception as e:
                console.print(
                    f"[red]Error converting tool {tool.name} to OpenAI format: {e}[/red]"
                )
        return tools

    def auto_discover_tools(self, tools_dir: str = "tools/available") -> None:
        """Auto-discover tools from the tools/available directory with enhanced error handling."""
        p = Path(tools_dir)
        if not p.exists():
            console.print(f"[yellow]⚠️[/yellow] Tools directory '{tools_dir}' not found")
            return

        tools_found = 0
        errors = []

        for f in p.glob("*.py"):
            if f.name.startswith("__"):
                continue

            # Skip empty files
            if f.stat().st_size == 0:
                console.print(f"[yellow]⚠️[/yellow] Skipping empty file: {f.name}")
                continue

            mod_name = f"tools.available.{f.stem}"
            try:
                mod = importlib.import_module(mod_name)
                for attr_name in dir(mod):
                    attr = getattr(mod, attr_name)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, BaseTool)
                        and attr is not BaseTool
                    ):
                        try:
                            self.register(attr())
                            tools_found += 1
                        except Exception as e:
                            error_msg = (
                                f"Failed to register {attr_name} from {f.name}: {e}"
                            )
                            errors.append(error_msg)
                            console.print(f"[red]✗[/red] {error_msg}")

            except Exception as e:
                error_msg = f"Error loading module {f.name}: {e}"
                errors.append(error_msg)
                console.print(f"[red]✗[/red] {error_msg}")

        # Summary
        if tools_found == 0:
            console.print(
                "[cyan]ℹ️[/cyan] No tools discovered. Add tools to tools/available/ directory."
            )
        else:
            console.print(f"[green]✓[/green] Discovered {tools_found} tool(s)")

        if errors:
            console.print(
                f"[yellow]⚠️[/yellow] {len(errors)} error(s) during tool discovery"
            )

    def execute_tool(self, name: str, **kwargs):
        """Execute a tool with comprehensive error handling."""
        try:
            tool = self.get_tool(name)

            # Validate required parameters
            required_params = [p.name for p in tool.parameters if p.required]
            missing_params = [param for param in required_params if param not in kwargs]

            if missing_params:
                raise ValueError(
                    f"Missing required parameters: {', '.join(missing_params)}"
                )

            # Execute the tool
            result = tool.execute(**kwargs)
            return result

        except Exception as e:
            error_msg = f"Error executing tool '{name}': {str(e)}"
            console.print(f"[red]✗[/red] {error_msg}")
            return f"Error: {str(e)}"

    def show_tool_details(self, name: str = None) -> None:
        """Display detailed information about tools."""
        if name:
            # Show specific tool details
            try:
                tool_info = self.get_tool_info(name)
                tool = self.get_tool(name)

                table = Table(title=f"Tool Details: {name}")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="green")

                table.add_row("Name", tool_info["name"])
                table.add_row("Description", tool_info["description"])

                params_text = ""
                for param in tool_info["parameters"]:
                    required = "✓" if param["required"] else "✗"
                    params_text += (
                        f"• {param['name']} ({param['type']}) - {required} required\n"
                    )
                    if param.get("enum"):
                        params_text += f"  Options: {', '.join(param['enum'])}\n"

                table.add_row("Parameters", params_text.strip())

                console.print(table)

            except Exception as e:
                console.print(f"[red]Error showing tool details: {e}[/red]")
        else:
            # Show all tools summary
            if not self._tools:
                console.print("[yellow]No tools registered[/yellow]")
                return

            table = Table(title="Available Tools")
            table.add_column("Tool Name", style="cyan")
            table.add_column("Description", style="green")
            table.add_column("Parameters", style="yellow")

            for tool in self._tools.values():
                param_count = len(tool.parameters)
                required_count = len([p for p in tool.parameters if p.required])
                param_info = f"{param_count} total, {required_count} required"

                table.add_row(tool.name, tool.description, param_info)

            console.print(table)

    def get_registry_stats(self) -> Dict[str, Any]:
        """Get statistics about the tool registry."""
        return {
            "total_tools": len(self._tools),
            "tool_names": list(self._tools.keys()),
            "errors": len(self._tool_errors),
            "error_messages": self._tool_errors.copy(),
        }
