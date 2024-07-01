import json


def get_config():
    with open('config/config.json', 'r') as file:
        config = json.load(file)
    return config


def get_property(key):
    config = get_config()
    return config.get(key)
