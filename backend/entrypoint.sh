#!/bin/sh
set -e
alembic upgrade head
flask run