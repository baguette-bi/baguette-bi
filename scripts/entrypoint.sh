#!/bin/bash
/home/baguette/.local/bin/poetry run baguette db init
/home/baguette/.local/bin/poetry run baguette docs --reload --host 0.0.0.0
