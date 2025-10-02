# General notes

## Basic Commands

!!! tip
    If running the stack using docker, `<prefix>` the commands with `docker compose -f docker-compose.local.yml run --rm django python`

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:
      ```sh
      <prefix> uv run python manage.py createsuperuser
      ```
For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    ```sh
    <prefix> uv run mypy django_template
    ```

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    ```sh
    <prefix> uv run coverage run -m pytest
    <prefix> uv run coverage html
    <prefix> uv run open htmlcov/index.html
    ```

#### Running tests with pytest

    ```sh
    <prefix> uv run pytest
    ```

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html#using-webpack-or-gulp).

### Celery

This app comes with Celery.

To run a celery worker:

```sh
cd django_template
<prefix> uv run celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd django_template
<prefix> uv run celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```sh
cd django_template
<prefix> uv run celery -A config.celery_app worker -B -l info
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [Mailpit](https://github.com/axllent/mailpit) with a web interface is available as docker container.

Container mailpit will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally-docker.html) for more details how to start all containers.

With Mailpit running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html).


## Filtering Docker Compose Containers

Docker does not record which `compose.local.yml` file created a container.
Direct filtering by compose file name is not possible.

### Approach 1: Manual Labels

Add labels manually to each service:

```yaml
labels:
  - source=compose.local.yml
```

### Usage

Filter containers:

```bash
docker ps --filter "label=source=compose.local.yml"
```

### Downsides

* Duplication across every service in YAML.
* Typos or inconsistencies break filtering.
* Extra cognitive overhead for contributors.
* Risk of drift across environments (dev, prod).
* Labels are visible via `docker inspect` → metata leakage.
* No enforcement by Docker.

### Approach 2: Using `-p` Project Name (Recommended)

Run compose with an explicit project name:

```sh
docker compose -f compose.local.yml -p local up -d
```

Even `docker compose down` must use the same -p <project_name> that was used to bring the stack up. For any docker compose command that targets a project (including --rm clean-up options), you must also pass the same -p <project_name>.

Docker auto-labels all resources:

```sh
com.docker.compose.project=local
```

### Usage

Filter containers:

```bash
docker ps --filter "label=com.docker.compose.project=local"
```

### Advantages

* No YAML edits.
* Enforced automatically by Docker Compose.
* Consistent across all services.
* Lower maintenance overhead.

### Downsides

* Must remember to always pass `-p local`.
* Forgetting `-p` daults to directory name, which creates a different project stack.

### Best Practice

* Always
nvironment>` for clear separation:


  * `-p local`
  * `-p staging`
  * `-p prod`
