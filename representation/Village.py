from representation.VillageInteraction import VillageInteraction 

import random

class Village:
    TIER_LOW = 0
    TIER_MID = 1
    TIER_HIGH = 2

    def __init__(self) -> None:
        self.name:str = ""
        self.biomeId:int = 0
        self.tier:int = random.randint(0, 2)

        self.villageInteractions:tuple = []

        self.isDestroyed:bool = False