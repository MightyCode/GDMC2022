from utils.nameGenerator import NameGenerator

import random


class Village:
    TIER_LOW = 0
    TIER_MID = 1
    TIER_HIGH = 2

    CHANCE_TIER_2_OLD = 0.2
    CHANCE_TIER_3_OLD = 0.2

    # Incremented to have unique id for each village
    ID = 0

    def __init__(self) -> None:
        # Pre generation information
        self.id = Village.ID
        Village.ID += 1

        self.name: str = ""
        self.tier: int = 0
        # 0 is young village, 1 represents old village
        self.age: int = 0

        self.villageInteractions: dict = {}

        self.isDestroyed: bool = False

        self.generated: bool = False

        # Within generation information
        self.villagers: list = []
        self.deadVillager: list = []
        self.lore_structures: list = []

        self.free_villager: int = 0

        self.murderer_data: MurdererData = MurdererData()

        self.color: str = "Undefined"

    def defineTierAndAge(self):
        self.tier = random.randint(0, 2)
        self.age = 0

        if self.tier == 1:
            if random.uniform(0, 1) <= Village.CHANCE_TIER_2_OLD:
                self.age = 1
        elif self.tier == 2:
            if random.uniform(0, 1) <= Village.CHANCE_TIER_3_OLD:
                self.age = 1

    def makeRelation(self, otherVillages: list):
        for village in otherVillages:
            relation: VillageInteraction = VillageInteraction(self, village)

            self.villageInteractions[village.id] = relation
            village.addRelation(self, relation)

    def addRelation(self, otherVillage, relation):
        self.villageInteractions[otherVillage.id] = relation

    def generateVillageInformation(self, name_generator: NameGenerator):
        self.name = name_generator.generateVillageName(True)

    def generateVillageLore(self):
        if len(self.villagers) > 1:
            index = random.choice([i for i in range(0, len(self.villagers)) if
                                   self.villagers[i].job != "Mayor"])

            self.murderer_data.villagerIndex = self.villagers[index]

            index = random.choice(
                [i for i in range(0, len(self.villagers)) if i != self.murderer_data.villagerIndex])

            self.murderer_data.villagerTargetIndex = self.villagers[index]

        for structure in self.lore_structures:
            if self.murderer_data.villagerTarget in structure.villagers:
                structure.gift = "minecraft:tnt"


from generation.data.murdererData import MurdererData
from representation.villageInteraction import VillageInteraction
