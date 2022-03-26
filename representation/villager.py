from representation.village import Village
import random


class Villager:
    VILLAGE_PROFESSION_LIST = [
        "farmer", "fisherman", "shepherd", "fletcher", "librarian", "cartographer",
        "cleric", "armorer", "weaponsmith", "toolsmith", "butcher", "leatherworker", "mason", "nitwit"]

    def __init__(self, village: Village) -> None:
        self.name: str = ""

        self.village: Village = village

        self.isDead = False

        self.parentOf: list = []
        self.childOf: list = []

        self.job: str = "Unemployed"
        self.minecraftJob: str = "Unemployed"

        # Profession level of the villager (2: Apprentice, 3: Journeyman, 4: Expert, 5: Master)
        self.jobLevel = random.randint(2, 5)

        # [[0 -> content, 1 -> isGift], [...] , ...]
        self.diary: list = []

        self.trades: list = []

    def hasNoTrade(self) -> bool:
        return len(self.trades) <= 0
