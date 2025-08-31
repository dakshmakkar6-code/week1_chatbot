"""
DateTime tool for the chatbot.
"""

from datetime import datetime, timedelta
from typing import List

import pytz

from tools.base import BaseTool, ToolParameter


class DateTimeTool(BaseTool):
    @property
    def name(self) -> str:
        return "datetime"

    @property
    def description(self) -> str:
        return "Get current date and time, timezone information, and perform date calculations."

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="action",
                type="string",
                description="The action to perform: 'current' (current time), 'timezone' (list timezones), 'convert' (convert timezone), 'add' (add time), 'diff' (time difference)",
                required=True,
                enum=["current", "timezone", "convert", "add", "diff"],
            ),
            ToolParameter(
                name="timezone",
                type="string",
                description="Timezone name (e.g., 'UTC', 'America/New_York', 'Europe/London')",
                required=False,
            ),
            ToolParameter(
                name="amount",
                type="string",
                description="Amount to add/subtract (e.g., '1 day', '2 hours', '30 minutes')",
                required=False,
            ),
            ToolParameter(
                name="date1",
                type="string",
                description="First date for comparison (format: YYYY-MM-DD HH:MM:SS)",
                required=False,
            ),
            ToolParameter(
                name="date2",
                type="string",
                description="Second date for comparison (format: YYYY-MM-DD HH:MM:SS)",
                required=False,
            ),
        ]

    def execute(
        self,
        action: str,
        timezone: str = None,
        amount: str = None,
        date1: str = None,
        date2: str = None,
    ) -> str:
        """Execute the datetime tool."""
        try:
            if action == "current":
                if timezone:
                    tz = pytz.timezone(timezone)
                    current_time = datetime.now(tz)
                    return f"Current time in {timezone}: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
                else:
                    utc_time = datetime.now(pytz.UTC)
                    local_time = datetime.now()
                    return f"Current time:\nUTC: {utc_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\nLocal: {local_time.strftime('%Y-%m-%d %H:%M:%S')}"

            elif action == "timezone":
                common_timezones = [
                    "UTC",
                    "America/New_York",
                    "America/Los_Angeles",
                    "Europe/London",
                    "Europe/Paris",
                    "Asia/Tokyo",
                    "Australia/Sydney",
                    "Asia/Dubai",
                    "Asia/Shanghai",
                ]
                return f"Common timezones: {', '.join(common_timezones)}"

            elif action == "convert":
                if not timezone:
                    return "Error: timezone parameter required for convert action"

                tz = pytz.timezone(timezone)
                current_time = datetime.now(tz)
                return f"Current time in {timezone}: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"

            elif action == "add":
                if not amount:
                    return "Error: amount parameter required for add action"

                # Parse amount (e.g., "1 day", "2 hours", "30 minutes")
                parts = amount.split()
                if len(parts) != 2:
                    return "Error: amount should be in format 'number unit' (e.g., '1 day')"

                number = int(parts[0])
                unit = parts[1].lower()

                current_time = datetime.now()

                if unit in ["day", "days"]:
                    new_time = current_time + timedelta(days=number)
                elif unit in ["hour", "hours"]:
                    new_time = current_time + timedelta(hours=number)
                elif unit in ["minute", "minutes"]:
                    new_time = current_time + timedelta(minutes=number)
                elif unit in ["second", "seconds"]:
                    new_time = current_time + timedelta(seconds=number)
                else:
                    return f"Error: unsupported time unit '{unit}'"

                return f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}\nAfter adding {amount}: {new_time.strftime('%Y-%m-%d %H:%M:%S')}"

            elif action == "diff":
                if not date1 or not date2:
                    return "Error: date1 and date2 parameters required for diff action"

                try:
                    dt1 = datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
                    dt2 = datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")
                    diff = abs(dt2 - dt1)

                    days = diff.days
                    hours, remainder = divmod(diff.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    return f"Time difference between {date1} and {date2}:\n{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

                except ValueError:
                    return "Error: dates should be in format YYYY-MM-DD HH:MM:SS"

            else:
                return f"Error: unknown action '{action}'"

        except Exception as e:
            return f"Error in datetime operation: {str(e)}"
