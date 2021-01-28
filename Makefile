help:
	@echo "  install       install dependencies"
	@echo "  fix           fix style code convention"

install:
	poetry install

fix:
	poetry run isort **/*.py