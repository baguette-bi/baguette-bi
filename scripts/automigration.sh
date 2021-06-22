#!/bin/bash
cd /home/baguette/baguette_bi/baguette_bi/alembic
poetry run alembic upgrade head
poetry run alembic revision --autogenerate -m "$1"
poetry run black .
