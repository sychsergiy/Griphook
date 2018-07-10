import trafaret

template = trafaret.Dict({
    'api': trafaret.String(),
    'cli': trafaret.String(),
    'db': trafaret.String(),
    'tasks': trafaret.Dict({
        "DATA_SOURCE_DATA_EXPIRES": trafaret.String(),
        "CELERY_BROKER_URL": trafaret.String(),
        "TRYING_SETUP_PARSER_INTERVAL": trafaret.Int(),
        "PARSE_METRIC_EXPIRES": trafaret.Int(),
    })

})
