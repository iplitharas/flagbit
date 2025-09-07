# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.DEFAULT_GOAL := help

create-env:
	python -m venv .env && source .env/bin/activate && pip install --upgrade pip

poetry-install: create-env
	  source .env/bin/activate && poetry install

install-hooks:
	poetry run  pre-commit install

setup-local-env: poetry-install install-hooks ## Setup the local environment 🔨🐍

test-cov: ## Run pytest with an html coverage report 🏁
	poetry run pytest . -vv -p no:warnings --cov=. --cov-report=xml --cov-report=html

test: ## Run pytest with coverage 🏁
	poetry run pytest . -vv -p no:warnings --cov=.

check: ## Run ruff formatter,linter and mypy static analyzer and check code quality 🧐
	poetry run ruff format src
	poetry run ruff check src
	poetry run mypy src

clean:  ## Clean temp dirs 🧹
	rm -rf  .pytest_cache coverage.xml .mypy_cache  .coverage .coverage.* htmlcov

clean-hooks: ## Clean hooks 🧹
	poetry run pre-commit clean

.PHONY: help create-env poetry-install install-hooks setup-local-env test test-cov \
 		 check clean-hooks clean

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)