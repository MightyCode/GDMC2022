import os
import json

CONFIG_PATH: str = "config/config.json"


def createConfig() -> dict:
    return {
        "debugMode": True
    }

def createConfigFile() -> dict:
    config: dict = createConfig()

    os.mkdir("config")
    with open(CONFIG_PATH, "w") as f:
        f.write(json.dumps(config))

    return config


def getOrCreateConfig() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    else:
        return createConfigFile()