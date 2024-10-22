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
        message=(
            f"The selected floor is not in range, 1 <= floor <= {TOP_FLOOR}"
            f"{', excluding 13.'if TOP_FLOOR > 13 else '.'}"
        ),
    ):
        super().__init__(message)


class InvalidButton(AttributeError):
    """
    Custom exception for requesting a button with a string input that is not 'elevator', 'up', or 'down'. Other key must
    be an integer.
    """

    def __init__(
        self,
        message=(
            "A string source must be 'elevator', a string button must be 'up' or 'down. Other key must be an "
            "integer"
        ),
    ):
        super().__init__(message)
