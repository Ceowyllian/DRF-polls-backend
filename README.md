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

* [Table of contents](#table-of-contents)
* [System requirements](#system-requirements)
* [Installation](#installation)
    * [1 Create a DB and a user for the django project](#1-create-a-db-and-a-user-for-the-django-project)
    * [2 Clone this repo and install the dependencies](#2-clone-this-repo-and-install-the-dependencies)
    * [3 Configure the environment](#3-configure-the-environment)
    * [4 Create a DB schema and an administrator user](#4-create-a-db-schema-and-an-administrator-user)
* [Run the local server](#run-the-local-server)

<!-- TOC -->

## System requirements

- Python 3.10.2 or higher
- PostgreSQL 14 or higher

## Installation

All the steps described below were performed on a computer with `Windows 10` installed. If you are not using `Windows`,
you may need to replace some shell commands with those that match your OS.

### 1 Create a DB and a user for the django project

```sql
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

### 2 Clone this repo and install the dependencies

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

### 3 Configure the environment

To specify the environment variables simply create the `.env` file in the root directory, where the `manage.py` file is
located. Here is the list of all the variables:

| Variable                    | Example (plain text)                             | Default (Python value)         |
|-----------------------------|--------------------------------------------------|--------------------------------|
| DB_URL                      | `postgres://username:password@host:port/db_name` | `"postgres://django_polls_db"` |
| **SECRET_KEY** - necessary  | `PoTFPuiCcapnlgeYiKHMDY29SAlUj4lWkYBKOtztVDN`    | `None`                         |
| DJANGO_DEBUG                | `False`                                          | `False`                        |
| CORS_ALLOWED_ORIGINS        | `http://localhost:8080, https://example.com `    | `[]`                           |
| SECURE_CONTENT_TYPE_NOSNIFF | `True`                                           | `True`                         |

For more information, read the following articles:

- [Django "settings.py" file](https://docs.djangoproject.com/en/4.1/topics/settings/)
- ["django-environ" package](https://django-environ.readthedocs.io/en/latest/index.html)
  and [how to use multiple ".env" files](https://django-environ.readthedocs.io/en/latest/index.html)

### 4 Create a DB schema and an administrator user

Run manage.py commands to make migrations and create all the necessary DB tables:

```shell
python manage.py makemigrations
python manage.py migrate
```

Create an admin user using the following command (you will need to choose an email with username and create password):

```shell
 python manage.py createsuperuser
```

Now the application is ready to be launched and tested.

## Run the local server

```shell
python manage.py runserver
```

During this run will be used the settings from [base.py](/config/django/base.py). You can specify the Django settings
file by adding an environment variable to your run configuration (not in the file `.env`):

- `DJANGO_SETTINGS_MODULE=config.django.test`
- `DJANGO_SETTINGS_MODULE=config.django.production`
- `DJANGO_SETTINGS_MODULE=config.django.base` (default)
