from utils.nameGenerator import NameGenerator

import random


class Village:
    TIER_LOW = 0
    TIER_MID = 1
    TIER_HIGH = 2

    def __init__(self) -> None:
        # Pre generation information
        self.name: str = ""
        self.tier: int = random.randint(0, 2)

        self.villageInteractions: list = []

        self.isDestroyed: bool = False

        # Within generation information
        self.villagers: list = []

    def generateVillageInformation(self, name_generator: NameGenerator):
        self.name = name_generator.generateVillageName(True)
