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

## 0.3.0 (18 October 2024)
- Flask and Elevator run in separate and parallel processes.
- Updated health check endpoint to have a URI suffix.
- Added a playback speed constant.
