import os
import json


class Config:
    CONFIG_PATH: str = "config/config.json"

    @staticmethod
    def createConfig() -> dict:
        return {
            "timeLimit": 600,
            "villageWall": "convexHull",
            "shouldShowWallSchematic": False,
            "minVillageStructure": 25,
            "maxVillageStructure": 55,
            "saveConstructionInFile": True,
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
            },
            "villageDestroyedCause": {
                "state": False,
                "value": "war",
            },
            "villageName": {
                "state": False,
                "value": "Test"
            },
            "villageRelationShip": {
                "state": False,
                "value": 0
            },
            "villageStatus": {
                "state": False,
                "value": "war"
            },
            "villageColor": {
                "state": False,
                "value": "blue"
            },
            "numberStructures": {
                "state": False,
                "value": 10
            }
        }

    LOADED_CONFIG: dict = {}

    @staticmethod
    def createConfigFile() -> dict:
        config: dict = Config.createConfig()

        print(os.mkdir("config"))
        with open(Config.CONFIG_PATH, "w") as f:
            f.write(json.dumps(config, indent=4, sort_keys=True))

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
        if Config.LOADED_CONFIG[valueName]["state"]:
            return Config.LOADED_CONFIG[valueName]["value"]

        return defaultValue
