"""
person.py
Samuel Koller
Created: 19 October 2024
Updated: 21 October 2024

Class for the Person object, which tracks the location of the person and other attributes.
"""

import numpy as np

from ..utils import id_generator


# pylint: disable-next=too-few-public-methods
class Person:
    """
    Information regarding a person and their journey.
    """

    def __init__(self, origin, destination, weight=0, cargo=None) -> None:
        """
        Sets initial location to origin, and generates an identifier.

        Attributes:
            id (int): A unique identifier given to the person.
            location (int | str): The person's location.
            destination (int): The destination of the person.
            weight (float): The weight of the person.
            cargo (float): The weight of the person's cargo.
        """
        self.id: int = id_generator()
        self.location = origin
        self.destination = destination

        # ? If no weight provided, normally distribute weight, constrain to between 20 (persons less than 20 pounds
        # ? considered cargo) and 500 (arbitrary maximum)
        if 20 <= weight <= 500:
            self.weight = weight
        else:
            self.weight: float = max(20, min(np.random.normal(loc=150, scale=100), 500))
        # ? If no cargo provided, normally distribute cargo weight, constrain to between 0 and 100 (arbitrary maximum)
        if cargo is not None and 0 <= cargo <= 100:
            self.cargo = cargo
        else:
            self.cargo: float = max(0, min(np.random.normal(loc=25, scale=5), 100))
