

## Local Installation docker


RUN with docker-compose.
```sh
docker-compose run --build
```

RUN tests with docker-compose.
```sh
docker-compose build
docker-compose -f compose-test.yml run pytest
```