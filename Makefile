.PHONY: dist

install_test_requirements:
	pip install -r test-requirements.txt

run_tests:
	pytest --cov=firmware/lib
	coverage xml
	coverage report --fail-under=80

dist:
	mkdir -p dist
	cp -r firmware/* dist
	python -m upip install -r requirements.txt -p 'dist/'