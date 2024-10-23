python -m black . --quiet
python -m isort . --quiet
(echo -e "Pylint Report Generated $(date -u +%Y-%m-%dT%H:%M:%S%Z):\n" && python -m pylint . --output-format=text) > linting_report.txt
(echo -e "Coverage Report Generated $(date -u +%Y-%m-%dT%H:%M:%S%Z):\n" && python -m coverage run -m pytest -vv . && python -m coverage report -m) > testing_report.txt
echo "Precommit finished running, see ./linting_report.txt and ./testing_report.txt for results."
