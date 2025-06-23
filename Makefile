SHELL := /bin/bash

# ---

# Read default configuration
include config.default
export $(shell sed 's/=.*//' config.default)

# ---

YAMLLINT := $(shell command -v yamllint 2> /dev/null)
FLAKE8 := $(shell command -v flake8 2> /dev/null)
GCLOUD := $(shell command -v gcloud 2> /dev/null)

# ---

SRC := src

# ---

.DEFAULT_GOAL := all

.PHONY: all lint lint-yaml lint-py deploy

all: lint deploy

lint: lint-yaml lint-py

lint-yaml:
ifndef YAMLLINT
	$(error "yamllint is not installed: https://github.com/adrienverge/yamllint")
endif
	@$(YAMLLINT) -d "{extends: default, rules: {line-length: disable}}" .circleci/config.yml

lint-py:
ifndef FLAKE8
	$(error "flake8 is not installed: https://pypi.org/project/flake8/")
endif
	@flake8

deploy:
ifndef GCLOUD
	$(error "gcloud is not installed: https://cloud.google.com/sdk/gcloud")
endif
	@gcloud functions deploy $(FUNCTION_NAME) \
		--entry-point $(ENTRYPOINT) \
		--runtime $(PYTHON_VERSION) \
		--trigger-http \
		--source ./src/ \
		--project $(GOOGLE_PROJECT_ID) \
		--region $(REGION) \
		--set-env-vars CIRCLE_TOKEN=$(CIRCLE_TOKEN)
