from generation.data.village import Village
import random


class Villager:
    DEFAULT_JOB = "Unemployed"
    DEFAULT_MINECRAFT_JOB = "nitwit"

    VILLAGE_PROFESSION_LIST = [
        "farmer", "fisherman", "shepherd", "fletcher", "librarian", "cartographer",
        "cleric", "armorer", "weaponsmith", "toolsmith", "butcher", "leatherworker", "mason", "nitwit"]

    def __init__(self, village: Village) -> None:
        self.name: str = ""

        self.village: Village = village

        self.parentOf: list = []
        self.childOf: list = []

        self.job: str = Villager.DEFAULT_JOB
        self.minecraftJob: str = Villager.DEFAULT_MINECRAFT_JOB

        # Profession level of the villager (2: Apprentice, 3: Journeyman, 4: Expert, 5: Master)
        self.jobLevel = random.randint(2, 5)

        # [[0 -> content, 1 -> isGift], [...] , ...]
        self.diary: list = []

        self.trades: list = []

        self.reason_death: str = ""

    def hasNoTrade(self) -> bool:
        return len(self.trades) <= 0
