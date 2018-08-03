# Griphook

## About

Server monitoring and billing service

## Installation

```bash
git clone http://git.interns.evo/EVO2018-Vlad-team/Griphook
cd Griphook
export PYTHONPATH=$PWD

```

To run data fetcher:
```bash
python manage.py run_fetcher --celery_args='-l INFO'
``` 


To install flask app
1. [setup-with-docker.md](setup-with-docker.md)
1. [setup-without-docker.md](setup-without-docker.md)
