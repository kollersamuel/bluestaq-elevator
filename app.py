"""
app.py
Samuel Koller
Created: 15 October 2024
Updated: 16 October 2024

Main file for the Bluestaq Elevator Application. Houses the Flask server and relevant endpoints.

Functions:
    health_check(): A route to check if the service is running.
"""

__version__ = "0.1.1"

import os

from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

app = Flask(__name__)


debug: str = os.getenv("DEBUG", "False")
port: str = os.getenv("PORT", "5000")


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


if __name__ == "__main__":
    app.run(debug=debug, port=port)
