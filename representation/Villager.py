from this import d
from representation.Village import Village

class Villager:
    def __init__(self, village:Village) -> None:
        self.name:str = ""

        self.village:Village = village

        self.isDead = False

        self.parentOf:tuple = []
        self.childOf:tuple = []


        self.job:str = "Unemployed"