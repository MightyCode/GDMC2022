import random


class LoreStructure:
    CHANCE_VILLAGE_YOUNG_TIER_2_OLD = 0.05
    CHANCE_VILLAGE_OLD_TIER_2_OLD = 0.3
    CHANCE_VILLAGE_YOUNG_TIER_3_OLD = 0.07
    CHANCE_VILLAGE_OLD_TIER_3_OLD = 0.4

    EXCLUDED_FROM_AGE = ["townhall"]

    TYPE_HOUSES = "houses"
    TYPE_FUNCTIONALS = "functionals"
    TYPE_REPRESENTATIVES = "representatives"

    def __init__(self):
        self.age: int = 0
        self.name: str = ""

        self.rotation: int = 0
        self.flip: int = 0

        self.type: str = "None"
        self.group: str = "None"
        self.villagers: list = []
        self.gift: str = "Undefined"

        self.position: list = []
        self.validPosition: list = []
        self.prebuildingInfo: dict = {}

        self.destroyed: bool = False
        self.causeDestroy: bool = {}
        self.inConstruction: bool = False

    def generateAge(self, village):
        if village.tier == 0:
            return

        for excluded in LoreStructure.EXCLUDED_FROM_AGE:
            if excluded in self.name.lower():
                return

        if village.tier == 1:
            if village.age == 0 and random.uniform(0, 1) <= LoreStructure.CHANCE_VILLAGE_YOUNG_TIER_2_OLD:
                self.age = 1

            if village.age == 1 and random.uniform(0, 1) <= LoreStructure.CHANCE_VILLAGE_OLD_TIER_2_OLD:
                self.age = 1
        else:
            if village.age == 0 and random.uniform(0, 1) <= LoreStructure.CHANCE_VILLAGE_YOUNG_TIER_3_OLD:
                self.age = 1

            if village.age == 1 and random.uniform(0, 1) <= LoreStructure.CHANCE_VILLAGE_OLD_TIER_3_OLD:
                self.age = 1
