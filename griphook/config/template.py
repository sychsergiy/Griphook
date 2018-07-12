import trafaret

template = trafaret.Dict({
    "api": trafaret.Dict({
        "GRAPHITE_URL": trafaret.String(),
    }),
    "db": trafaret.Dict({
        "DATABASE_URL": trafaret.String(),
    }),
    "tasks": trafaret.Dict({
        "DATA_SOURCE_DATA_EXPIRES": trafaret.Int(),
        "CELERY_BROKER_URL": trafaret.String(),
        "TRYING_SETUP_PARSER_INTERVAL": trafaret.Int(),
        "PARSE_METRIC_EXPIRES": trafaret.Int(),
        "DATA_GRANULATION": trafaret.Int(),
    })
})
