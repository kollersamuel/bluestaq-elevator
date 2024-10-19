"""
person.py
Samuel Koller
Created: 19 October 2024
Updated: 19 October 2024

Class for the Person object, which tracks the location of the person and other attributes.
"""

import numpy as np

from ..utils import id_generator


# pylint: disable-next=too-few-public-methods
class Person:
    """
    The Person object: Information regarding a person and their journey.

    Attributes:
        id (int): A unique identifier given to the person.
        location (int | str): The person's location.
        destination (int): The destination of the person.
        weight (float): The weight of the person.
        cargo (float): The weight of the person's cargo.

    Examples:
        person = Person()
    """

    def __init__(self, **kwargs) -> None:
        """Initializes a Person class, sets initial location to origin, and generates an identifier."""
        self.id: int = id_generator()
        self.location = kwargs.get("origin")
        self.destination = kwargs.get("destination")

        # ? If no weight provided, normally distribute weight, constrain to between 20 (persons less than 20 pounds
        # ? considered cargo) and 500 (arbitrary maximum)
        if kwargs.get("weight"):
            self.weight = kwargs.get("weight")
        else:
            self.weight: float = max(20, min(np.random.normal(loc=150, scale=100), 500))
        # ? If no cargo provided, normally distribute cargo weight, constrain to between 0 and 100 (arbitrary maximum)
        if kwargs.get("cargo"):
            self.cargo = kwargs.get("cargo")
        else:
            self.cargo: float = max(0, min(np.random.normal(loc=25, scale=5), 100))
