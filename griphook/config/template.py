import trafaret

CONFIG_TEMPLATE = trafaret.Dict({
    'api': trafaret.String(),
    'cli': trafaret.String(),
    'tasks': trafaret.String(),
    'db': trafaret.String(),
})
