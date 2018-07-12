# Configure app using .yml file

Create *.yml file and provide CONFIG_PATH env variable with relative path
```
export GH_DEFAULT_CONFIG_FILE_NAME=/griphook/tasks/config.yml
```
Or use default value ```config.yml``` (just a root of our project)

Import Config class create instance and use options property:
```
config = Config()
config.options
```


### Current template have next structure:
```
{
    "api": {
        "GRAPHITE_URL": "String",
    },
    "db": {
        "DATABASE_URL": "String",
    },
    "tasks": {
        "DATA_SOURCE_DATA_EXPIRES": "String",
        "CELERY_BROKER_URL": "String",
        "BROKER_DATABASE_URL": "String",
        "TRYING_SETUP_PARSER_INTERVAL": "Int",
        "PARSE_METRIC_EXPIRES": "Int",
    }
})
```

### Example of config.yml file:
```
api:
  GRAPHITE_URL: url_here
db:
  DATABASE_URL: url here
tasks:
  BROKER_DATABASE_URL: url here
  CELERY_BROKER_URL: test
  DATA_SOURCE_DATA_EXPIRES: test
  PARSE_METRIC_EXPIRES: 1
  TRYING_SETUP_PARSER_INTERVAL: 1
```


### Also you can overwrite options using environment variables with GH_ prefix

```
export GH_BROKER_DATABASE_URL=value
```