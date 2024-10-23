# Changelog

## 0.1

### 0.1.0 (16 October 2024)

- Set up of the initial application, to include the flask server with a health check endpoint, pip requirements, linting/formatting tools, README.md, and CHANGELOG.md.
- Class files with pseudo-code.

### 0.1.1 (16 October 2024)

- Set up of the CI pipeline to check formatting and linting of the code (black, isort, pylint).

### 0.1.2 (17 October 2024)

- Set up of the testing file structure.
- Set up of the CI pipeline to check testing success and coverage (pytest, coverage).
- Modify linting and precommit scripts.
- Skeleton implementation of Elevator.

## 0.2

### 0.2.0 (17 October 2024)

- Elevator can queue requests in the proper order.

## 0.3

### 0.3.0 (19 October 2024)

- Flask and Elevator run in separate and parallel processes.
- Updat health check endpoint to have a URI suffix.
- Add a make request endpoint so a user can manually send a request to the elevator system.
- Add a state machine method in elevator to run the state machine a infinite/finite number of iterations.
- Add a top floor and playback speed constants.
- Add a TODO.md with future tasks.
- Add a requests.json, which is used as the queued requests "database", and added prepopulated data.

### 0.3.1 (19 October 2024)

- Remove multiprocessing and infinite state machine.
- Remove requests.json, data stored within Elevator.
- Add Endpoints to submit requests and persons.

### 0.3.2 (19 October 2024)

- Elevator picks up and drops off persons.
- Elevator has new state of open to load and unload passengers.
- Elevator has capacity limits.

### 0.3.3 (20 October 2024)

- Correct bug in which elevator fails to turn around.

### 0.3.4 (20 October 2024)

- Remove the thirteenth floor.

### 0.3.5 (20 October 2024)

- Allow for priority stops.

## 0.4

### 0.4.0 (21 October 2024)

- Redesign the elevator to have three queues, up, down, and priority.
- Add detail to endpoint responses.

### 0.4.1 (22 October 2024)

- Correct bug in which when an elevator was filled to capacity and persons were left at the current floor, the floor was removed from the queue.

### 0.4.2 (22 October 2024)

- Add custom exceptions for person creation and button pressing.

# 1

## 1.0.0 (22 October 2024)

- Minimum viable product, with up-to-date documentation.
