# Changelog

## 0.1.0 (16 October 2024)
- Set up of the initial application, to include the flask server with a health check endpoint, pip requirements, linting/formatting tools, README.md, and CHANGELOG.md.
- Class files with pseudo-code.

## 0.1.1 (16 October 2024)
- Set up of the CI pipeline to check formatting and linting of the code (black, isort, pylint).

## 0.1.2 (17 October 2024)
- Set up of the testing file structure.
- Set up of the CI pipeline to check testing success and coverage (pytest, coverage).
- Modified linting and precommit scripts.
- Skeleton implementation of Elevator.

## 0.2.0 (17 October 2024)
- Elevator can queue requests in the proper order.

## 0.3.0 (19 October 2024)
- Flask and Elevator run in separate and parallel processes.
- Updated health check endpoint to have a URI suffix.
- Added a make request endpoint so a user can manually send a request to the elevator system.
- Added a state machine method in elevator to run the state machine a infinite/finite number of iterations.
- Added a top floor and playback speed constants.
- Added a TODO.md with future tasks.
- Added a requests.json, which is used as the queued requests "database", and added prepopulated data.

## 0.3.1 (19 October 2024)
- Removed multiprocessing and infinite state machine.
- Removed requests.json, data stored within Elevator.
- Added Endpoints to submit requests and persons.
