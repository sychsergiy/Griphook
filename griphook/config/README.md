# Configure app using .yml file

Create *.yml file and provide CONFIG_PATH env variable with relative path
```
export GH_CONFIG_FILE_NAME=griphook/*/*.yml
```
Or use default value ```config.yml``` (just a root of our project)

Import Config, class create instance and use options property:
```
config = Config()
config.options
```


### Current template have next structure:
```
{
    "api": {
        "GRAPHITE_URL": "url_here"
    },
    "db": {
        "DATABASE_URL": "url here"
    },
    "tasks": {
        "DATA_SOURCE_DATA_EXPIRES": 1,
        "CELERY_BROKER_URL": "String",
        "TRYING_SETUP_PARSER_INTERVAL": 1,
        "PARSE_METRIC_EXPIRES": 1,
        "DATA_GRANULATION": 1,
    },
}
```

### Example of config.yml file:
```
api:
  GRAPHITE_URL: url_here
db:
  DATABASE_URL: url here
tasks:
  DATA_SOURCE_DATA_EXPIRES: 1
  CELERY_BROKER_URL: test
  TRYING_SETUP_PARSER_INTERVAL: 1
  PARSE_METRIC_EXPIRES: 1
  DATA_GRANULATION: 1
```


### Also you can overwrite options using environment variables with GH_ prefix

```
export GH_YOUR_VARIABLE=value
```