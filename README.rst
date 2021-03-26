Tratum
======

Tratum. Monilito web application made in Python / Django. Structured by Django Cookiecutter Project.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


Start Project from scrath
---------


Prerequisites
^^^^^^^^^^^^^

Download and install Docker

- [For Mac](https://download.docker.com/mac/stable/Docker.dmg)
- [For Windows](https://download.docker.com/win/stable/InstallDocker.msi)
- [For Linux](https://docs.docker.com/engine/getstarted/step_one/#docker-for-linux)


Local Setup
^^^^^^^^^^^^^
For local set up, you must build and run all docker containers running the next two commands in your terminal on root project path::
    
    $ docker-compose.yml -f local.yml build
    $ docker-compose.yml -f local.yml up

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html

After building and uploading the containers, access the django container and run the following basic commands.

For access to django container, execute the following command (the container id could be change in your machine, make sure the name typing `docker ps` and see the right container name)::

    $ docker exec -it minutas_django_1 sh

Then you have to export the environment variable from the database once inside the container::

    $ export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"


* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser 


Access the Django administrator via http://0.0.0.0:8000/ and use the credentials created in the previous step.

Go to Social Accounts -> Social Applications and create the same Facebook and Google account that you can find in the live env. https://tratum.co/admin. Use the credentials provided for your partner.

This step is necessary for the correct operation of the project locally.

Learn about Django Settings
--------

Visit the django cookiecutter documentation to get more detailed info about how to manage django settings in the project.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html


Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy tratum

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html


Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.


