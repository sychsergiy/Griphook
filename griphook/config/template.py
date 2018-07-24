import trafaret

template = trafaret.Dict({
    "api": trafaret.Dict({
        "GRAPHITE_URL": trafaret.String(),
    }),
    "db": trafaret.Dict({
        "DATABASE_URL": trafaret.String(),
    }),
    "tasks": trafaret.Dict({
        # How long data in data source is saved.
        # now - DATA_SOURCE_DATA_EXPIRES -> start point for parsing
        # if no data in db.
        "DATA_SOURCE_DATA_EXPIRES": trafaret.Int(),
        "CELERY_BROKER_URL": trafaret.String(),
        "MAX_PARSE_TASKS_IN_QUEUE": trafaret.Int(),        
        # Time limit for parse task. (seconds)
        "PARSE_METRIC_EXPIRES": trafaret.Int(),
        # Time interval between filling task queue. (seconds)
        "FILLING_TASK_QUEUE_INTERVAL": trafaret.Int(),
        # Time interval between creating batches until now. (seconds)
        "CREATING_BATCHES_INTERVAL": trafaret.Int(),
    })
})
