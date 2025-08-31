"""
File operations tool for the chatbot.
"""

import json
import os
from typing import List

from tools.base import BaseTool, ToolParameter


class FileOperationsTool(BaseTool):
    @property
    def name(self) -> str:
        return "file_operations"

    @property
    def description(self) -> str:
        return "Perform file operations like reading, writing, listing files, and checking file information."

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="action",
                type="string",
                description="The action to perform: 'read', 'write', 'list', 'info', 'exists'",
                required=True,
                enum=["read", "write", "list", "info", "exists"],
            ),
            ToolParameter(
                name="filepath",
                type="string",
                description="Path to the file or directory",
                required=False,
            ),
            ToolParameter(
                name="content",
                type="string",
                description="Content to write to the file (for write action)",
                required=False,
            ),
            ToolParameter(
                name="directory",
                type="string",
                description="Directory to list files from (for list action)",
                required=False,
            ),
        ]

    def execute(
        self,
        action: str,
        filepath: str = None,
        content: str = None,
        directory: str = None,
    ) -> str:
        """Execute the file operations tool."""
        try:
            if action == "read":
                if not filepath:
                    return "Error: filepath parameter required for read action"

                if not os.path.exists(filepath):
                    return f"Error: File '{filepath}' does not exist"

                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                return f"File content of '{filepath}':\n{content}"

            elif action == "write":
                if not filepath or content is None:
                    return "Error: filepath and content parameters required for write action"

                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                return f"Successfully wrote content to '{filepath}'"

            elif action == "list":
                dir_path = directory or "."

                if not os.path.exists(dir_path):
                    return f"Error: Directory '{dir_path}' does not exist"

                if not os.path.isdir(dir_path):
                    return f"Error: '{dir_path}' is not a directory"

                files = []
                for item in os.listdir(dir_path):
                    item_path = os.path.join(dir_path, item)
                    if os.path.isfile(item_path):
                        files.append(f"📄 {item}")
                    elif os.path.isdir(item_path):
                        files.append(f"📁 {item}/")

                if not files:
                    return f"Directory '{dir_path}' is empty"

                return f"Contents of '{dir_path}':\n" + "\n".join(files)

            elif action == "info":
                if not filepath:
                    return "Error: filepath parameter required for info action"

                if not os.path.exists(filepath):
                    return f"Error: File '{filepath}' does not exist"

                stat = os.stat(filepath)
                size = stat.st_size
                modified = stat.st_mtime

                # Format file size
                if size < 1024:
                    size_str = f"{size} bytes"
                elif size < 1024 * 1024:
                    size_str = f"{size / 1024:.1f} KB"
                else:
                    size_str = f"{size / (1024 * 1024):.1f} MB"

                from datetime import datetime

                modified_str = datetime.fromtimestamp(modified).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                info = f"""
File Information for '{filepath}':
- Size: {size_str}
- Modified: {modified_str}
- Type: {'Directory' if os.path.isdir(filepath) else 'File'}
                """

                return info.strip()

            elif action == "exists":
                if not filepath:
                    return "Error: filepath parameter required for exists action"

                exists = os.path.exists(filepath)
                return f"File '{filepath}' {'exists' if exists else 'does not exist'}"

            else:
                return f"Error: unknown action '{action}'"

        except Exception as e:
            return f"Error in file operation: {str(e)}"
