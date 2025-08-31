"""
Calculator tool for the chatbot.
"""

import math
from typing import List

from tools.base import BaseTool, ToolParameter


class CalculatorTool(BaseTool):
    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Perform mathematical calculations including basic arithmetic, trigonometry, and more."

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="expression",
                type="string",
                description="The mathematical expression to evaluate (e.g., '2 + 3 * 4', 'sin(45)', 'sqrt(16)')",
                required=True,
            )
        ]

    def execute(self, expression: str) -> str:
        """Execute the calculator tool."""
        try:
            # Replace common math functions
            expression = expression.lower()
            expression = expression.replace("sin", "math.sin")
            expression = expression.replace("cos", "math.cos")
            expression = expression.replace("tan", "math.tan")
            expression = expression.replace("sqrt", "math.sqrt")
            expression = expression.replace("log", "math.log10")
            expression = expression.replace("ln", "math.log")
            expression = expression.replace("pi", "math.pi")
            expression = expression.replace("e", "math.e")

            # Evaluate the expression
            result = eval(expression, {"__builtins__": {}}, {"math": math})

            return f"Result: {result}"

        except Exception as e:
            return f"Error calculating '{expression}': {str(e)}"
