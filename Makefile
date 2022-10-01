install_test_requirements:
	pip install -r test-requirements.txt

run_tests:
	pytest --cov=firmware/lib
	coverage report --fail-under=80
