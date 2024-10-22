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
from flask import Flask, Response, jsonify, request

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
        - **200 OK**: "Moved 0 steps."
    """
    for _ in range(steps):
        elevator.update()
        logger.debug(
            f"After this step, the elevator is now at {elevator.current_floor} and "
            f"has a status of {'Open' if elevator.is_open else 'Moving'} and a queue of stops for these floors: Priority: {elevator.priority_queue}, Up: {elevator.up_queue}, Down: {elevator.down_queue}."
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
        f"has a status of {'Open' if elevator.is_open else 'Moving'} and a queue of stops for these floors: Priority: {elevator.priority_queue}, Up: {elevator.up_queue}, Down: {elevator.down_queue}."
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
        - **200 OK**: "Succesfully created requested persons."
        - **400 ERROR**: "Submitted person(s) invalid, details show invalid persons."
    """
    new_request = request.get_json()

    response = {"message": "", "details": []}

    # Validate inputs
    for person in new_request:
        if person.get("origin") == 13 or person.get("destination") == 13:
            response["message"] = (
                "Submitted person(s) invalid, details show invalid persons."
            )
            response["details"].append(
                {
                    "origin": person.get("origin"),
                    "destination": person.get("destination"),
                }
            )

    if response["details"]:
        return jsonify(response), 400
    response["message"] = "Succesfully created requested persons."

    for person in new_request:
        new_person = Person(**person)
        elevator.add_person(new_person)
        response["details"].append(
            {
                "id": new_person.id,
                "origin": new_person.location,
                "destination": new_person.destination,
                "weight": new_person.weight,
                "cargo": new_person.cargo,
            }
        )

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True, port=3148)
