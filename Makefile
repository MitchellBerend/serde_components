full: test mypy black

.PHONY:
setup:
	@poetry install

.PHONY:
test:
	@poetry run pytest -vv

.PHONY:
mypy:
	@mypy serde_components/

.PHONY:
black:
	@black -S serde_components/

.PHONY:
update-dependencies:
	@poetry run pip freeze > dev-requirements.txt
