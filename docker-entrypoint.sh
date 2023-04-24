#!/usr/bin/env bash

set -e

cd assessment

if [ "$1" = "runserver" ]; then
    shift
    # Run server
    python manage.py runserver 0.0.0.0:8000
fi

if [ "$1" = "shell" ]; then
    shift
    # Run shell
    python manage.py shell
fi

if [ "$1" = "test" ]; then
    shift
    # Run tests
    python manage.py test
fi

if [ "$1" = "createsuperuser" ]; then
    shift
    # Create superuser
    python manage.py createsuperuser
fi

if [ "$1" = "makemigrations" ]; then
    shift
    # Create migrations
    python manage.py makemigrations
fi

if [ "$1" = "migrate" ]; then
    shift
    # Run migrations
    python manage.py migrate
fi

if [ "$1" = "collectstatic" ]; then
    shift
    # Collect static files
    python manage.py collectstatic --noinput
fi

exec "$@"
