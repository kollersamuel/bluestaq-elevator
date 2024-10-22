"""
custom_exceptions.py
Samuel Koller
Created: 22 October 2024
Updated: 22 October 2024

Custom Exceptions used throughout the application.
"""

from src.utils.constants import TOP_FLOOR


class InvalidFloor(AttributeError):
    """
    Custom exception for requesting an invalid floor.
    """

    def __init__(
        self,
        message=f"The selected floor is not in range, 1 <= floor <= {TOP_FLOOR}"
        f"{', excluding 13.'if TOP_FLOOR > 13 else '.'}",
    ):
        super().__init__(message)
