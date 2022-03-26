from representation.village import Village


class Villager:
    def __init__(self, village: Village) -> None:
        self.name: str = ""

        self.village: Village = village

        self.isDead = False

        self.parentOf: list = []
        self.childOf: list = []

        self.job: str = "Unemployed"
        self.minecraftJob: str = "Unemployed"

        # [[0 -> content, 1 -> isGift], [...] , ...]
        self.diary: list = []
