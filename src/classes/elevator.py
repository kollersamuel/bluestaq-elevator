"""
elevator.py
Samuel Koller
Created: 17 October 2024
Updated: 17 October 2024

Class for the Elevator object, which tracks the state an contents of the elevator.
"""


# TODO: Remove pylint disable, added temporarily as this class is not being implemented on this branch.
# pylint: disable-next=R0903
class Elevator:
    """
    The Elevator object: transports persons to their requested destination.

    Attributes:
        status (str): The status of the elevator. Can be a string of select choices: ["Idle"]

    Examples:
        elevator = Elevator()
    """

    def __init__(self) -> None:
        """Initializes an Elevator class, sets initial state to "Idle"."""
        self.status: str = "Idle"
