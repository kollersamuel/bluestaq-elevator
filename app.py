"""
app.py
Samuel Koller
Created: 15 October 2024
Updated: 18 October 2024

Main file for the Bluestaq Elevator Application. Houses the Flask server and relevant endpoints.

Functions:
    health_check(): A route to check if the service is running.
"""

__version__ = "0.3.0"

import json
import multiprocessing
from time import sleep

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from src.classes.elevator import Elevator

# from src.utils.request_queue import stop_queue

load_dotenv()
app = Flask(__name__)
elevator = Elevator([])


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check route to ping for application status. Returns a response message and status code.

    Responses:
        - **200 OK**: "Elevator is Online"

    Returns:
        JSON, int
    """
    return jsonify({"message": "Elevator is Online"}), 200


@app.route("/request", methods=["POST"])
def make_request():
    new_request = request.get_json()

    with open("./requests.json", "r") as requests_json:
        requests = json.load(requests_json)
    requests.append(new_request)
    with open("./requests.json", "w") as requests_json:
        json.dump(requests, requests_json, indent=2)

    return jsonify({}), 200


def start_flask() -> None:
    """Runs the app via a function, so it can be used with multiprocessing."""
    # ! NOTE: This will NOT work in debug mode !
    app.run(debug=False, port=3148)


if __name__ == "__main__":
    flask_process = multiprocessing.Process(target=start_flask, daemon=False)
    flask_process.start()

    sleep(5)
    elevator_process = multiprocessing.Process(
        target=elevator.start_state_machine, daemon=True
    )
    elevator_process.start()

    elevator_process.join()
    flask_process.terminate()
    flask_process.join()
