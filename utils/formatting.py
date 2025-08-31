from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()


def format_message(role: str, text: str) -> None:
    color = "green" if role == "assistant" else "blue"
    console.print(
        Panel(
            Markdown(text),
            title=f"[bold {color}]{role.capitalize()}[/bold {color}]",
            border_style=color,
            padding=(0, 1),
        )
    )


def format_error(text: str) -> None:
    console.print(Panel(text, title="[bold red]Error[/bold red]", border_style="red"))


def format_tool_call(name: str, args: dict) -> None:
    table = Table(title=f"🔧 Calling tool: {name}")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")
    for k, v in (args or {}).items():
        table.add_row(k, str(v))
    console.print(table)


def format_tool_result(name: str, result) -> None:
    console.print(
        Panel(
            str(result),
            title=f"[bold magenta]Tool result: {name}[/bold magenta]",
            border_style="magenta",
        )
    )


def format_welcome() -> None:
    console.print(
        Panel(
            "[bold]CLI Chatbot[/bold]\nType 'help' for commands, 'tools' to list tools, 'exit' to quit.",
            title="[bold green]Welcome[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
    )


def format_help(tools: list[str]) -> None:
    text = "Commands: help | tools | quit/exit\n\n" "Tools: " + (
        ", ".join(tools) if tools else "none"
    )
    console.print(Panel(text, title="[bold cyan]Help[/bold cyan]", border_style="cyan"))
