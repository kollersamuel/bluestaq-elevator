python -m black .
python -m isort .
(echo -e "Pylint Report Generated: $(date -u +%Y-%m-%dT%H:%M:%S%Z):\n" && python -m pylint . --output-format=text) > pylint_results.txt
