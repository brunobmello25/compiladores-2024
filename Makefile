setup-venv:
	python -m venv venv

example1:
	python -m src.main --token-file ./examples/example1/tokens.txt --input-file examples/example1/input.txt
