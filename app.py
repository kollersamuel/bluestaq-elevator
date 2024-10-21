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

__version__ = "0.3.5"


import logging

from dotenv import load_dotenv
from flask import Flask, Response, request

from src.classes.elevator import Elevator
from src.classes.person import Person

load_dotenv()
app = Flask(__name__)
elevator = Elevator()
elevator.current_floor=5


logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger("Elevator")


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check route to ping for application status.

    Responses:
        - **200 OK**: "Elevator is Online"
    """
    return Response("Elevator is Online", status=200)


@app.route("/step/<int:steps>", methods=["GET"])
def step(steps: int):
    """
    Route to submit a request to the elevator system.

    Parameters:
        steps (int): The number of steps to take.

    Responses:
        - **200 OK**: "Moved 0 steps."
    """
    for _ in range(steps):
        elevator.update()
        logger.debug(
            f"After this step, the elevator is now at {elevator.current_floor} and "
            f"has a status of  and a queue of stops for these floors: {elevator.priority_queue}, {elevator.up_queue}, {elevator.down_queue}."
        )
        # pylint: disable=expression-not-assigned
        [
            logger.debug(
                f"Currently, there are: {len(v)} persons in the location of {k}"
            )
            for k, v in elevator.persons.items()
            if v
        ]
        # pylint: enable: expression-not-assigned

    logger.info(
        f"After {steps} step(s), the elevator is now at {elevator.current_floor} and "
        f"has a status of and a queue of stops for these floors: {elevator.priority_queue}, {elevator.up_queue}, {elevator.down_queue}."
    )
    return Response(f"Moved {steps} steps.", status=200)


@app.route("/press_button", methods=["POST"])
def press_button():
    """
    Route to submit a request to the elevator system.

    Body:
        JSON list of buttons to press, each button must follow the format of {"source": int | str, "button": int | str}.

    Responses:
        - **200 OK**: "Pushed requested button(s)"
    """
    new_request = request.get_json()

    # pylint: disable=expression-not-assigned
    [elevator.process_request(**button) for button in new_request]
    # pylint: enable=expression-not-assigned

    return Response("Pushed requested button(s).", status=200)


@app.route("/create_person", methods=["POST"])
def create_person():
    """
    Route to add a person to the elevator system.

    Body:
        JSON list of persons to add, each person must follow the format of {"origin": int , "destination": int},
        with optional keys of {"weight": float, "cargo": float}.

    Responses:
        - **200 OK**:
            "Created Person 0 with the following attributes: Origin: 1, Destination: 2, Weight: 150, Cargo: 25."
    """
    new_request = request.get_json()

    res_msg = ""

    # Validate inputs
    for person in new_request:
        if person.get("origin") == 13 or person.get("destination") == 13:
            return Response("One of the submitted persons was invalid", status=400)

    for person in new_request:
        new_person = Person(**person)
        elevator.add_person(new_person)
        res_msg += (
            f"Created Person {new_person.id} with the following attributes: Origin: {new_person.location}, "
            f"Destination: {new_person.destination}, Weight: {new_person.weight}, Cargo: {new_person.cargo}.\n"
        )

    return Response(res_msg, status=200)


if __name__ == "__main__":
    app.run(debug=True, port=3148)
