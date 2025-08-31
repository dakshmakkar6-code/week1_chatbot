from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pydantic import BaseModel


class ToolParameter(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True
    enum: List[str] | None = None


class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    @property
    @abstractmethod
    def description(self) -> str: ...
    @property
    @abstractmethod
    def parameters(self) -> List[ToolParameter]: ...
    @abstractmethod
    def execute(self, **kwargs) -> Any: ...

    def to_openai_tool(self) -> Dict[str, Any]:
        properties, required = {}, []
        for p in self.parameters:
            d = {"type": p.type, "description": p.description}
            if p.enum:
                d["enum"] = p.enum
            properties[p.name] = d
            if p.required:
                required.append(p.name)
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }
