"""
app.py
Samuel Koller
Created: 15 October 2024
Updated: 20 October 2024

Main file for the Bluestaq Elevator Application. Houses the Flask server and relevant endpoints.

Functions:
    health_check(): A route to check if the service is running.
    step(int): A route to induce a given number of steps for the state machine.
    press_button(): A route to manually press a button.
    step(): A route to add persons to the system.
"""

__version__ = "0.4.0"


import logging

from dotenv import load_dotenv
from flask import Flask, request

from src.classes.elevator import Elevator
from src.classes.person import Person

load_dotenv()
app = Flask(__name__)
elevator = Elevator()


logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger("Elevator")


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check route to ping for application status.

    Responses:
        - **200 OK**: "Elevator is Online"
    """
    return "Elevator is Online", 200


@app.route("/step/<int:steps>", methods=["GET"])
def step(steps: int):
    """
    Route to submit a request to the elevator system.

    Parameters:
        steps (int): The number of steps to take.

    Responses:
        - **200 OK**: "Moved 0 step(s)."
    """
    response = {}
    person_locations = ""

    for _ in range(steps):
        elevator.update()
        logger.debug(
            f"After this step, the elevator is at {elevator.current_floor} and has a status of "
            f"{'Open' if elevator.is_open else 'Moving'} and a queue of stops for these floors:\nPriority: "
            f"{elevator.priority_queue}\nUp: {elevator.up_queue}\nDown: {elevator.down_queue}\n{person_locations}"
        )
        person_locations = [
            {k: f"There are: {len(v)} persons here"}
            for k, v in elevator.persons.items()
            if v
        ]

    response["details"] = {
        "Elevator Floor": elevator.current_floor,
        "Status": "Open" if elevator.is_open else "Moving",
        "Priority Queue": elevator.priority_queue,
        "Up Queue": elevator.up_queue,
        "Down Queue": elevator.down_queue,
        "Person Locations": person_locations,
    }
    return f"Moved {steps} step(s).\n{response}", 200


@app.route("/press_button", methods=["POST"])
def press_button():
    """
    Route to submit a request to the elevator system.

    Body:
        JSON list of buttons to press, each button must follow the format of
        {"source": int | str, "button": int | str | [int, str]}.

    Responses:
        - **200 OK**: "Succesfully pressed requested button(s)."
        - **400 OK**: "Submitted button(s) invalid, details show invalid button(s)."
    """
    new_request = request.get_json()

    response = {"Buttons": []}
    response_message = ""

    # Validate inputs
    for button in new_request:
        if isinstance(button.get("button"), int) and button.get("button") == 13 or isinstance(button.get("button"), list) and  13 in button.get("button"):
            response_message = (
                "Submitted button(s) invalid, details show invalid button(s)."
            )
            response["Buttons"].append(
                {
                    "source": button.get("source"),
                    "button": button.get("button"),
                }
            )

    if response["Buttons"]:
        return f"{response_message}\n{response}", 400
    response_message = "Succesfully pressed requested button(s)."

    for button in new_request:
        elevator.process_request(**button)
        response["Buttons"].append(
            {
                "source": button.get("source"),
                "button": button.get("button"),
            }
        )

    return f"{response_message}\n{response}", 200


@app.route("/create_person", methods=["POST"])
def create_person():
    """
    Route to add a person to the elevator system.

    Body:
        JSON list of persons to add, each person must follow the format of {"origin": int , "destination": int},
        with optional keys of {"weight": float, "cargo": float}.

    Responses:
        - **200 OK**: "Succesfully created requested person(s)."
        - **400 ERROR**: "Submitted person(s) invalid, details show invalid person(s)."
    """
    new_request = request.get_json()

    response = {"Persons": []}
    response_message = ""

    # Validate inputs
    for person in new_request:
        if person.get("origin") == 13 or person.get("destination") == 13:
            response_message = (
                "Submitted person(s) invalid, details show invalid person(s)."
            )
            response["Persons"].append(
                {
                    "origin": person.get("origin"),
                    "destination": person.get("destination"),
                }
            )

    if response["Persons"]:
        return f"{response_message}\n{response}", 400
    response_message = "Succesfully created requested person(s)."

    for person in new_request:
        new_person = Person(**person)
        elevator.add_person(new_person)
        response["Persons"].append(
            {
                "id": new_person.id,
                "origin": new_person.location,
                "destination": new_person.destination,
                "weight": new_person.weight,
                "cargo": new_person.cargo,
            }
        )

    return f"{response_message}\n{response}", 200


if __name__ == "__main__":
    app.run(debug=True, port=3148)
