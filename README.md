# DRF polls backend

[![](https://github.com/Ceowyllian/DRF-polls-backend/actions/workflows/django.yml/badge.svg)](https://github.com/Ceowyllian/DRF-polls-backend/actions/workflows/django.yml)
[![](https://codecov.io/gh/Ceowyllian/DRF-polls-backend/branch/master/graph/badge.svg?token=DDAU4GIT09)](https://codecov.io/gh/Ceowyllian/DRF-polls-backend)
[![](https://img.shields.io/github/license/Ceowyllian/DRF-polls-backend?color=blue&label=License)](https://github.com/Ceowyllian/DRF-polls-backend/blob/master/LICENSE)
[![](https://img.shields.io/github/pipenv/locked/dependency-version/Ceowyllian/DRF-polls-backend/django?label=Django)](https://www.djangoproject.com)
[![](https://img.shields.io/github/pipenv/locked/dependency-version/Ceowyllian/DRF-polls-backend/djangorestframework?label=REST+Framework)](https://www.django-rest-framework.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?label=Code+style)](https://github.com/psf/black)

This is an API for the voting service inspired by
the [tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/) in the Django docs.  
The project structure and some architecture concepts are taken from
the [Django Styleguide](https://github.com/HackSoftware/Django-Styleguide).
I also want to thank [qaa-engineer](https://github.com/qaa-engineer/) for his deployment
[guide](https://github.com/qaa-engineer/deploy-django) (some installation steps are taken from there).
___

## Table of contents

<!-- TOC -->

* [DRF polls backend](#drf-polls-backend)
    * [Table of contents](#table-of-contents)
    * [System requirements](#system-requirements)
    * [Installation](#installation)
        * [Create a DB and a user for the django project](#create-a-db-and-a-user-for-the-django-project)
        * [Clone this repo and install the dependencies](#clone-this-repo-and-install-the-dependencies)
        * [Configure the environment](#configure-the-environment)
        * [Create a DB schema and an administrator user](#create-a-db-schema-and-an-administrator-user)
    * [Run](#run)
        * [Local development server](#local-development-server)

<!-- TOC -->

## System requirements

- Python 3.10.2 or higher
- PostgreSQL 14 or higher

## Installation

All the steps described below were performed on a computer with `Windows 10` installed. If you are not using `Windows`,
you may need to replace some shell commands with those that match your OS.

### Create a DB and a user for the django project

```postgresql
-- Create database named "django_polls_db".
CREATE DATABASE django_polls_db;

-- Create user "django_polls_user". Be sure to use a secure password.
CREATE USER django_polls_user WITH PASSWORD 'password';

-- Set connection parameters for the user.
ALTER ROLE django_polls_user SET client_encoding TO 'utf8';
ALTER ROLE django_polls_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_polls_user SET timezone TO 'UTC';

-- Grant the created user access to administer the new database.
GRANT ALL PRIVILEGES ON DATABASE django_polls_db TO django_polls_user;
```

### Clone this repo and install the dependencies

Clone branch `master` and switch to the project directory (make sure you have `git` and `python` installed in
your `PATH` variable):

```shell
git clone https://github.com/Ceowyllian/DRF-polls-backend.git
cd DRF-polls-backend
```

Create and activate virtual environment. Install all the necessary packages using `pip` (it may take a few minutes):

```shell
python -m venv .\venv
venv\Scripts\activate
pip install -r requirements\base.txt -r requirements\local.txt
```

### Configure the environment

To specify the environment variables simply create the `.env` file in the root directory, where the `manage.py` file is
located.

You can specify the path to another file with variables using the `ENV_PATH` variable (e.g. place it in
the `.env` file). Here is the list of the required variables:

| Variable                   | Example (plain text)                             | Default (Python value) |
|----------------------------|--------------------------------------------------|------------------------|
| **DB_URL** - necessary     | `postgres://username:password@host:port/db_name` | `None`                 |
| **SECRET_KEY** - necessary | `PoTFPuiCcapnlgeYiKHMDY29SAlUj4lWkYBKOtztVDN`    | `None`                 |
| DJANGO_DEBUG               | `False`                                          | `False`                |
| CORS_ALLOWED_ORIGINS       | `http://localhost:8080, https://example.com `    | `[]`                   |
| ENV_PATH                   | `env\production.env`                             | `".env"`               |

For more information, read the following articles:

- [Django "settings.py" file](https://docs.djangoproject.com/en/4.1/topics/settings/)
- ["django-environ" package](https://django-environ.readthedocs.io/en/latest/index.html)
  and [how to use multiple ".env" files](https://django-environ.readthedocs.io/en/latest/index.html)

### Create a DB schema and an administrator user

Run manage.py commands to make migrations and create all the necessary DB tables:

```shell
python manage.py makemigrations
python manage.py migrate
```

Create an admin user using the following command (you will need to choose an email with username and create password):

```shell
 python manage.py createsuperuser
```

## Run

### Local development server

```shell
python manage.py runserver
```
