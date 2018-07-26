

## Local Installation without docker


Create and activate a virtual environment, and then install the requirements.
```sh
pip install -r requirements/dev.txt
```


### Set Environment Variables

Update *griphook/server/config.py*, and then run:

```sh
$ export APP_NAME="Flask Skeleton"
$ export APP_SETTINGS="griphook.server.config.DevelopmentConfig"
$ export FLASK_DEBUG=1
```

Using [python-dotenv](https://github.com/theskumar/python-dotenv) with *.env* file to set environment variables:

```sh
APP_NAME="Flask Skeleton"
APP_SETTINGS="griphook.server.config.DevelopmentConfig"
FLASK_DEBUG=1
```

### Create DB

```sh
$ python manage.py db migrate
```

### Run the Application


```sh
$ python manage.py run
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)

### Testing

Without coverage:

```sh
$ python manage.py test
```
or
```sh
$ pytest
```


With coverage:

```sh
$ python manage.py cov
```

Run flake8 on the app:

```sh
$ python manage.py flake
```

or

```sh
$ flake8 griphook
```

Also you can add your development commands to manage.py file