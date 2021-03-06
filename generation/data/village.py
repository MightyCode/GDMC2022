from utils.checkOrCreateConfig import Config
from utils.nameGenerator import NameGenerator

import random


class Village:
    STATE_PEACEFUL = "peaceful"
    STATE_WAR = "war"
    STATE_DESTROYED = "destroyed"

    DESTROYED_NONE = ""
    DESTROYED_WAR = "war"
    DESTROYED_PILLAGER = "pillager"

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

        self.position: list = [0, 0]

        self.village_interactions: dict = {}
        # Could be in war
        self.status = Village.STATE_PEACEFUL

        self.isDestroyed: bool = False
        self.destroyCause: str = ""

        self.generated: bool = False

        # Within generation information
        self.villagers: list = []
        self.dead_villagers: list = []
        self.lore_structures: list = []

        self.free_villager: int = 0

        self.murderer_data: MurdererData = MurdererData()

        self.color: str = "white"

    def generateVillageInformation(self, name_generator: NameGenerator):
        self.name = Config.getValueOrDefault("villageName", name_generator.generateVillageName(True))

    def defineTierAndAge(self):
        self.tier = random.randint(0, 2)
        self.age = 0

        if self.tier == 1:
            if random.uniform(0, 1) <= Village.CHANCE_TIER_2_OLD:
                self.age = 1
        elif self.tier == 2:
            if random.uniform(0, 1) <= Village.CHANCE_TIER_3_OLD:
                self.age = 1

        self.tier = Config.getValueOrDefault("villageTier", self.tier)
        self.age = Config.getValueOrDefault("villageAge", self.age)
        # print("Tier : " + str(self.tier) + ", Age : " + str(self.age))

    def generateVillageLore(self):
        self.defineTierAndAge()
        colors = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan",
                  "purple", "blue", "brown", "green"]

        self.color = Config.getValueOrDefault("villageColor", colors[random.randint(0, len(colors) - 1)])

    def makeRelations(self, otherVillages: list):
        for village in otherVillages:
            relation: VillageInteraction = VillageInteraction(self, village)

            village.addRelation(self, relation)
            self.addRelation(village, relation)

    def addRelation(self, otherVillage, relation):
        self.village_interactions[otherVillage] = relation

    def generateLoreAfterRelation(self):
        self.status = Village.STATE_PEACEFUL

        for key in self.village_interactions.keys():
            interaction = self.village_interactions[key]

            if interaction.state == VillageInteraction.STATE_WAR:
                self.status = Village.STATE_WAR

        self.status = Config.getValueOrDefault("villageStatus", self.status)


from generation.data.murdererData import MurdererData
from generation.data.villageInteraction import VillageInteraction
