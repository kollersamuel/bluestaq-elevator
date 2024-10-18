from dotenv import load_dotenv
from flask import Flask, jsonify

import threading
from time import sleep


class Elevator:
    def __init__(self) -> None:
        self.current_floor: int = 1
        self.stop_queue: list[int] = [100]

        self.lock = threading.Lock()
        threading.Thread(target=self.update, daemon=True).start()

    def update(self) -> None:
        while True:
            if self.current_floor != self.stop_queue[0]:
                self.move()
            sleep(0.001)

    def move(self) -> None:
        with self.lock:                
            if self.stop_queue[0] > self.current_floor:
                sleep(1)
                self.current_floor += 1
            elif self.stop_queue[0] < self.current_floor:
                sleep(1)
                self.current_floor -= 1
            app.logger.debug(f"Current floor: {self.current_floor}")

    def add_stop(self, requested_floor) -> None:
        with self.lock:
            self.stop_queue.append(requested_floor)

        app.logger.debug(self.stop_queue)

load_dotenv()
app = Flask(__name__)
elevator = Elevator()

@app.route("/floor/<int:floor>", methods=["GET"])
def add_stop(floor):
    elevator.add_stop(floor)
    return jsonify({"status": "stop added", "floor": floor})

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded = True)
