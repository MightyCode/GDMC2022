from generation.resources import Resources
from generation.data.murdererData import MurdererData
from representation.village import Village
import copy


class SettlementData:
    VILLAGE_PROFESSION_LIST = [
                    "farmer", "fisherman", "shepherd", "fletcher", "librarian", "cartographer",
                    "cleric", "armorer", "weaponsmith", "toolsmith", "butcher", "leatherworker", "mason", "nitwit"]

    def __init__(self, village: Village):
        self.villageModel = village
        self.area: list = [0, 0]
        self.center: list = [0, 0]
        self.size: list = []

        self.discoveredChunks: list = []

        # Materials replacement
        self.__materialsReplacement: dict = {}

        # Biome 
        self.biomeId: int = 0
        self.biomeName: str = ""
        self.biomeBlockId: int = 0

        self.__materialsReplacement["villageName"] = self.villageModel.name

        self.villagerNames: list = []
        self.villagerProfession: list = []
        self.villagerGameProfession: list = []

        # [[0 -> content, 1 -> isGift], [...] , ...]
        self.villagerDiary: list = []
        
        self.structuresNumberGoal: list = []

        # structures contains "position", "rotation", "flip" "name", "type", "group", "villagersId", "gift"
        self.structures: list = []
        self.freeVillager: int = 0

        self.resources: dict = {
            "woodResources" : 0,
            "dirtResources" : 0,
            "stoneResources" : 0
        }

        self.murdererData:MurdererData = MurdererData()

    def setArea(self, newArea: tuple) -> None:
        self.area = newArea
        self.center = [int((self.area[0] + self.area[3]) / 2), 80, int((self.area[2] + self.area[5]) / 2)]
        self.size = [self.area[3] - self.area[0] + 1, self.area[5] - self.area[2] + 1]

    def setVillageBiome(self, biomeId: int, resources: Resources) -> None:
        self.biomeId = biomeId
        self.biomeName = resources.biomeMinecraftId[int(self.biomeId)]
        self.biomeBlockId =  str(resources.biomesBlockId[self.biomeName])

        if self.biomeBlockId == "-1": 
            print("Generation on biome block id -1")
            self.biomeBlockId = "0"

    def setMaterialReplacement(self, propertyName: str, replacement: str) -> str:
        self.__materialsReplacement[propertyName] = replacement

    def getMaterialReplacement(self, propertyName: str) -> str:
        return self.__materialsReplacement[propertyName]

    def getMatRepDeepCopy(self) -> dict:
        return copy.deepcopy(self.__materialsReplacement)
