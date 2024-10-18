"""
app.py
Samuel Koller
Created: 15 October 2024
Updated: 17 October 2024

Main file for the Bluestaq Elevator Application. Houses the Flask server and relevant endpoints.

Functions:
    health_check(): A route to check if the service is running.
"""

__version__ = "0.3.0"

import multiprocessing
from time import sleep
from dotenv import load_dotenv
from flask import Flask, jsonify

from src.classes.elevator import Elevator

stop_queue = multiprocessing.Manager().list([2])

load_dotenv()
app = Flask(__name__)
elevator = Elevator()

@app.route("/", methods=["GET"])
def health_check():
    """
    Health check route to ping for application status. Returns a response message and status code.

    Responses:
        - **200 OK**: "Elevator is Online"

    Returns:
        JSON, int
    """
    return jsonify({"message": "Elevator is Online"}), 200

@app.route("/floor/<int:floor>", methods=["GET"])
def add_stop(floor):
    elevator.add_stop(floor)
    return jsonify({}), 200

def start_flask() -> None:
    app.run(debug=False, port=3148, )

if __name__ == "__main__":
    flask_process = multiprocessing.Process(target=start_flask, daemon=False)    
    flask_process.start()

    sleep(5)
    elevator_process = multiprocessing.Process(target=elevator.update, daemon=True)
    elevator_process.start()

    elevator_process.join()
    flask_process.terminate()
    flask_process.join()
