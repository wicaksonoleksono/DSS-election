import json


class Config:
    def __init__(self, config_file="config.json"):
        with open(config_file) as f:
            config_data = json.load(f)
        self.FIREBASE_CREDENTIALS = config_data.get("FIREBASE_CREDENTIALS")


def get_config():
    return Config()
