import json

import numpy as np

from src.classes.button import Button

from ..utils import id_generator


class Person:
    def __init__(self, **kwargs) -> None:
        self.id: int = id_generator()
        self.in_elevator = False
        self.origin = kwargs.get("origin")
        self.destination = kwargs.get("destination")

        # ? If no weight provided, normally distribute weight, constrain to between 20 (persons less than 20 pounds
        # ? considered cargo) and 500 (arbitrary maximum)
        if kwargs.get("weight"):
            self.weight = kwargs.get("weight")
        else:
            self.weight: float = max(20, min(np.random.normal(loc=150, scale=50), 500))
        # ? If no cargo provided, normally distribute cargo weight, constrain to between 0 and 100 (arbitrary maximum)
        if kwargs.get("cargo"):
            self.cargo = kwargs.get("cargo")
        else:
            self.cargo: float = max(0, min(np.random.normal(loc=25, scale=5), 100))
        if self.origin != self.destination:
            self.create_person()
            # self.create_initial_request()

    def create_person(self):
        with open("./persons.json", "r", encoding="utf-8") as persons_json:
            persons = json.load(persons_json)
        persons.append(
            {
                "id": self.id,
                "in_elevator": self.in_elevator,
                "weight": self.weight,
                "cargo": self.cargo,
                "origin": self.origin,
                "destination": self.destination,
            }
        )
        with open("./persons.json", "w", encoding="utf-8") as persons_json:
            json.dump(persons, persons_json, indent=2)

    def create_initial_request(self):
        Button(
            **{
                "source": self.origin,
                "button": "up" if self.destination > self.origin else "down",
            }
        )
