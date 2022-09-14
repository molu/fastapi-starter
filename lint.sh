#!/bin/bash
poetry run black app
poetry run isort app
poetry run flake8 app
