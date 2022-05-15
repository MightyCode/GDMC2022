import os
import json


class Config:
    CONFIG_PATH: str = "config/config.json"

    @staticmethod
    def createConfig() -> dict:
        return {
            "debugMode": True,
            "villageTier": {
                "state": False,
                "value": 0
            },
            "villageAge": {
                "state": False,
                "value": 0
            },
            "villageDestroyed": {
                "state": False,
                "value": True
            }
        }

    LOADED_CONFIG: dict = createConfig()

    @staticmethod
    def createConfigFile() -> dict:
        config: dict = Config.createConfig()

        os.mkdir("config")
        with open(Config.CONFIG_PATH, "w") as f:
            f.write(json.dumps(config))

        return config

    @staticmethod
    def getOrCreateConfig():
        if os.path.exists(Config.CONFIG_PATH):
            with open(Config.CONFIG_PATH) as f:
                Config.LOADED_CONFIG = json.load(f)
        else:
            Config.LOADED_CONFIG = Config.createConfigFile()

    @staticmethod
    def getValueOrDefault(valueName: str, defaultValue):
        if valueName in Config.LOADED_CONFIG.keys():
            if Config.LOADED_CONFIG[valueName]["state"]:
                return Config.LOADED_CONFIG[valueName]["value"]

        return defaultValue
