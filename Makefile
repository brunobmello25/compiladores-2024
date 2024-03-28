setup-venv:
	python -m venv venv

test:
	./venv/bin/pytest
