# Configure app using .yml file

Create *.yml file and provide GH_CONFIG_FILE_NAME env variable with relative path
```bash
export GH_CONFIG_FILE_NAME=griphook/**/*.yml
```
Or use default value ```config.yml``` (just a root of our project).

Recommended to use local.yml file for local development. Create `local.yml` file.
Provide your local settings there and set env variable to use it:

```bash
export GH_CONFIG_FILE_NAME=local.yml
```

Import Config, class create instance and use options property:
```python
from griphook.config import Config

config = Config()
settings = config.options
```


### Current template have next structure:
```json
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
```yaml
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

```bash
export GH_YOUR_VARIABLE=value
```