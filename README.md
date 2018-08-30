# Griphook

## About

Griphook

![griphook-logo](griphook.png)

Server monitoring and billing service

## How to set up project locally

Clone the repository

```bash
git clone http://git.interns.evo/EVO2018-Vlad-team/Griphook
```

Choose installation method and go ahead

1. [Using Docker](setup-with-docker.md)
1. [Without Docker](setup-without-docker.md)


### How to run data fetcher:

Worker
```bash
celery -A griphook.tasks.tasks worker -l INFO
```

Scheduler
```bash
python3 griphook/tasks/task_scheduler.py
```

## Cli usage

```
Usage: manage.py [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  admin
  create_data  Creates sample data.
  create_db
  db           Perform database migrations.
  drop_db      Drops the db tables.
  flake        Runs flake8 on the griphook.
  routes       Show the routes for the app.
  run          Runs a development server.
  shell        Runs a shell in the app context.
```

***Dont forget to create admin user***

```bash
python manage.py admin create
``` 

To edit admins password 

```bash
python manage.py admin set_password
```
